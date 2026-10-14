local playerOrderReason
package.preload['extensions.tm_empire_management.ui.player_order_guard']=function() return {reason=function() return playerOrderReason end} end
-- Actual LuaJIT uint64 arithmetic, no game effects or mocked seed arithmetic.
local api
Register_Require_With_Init=function(name,module)
    assert(name=='extensions.tm_empire_management.ui.personnel_transfer'); api=module
end
dofile('X4_TopManager/ui/personnel_transfer.lua')
for _, value in ipairs({'0','9007199254740993','9873631311134785487','18446744073709551615'}) do
    assert(tostring(api.seed64(value))==value .. 'ULL')
end
assert(tostring(api.seed64('-1'))=='18446744073709551615ULL')
assert(tostring(api.seed64('-9223372036854775808'))=='9223372036854775808ULL')
for _, value in ipairs({'18446744073709551616','-9223372036854775809','1.0','1e3','',9007199254740992}) do
    assert(not pcall(api.seed64,value))
end
