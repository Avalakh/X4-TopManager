local realffi = require('ffi')
local rows, count, loop, ship, unavailable, mismatch = {}, 0, false, true, false, false
local C = {
    IsComponentClass=function() return ship end,
    GetOrderQueueFirstLoopIdx=function(_, valid) valid[0]=loop; return 0 end,
    GetNumOrders=function() if unavailable then error('queue unavailable') end; return count end,
    GetOrders3=function(buffer, length)
        for i=0,length-1 do
            buffer[i].isoverride=rows[i+1] and rows[i+1].manual or false
            buffer[i].ispriority=rows[i+1] and rows[i+1].priority or false
        end
        return mismatch and length-1 or length
    end,
}
package.loaded.ffi={C=C,typeof=realffi.typeof,cdef=realffi.cdef,new=realffi.new}
ConvertIDTo64Bit=function() return 10 end
Register_Require_With_Init=function() end
local guard=dofile('X4_TopManager/ui/player_order_guard.lua')
assert(guard.reason(10)==nil)
count=2; rows={{},{manual=true}}
assert(guard.reason(10)=='manual_or_priority_order')
rows={{},{priority=true}}
assert(guard.reason(10)=='manual_or_priority_order')
rows={{},{}}; assert(guard.reason(10)==nil)
loop=true; assert(guard.reason(10)=='manual_or_priority_order'); loop=false
count=33; assert(guard.reason(10)=='order_queue_inspection_incomplete')
count=2; mismatch=true; assert(guard.reason(10)=='order_queue_inspection_incomplete'); mismatch=false
unavailable=true; assert(guard.reason(10)=='order_queue_inspection_unavailable')
ship=false; assert(guard.reason(10)==nil)
print('PASS: native queue buffer, queued manual/priority, bounded and unavailable data')
