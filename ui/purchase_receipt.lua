-- Узкий внутриигровой адаптер: отмечает уже оплаченную штатную постройку.
-- Не выбирает корабли, не переводит деньги и не принимает команды pipes.
local ffi = require('ffi')
ffi.cdef[[
typedef unsigned long long UniverseID;
typedef unsigned long long BuildTaskID;
typedef struct {
    BuildTaskID id;
    UniverseID buildingcontainer;
    UniverseID component;
    const char* macro;
    const char* factionid;
    UniverseID buildercomponent;
    int64_t price;
    bool ismissingresources;
    uint32_t queueposition;
} BuildTaskInfo;
UniverseID GetPlayerID(void);
UniverseID GetTopLevelContainer(UniverseID componentid);
BuildTaskInfo GetBuildTaskInfo(BuildTaskID id);
void SetBuildTaskTransferredMoney(BuildTaskID id, int64_t value);
]]
local M = {}

function M.valid(data)
    if type(data) ~= 'table' or data.schema ~= 1 or data.state ~= 'payment_sent'
       or type(data.build) ~= 'userdata' or type(data.shipyard) ~= 'userdata'
       or type(data.paid) ~= 'number' or data.paid <= 0 or data.paid > 9007199254740991
       or data.paid % 1 ~= 0
       or type(data.price) ~= 'number' or data.price <= 0 or data.price % 1 ~= 0
       or type(data.crewprice) ~= 'number' or data.crewprice < 0 or data.crewprice % 1 ~= 0
       or data.paid ~= data.price + data.crewprice
       or type(data.macro) ~= 'string' or #data.macro == 0 or #data.macro > 256 then
        return false
    end
    return true
end

function M.record(_, shipyard)
    local player = ffi.C.GetPlayerID()
    if player == 0 or type(shipyard) ~= 'userdata' then return false end
    local data = GetNPCBlackboard(ConvertStringToLuaID(tostring(player)), '$tm_empire_purchase')
    if not M.valid(data) then return false end
    local expected = ConvertIDTo64Bit(data.shipyard)
    if ConvertIDTo64Bit(shipyard) ~= expected then return false end
    local build = ConvertIDTo64Bit(data.build)
    local info = ffi.C.GetBuildTaskInfo(build)
    if info.id == 0 or info.id ~= build or info.buildingcontainer ~= expected
       or tonumber(info.price) ~= data.price
       or ffi.string(info.factionid) ~= 'player' or ffi.string(info.macro) ~= data.macro then
        return false
    end
    -- Native MD subsequently reads build.transferredamount; this call is not
    -- payment success or ship readiness. Repeating the same amount is a set.
    ffi.C.SetBuildTaskTransferredMoney(build, data.paid)
    return true
end

function M.init()
    RegisterEvent('TM_Empire.RecordPaidBuild', M.record)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.purchase_receipt', M, M.init)
