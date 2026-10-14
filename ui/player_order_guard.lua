-- Read the native queue immediately before asynchronous player effects.
local ffi = require('ffi')
local M = {}
if not pcall(ffi.typeof, 'Order3') then
    ffi.cdef[[typedef struct {
        size_t queueidx; const char* state; const char* statename;
        const char* orderdef; size_t actualparams; bool enabled;
        bool isinfinite; bool issyncpointreached; bool istemporder;
        bool isoverride; bool ispriority;
    } Order3;]]
end
ffi.cdef[[
bool IsComponentClass(uint64_t componentid, const char* classname);
uint32_t GetNumOrders(uint64_t controllableid);
uint32_t GetOrders3(Order3* result, uint32_t resultlen, uint64_t controllableid);
size_t GetOrderQueueFirstLoopIdx(uint64_t controllableid, bool* isvalid);
]]
local function inspect(component)
    local id = ConvertIDTo64Bit(component)
    if not ffi.C.IsComponentClass(id, 'ship') then return nil end
    local hasloop = ffi.new('bool[1]')
    ffi.C.GetOrderQueueFirstLoopIdx(id, hasloop)
    if hasloop[0] then return 'manual_or_priority_order' end
    local count = tonumber(ffi.C.GetNumOrders(id))
    if not count or count < 0 or count > 32 then
        return 'order_queue_inspection_incomplete'
    end
    if count == 0 then return nil end
    local orders = ffi.new('Order3[?]', count)
    local read = tonumber(ffi.C.GetOrders3(orders, count, id))
    if read ~= count or tonumber(ffi.C.GetNumOrders(id)) ~= count then
        return 'order_queue_inspection_incomplete'
    end
    for index = 0, count - 1 do
        if orders[index].isoverride or orders[index].ispriority then
            return 'manual_or_priority_order'
        end
    end
    return nil
end
function M.reason(component)
    local ok, reason = pcall(inspect, component)
    if not ok then return 'order_queue_inspection_unavailable' end
    return reason
end
function M.init() end
Register_Require_With_Init('extensions.tm_empire_management.ui.player_order_guard', M, M.init)
return M
