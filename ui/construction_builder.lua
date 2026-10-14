-- MapMenu.selectCV: native fee and deployment, approved by the MD build claim.
local ffi=require('ffi')
ffi.cdef[[
int64_t GetBuilderHiringFee(void);
bool IsBuilderBusy(uint64_t);
bool IsOrderSelectableFor(const char*, uint64_t);
uint32_t CreateDeployToStationOrder(uint64_t);
bool EnableOrder(uint64_t, size_t);
uint32_t GetNumOrders(uint64_t);
]]
local M={}
local function owner() return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID())) end
local function integer(x) return type(x)=='number' and x>=0 and x<=9007199254740991 and x%1==0 end
local function budget(x) return type(x)=='number' and x>=0 and x<=9007199254740991 end
local function trueValue(x) return x==true or x==1 end
local function failure(value)
    local detail=tostring(value):sub(1,256)
    local code=detail:match('([%w_]+)$')
    if code and (code:match('^builder_') or code:match('^native_builder_')) then return code,detail end
    return 'native_builder_hire_unconfirmed',detail
end
local function read(state)
    local player=owner()
    local r=GetNPCBlackboard(player,'$tm_empire_builder_request')
    if type(r)~='table' or r.schema~=1 or r.state~=state
        or type(r.key)~='string' or #r.key<1 or #r.key>128
        or type(r.ship)~='userdata' or type(r.station)~='userdata'
        or type(r.storage)~='userdata' or not budget(r.budget) then return end
    return player,r
end
local function check(r)
    local ship,station,storage=ConvertIDTo64Bit(r.ship),ConvertIDTo64Bit(r.station),ConvertIDTo64Bit(r.storage)
    assert(trueValue(GetComponentData(r.station,'isplayerowned')) and trueValue(GetComponentData(r.storage,'isplayerowned')),'builder_destination_lost')
    local own,enemy=GetComponentData(r.ship,'isplayerowned','isreallyenemy')
    assert(not trueValue(own) and not trueValue(enemy) and ffi.C.IsComponentOperational(ship),'builder_unavailable')
    assert(not ffi.C.IsBuilderBusy(ship) and ffi.C.GetNumOrders(ship)==0,'builder_busy')
    assert(ffi.C.IsOrderSelectableFor('DeployToStation',ship),'builder_order_unavailable')
    local fee=tonumber(ffi.C.GetBuilderHiringFee())
    assert(integer(fee) and fee>0 and fee<=r.budget and fee<=GetPlayerMoney(),'builder_fee_unavailable')
    return ship,storage,fee
end
local function report(player,r,result)
    SetNPCBlackboard(player,'$tm_empire_builder_result',result)
    AddUITriggeredEvent('TM_Empire_Construction','BuilderHiringUpdated')
end
function M.quote()
    local player,r=read('check_requested'); if not r then return end
    local previous=GetNPCBlackboard(player,'$tm_empire_builder_result')
    if type(previous)=='table' and previous.key==r.key then return end
    local ok,ship,storage,fee=pcall(check,r)
    local reason,detail=''
    if not ok then reason,detail=failure(ship) end
    report(player,r,{key=r.key,state=ok and 'quoted' or 'rejected_before_effect',
        fee=ok and fee or nil,reason=reason,detail=detail})
end
function M.submit()
    local player,r=read('approved'); if not r then return end
    local previous=GetNPCBlackboard(player,'$tm_empire_builder_result')
    if type(previous)~='table' or previous.key~=r.key or previous.state~='quoted' then return end
    local ok,ship,storage,fee=pcall(check,r)
    if not ok or fee~=r.fee then
        local reason,detail=failure(ship)
        return report(player,r,{key=r.key,state='rejected_before_effect',reason=ok and 'builder_fee_changed' or reason,detail=not ok and detail or nil})
    end
    local current=GetNPCBlackboard(player,'$tm_empire_builder_request')
    if type(current)~='table' or current.key~=r.key or current.state~='approved'
        or not IsSameComponent(current.ship,r.ship) or not IsSameComponent(current.storage,r.storage)
        or not IsSameComponent(current.station,r.station) or current.budget~=r.budget
        or current.fee~=fee then return end
    local result={key=r.key,state='unknown',reason='native_builder_hire_outcome_pending',fee=fee,before=GetPlayerMoney()}
    SetNPCBlackboard(player,'$tm_empire_builder_result',result)
    local called,error=pcall(function()
        TransferPlayerMoneyTo(fee,ship)
        result.after=GetPlayerMoney()
        assert(result.before-result.after==fee,'native_builder_payment_unconfirmed')
        result.paid=fee
        SetNPCBlackboard(player,'$tm_empire_builder_result',result)
        local index=tonumber(ffi.C.CreateDeployToStationOrder(ship))
        assert(index and index>0,'native_builder_order_unconfirmed')
        result.orderindex=index
        result.destination_version=2
        SetNPCBlackboard(player,'$tm_empire_builder_result',result)
        -- Native DeployToStation takes the station; its AI resolves buildstorage.
        SetOrderParam(r.ship,index,1,nil,r.station)
        assert(ffi.C.EnableOrder(ship,index),'native_builder_order_not_enabled')
        result.state='sent'; result.reason='native_hired_builder_deployment_pending'
    end)
    if not called then result.reason,result.detail=failure(error) end
    report(player,r,result)
end
function M.recover()
    local player,r=read('recovery_approved'); if not r then return end
    local previous=GetNPCBlackboard(player,'$tm_empire_builder_result')
    if type(previous)~='table' or previous.key~=r.key or previous.state~='sent'
        or previous.destination_version~=nil or previous.recovery_attempted
        or not integer(previous.fee) or previous.fee<=0 or previous.paid~=previous.fee
        or type(previous.before)~='number' or type(previous.after)~='number'
        or previous.before-previous.after~=previous.paid or not integer(previous.orderindex)
        or previous.orderindex<1 then return end
    local ship=ConvertIDTo64Bit(r.ship)
    local station,storage=ConvertIDTo64Bit(r.station),ConvertIDTo64Bit(r.storage)
    local own,enemy=GetComponentData(r.ship,'isplayerowned','isreallyenemy')
    if trueValue(own) or trueValue(enemy) or not ffi.C.IsComponentOperational(ship)
        or not trueValue(GetComponentData(r.station,'isplayerowned')) or not trueValue(GetComponentData(r.storage,'isplayerowned'))
        or ffi.C.IsBuilderBusy(ship) or ffi.C.GetNumOrders(ship)~=0
        or not ffi.C.IsOrderSelectableFor('DeployToStation',ship) then return end
    local current=GetNPCBlackboard(player,'$tm_empire_builder_request')
    if type(current)~='table' or current.key~=r.key or current.state~='recovery_approved'
        or not IsSameComponent(current.ship,r.ship) or not IsSameComponent(current.station,r.station)
        or not IsSameComponent(current.storage,r.storage) or current.budget~=r.budget then return end
    -- One migration of the proven paid legacy order; never debit or replay it.
    previous.recovery_attempted=true
    previous.state='unknown'; previous.reason='native_builder_recovery_pending'
    SetNPCBlackboard(player,'$tm_empire_builder_result',previous)
    local ok,err=pcall(function()
        local index=tonumber(ffi.C.CreateDeployToStationOrder(ship))
        assert(index and index>0,'native_builder_order_unconfirmed')
        previous.orderindex=index; previous.destination_version=2
        SetNPCBlackboard(player,'$tm_empire_builder_result',previous)
        SetOrderParam(r.ship,index,1,nil,r.station)
        assert(ffi.C.EnableOrder(ship,index),'native_builder_order_not_enabled')
        previous.state='sent'; previous.reason='native_hired_builder_deployment_pending'
    end)
    if not ok then previous.reason,previous.detail=failure(err) end
    report(player,r,previous)
end
function M.init()
    RegisterEvent('TM_Empire.QuoteBuilder',M.quote)
    RegisterEvent('TM_Empire.HireBuilder',M.submit)
    RegisterEvent('TM_Empire.RecoverBuilder',M.recover)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.construction_builder',M,M.init)
