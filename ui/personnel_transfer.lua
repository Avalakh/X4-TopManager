-- MapMenu.performCrewExchange: one existing ordinary employee, no hiring.
local ffi=require('ffi')
local playerOrders=require('extensions.tm_empire_management.ui.player_order_guard')
local M={}
if not pcall(ffi.typeof,'UICrewExchangeResult') then
    ffi.cdef[[typedef struct {const char* reason; uint64_t person; uint64_t partnerperson;} UICrewExchangeResult;]]
end
ffi.cdef[[
UICrewExchangeResult PerformCrewExchange2(uint64_t, uint64_t, uint64_t*, uint32_t, uint64_t*, uint32_t, uint64_t, uint64_t, bool, bool);
bool IsPerson(uint64_t, uint64_t);
bool IsPersonTransferScheduled(uint64_t, uint64_t);
const char* GetPersonRole(uint64_t, uint64_t);
uint64_t GetPlayerControlledShipID(void);
]]
local function owner() return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID())) end
local function seed64(text)
    assert(type(text)=='string' and text:match('^-?%d+$'),'invalid_person_seed')
    local negative=text:sub(1,1)=='-'
    local digits=negative and text:sub(2) or text
    digits=digits:gsub('^0+',''); if digits=='' then digits='0' end
    local maximum=negative and '9223372036854775808' or '18446744073709551615'
    assert(#digits<#maximum or (#digits==#maximum and digits<=maximum),'person_seed_out_of_range')
    local value=ffi.new('uint64_t',0)
    for i=1,#digits do value=value*10+(digits:byte(i)-48) end
    return negative and ffi.new('uint64_t',0)-value or value
end
M.seed64=seed64
local function read(expected)
    local player=owner()
    local request=GetNPCBlackboard(player,'$tm_empire_crew_exchange_request')
    if type(request)~='table' or request.schema~=1 or request.state~=expected
       or type(request.key)~='string' or #request.key<1 or #request.key>128
       or type(request.source)~='userdata' or type(request.target)~='userdata'
       or type(request.role)~='string' then return end
    return player,request
end
local function validate(request)
    assert(request.role=='service' or request.role=='marine','crew_role_unsupported')
    local source,target=ConvertIDTo64Bit(request.source),ConvertIDTo64Bit(request.target)
    assert(source~=0 and target~=0 and source~=target,'crew_assets_unavailable')
    local sourceOwned=GetComponentData(request.source,'isplayerowned')
    local targetOwned=GetComponentData(request.target,'isplayerowned')
    assert((sourceOwned==true or sourceOwned==1) and (targetOwned==true or targetOwned==1),'crew_ownership_changed')
    assert(ffi.C.IsComponentOperational(source) and ffi.C.IsComponentOperational(target),'crew_assets_unavailable')
    local controlled=ffi.C.GetPlayerControlledShipID()
    assert(controlled~=source and controlled~=target,'player_helm')
    local protected=playerOrders.reason(request.source) or playerOrders.reason(request.target)
    if protected then error(protected,0) end
    local seed=seed64(request.seed)
    assert(ffi.C.IsPerson(seed,source) and not ffi.C.IsPerson(seed,target),'crew_membership_changed')
    assert(not ffi.C.IsPersonTransferScheduled(source,seed),'crew_transfer_already_scheduled')
    assert(ffi.string(ffi.C.GetPersonRole(seed,source))==request.role,'crew_role_changed')
    local people=ffi.new('uint64_t[1]',seed)
    local check=ffi.C.PerformCrewExchange2(source,target,people,1,nil,0,0,0,false,true)
    local reason=ffi.string(check.reason)
    assert(reason=='',reason)
    return source,target,people
end
local function report(player,key,state,reason,event,binding)
    local result={key=key,state=state,reason=tostring(reason or ''):sub(1,256)}
    if binding then
        result.source,result.target,result.seed,result.role=binding.source,binding.target,binding.seed,binding.role
    end
    SetNPCBlackboard(player,'$tm_empire_crew_exchange_result',result)
    AddUITriggeredEvent('TM_Empire_Personnel',event)
end
function M.check()
    local player,request=read('check_requested'); if not request then return end
    local previous=GetNPCBlackboard(player,'$tm_empire_crew_exchange_result')
    if type(previous)=='table' and previous.key==request.key then return end
    local ok,reason=pcall(validate,request)
    report(player,request.key,ok and 'checked' or 'rejected_before_effect',ok and '' or reason,'CrewChecked',request)
end
function M.submit()
    local player,request=read('approved'); if not request then return end
    local previous=GetNPCBlackboard(player,'$tm_empire_crew_exchange_result')
    if type(previous)~='table' or previous.key~=request.key or previous.state~='checked' then return end
    if type(previous.source)~='userdata' or type(previous.target)~='userdata'
       or not IsSameComponent(previous.source,request.source)
       or not IsSameComponent(previous.target,request.target)
       or previous.seed~=request.seed or previous.role~=request.role then
        return report(player,request.key,'rejected_before_effect','crew_approval_binding_changed','CrewSubmitted')
    end
    local ok,source,target,people=pcall(validate,request)
    if not ok then return report(player,request.key,'rejected_before_effect',source,'CrewSubmitted') end
    -- Persist before the native effect. Unknown is never submitted again.
    SetNPCBlackboard(player,'$tm_empire_crew_exchange_result',{key=request.key,state='unknown',reason='native_crew_exchange_outcome_pending'})
    local called,result=pcall(ffi.C.PerformCrewExchange2,source,target,people,1,nil,0,0,0,false,false)
    local reason=called and ffi.string(result.reason) or tostring(result)
    report(player,request.key,called and reason=='' and 'sent' or 'unknown',reason,'CrewSubmitted')
end
function M.init()
    RegisterEvent('TM_Empire.CheckCrewExchange',M.check)
    RegisterEvent('TM_Empire.SubmitCrewExchange',M.submit)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.personnel_transfer',M,M.init)
