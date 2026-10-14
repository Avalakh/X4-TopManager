-- Repair TopManager's native transport without replacing the provider's files
-- or File metatable. Other mods continue to use their original native API.
local PROVIDER = "extensions.sn_mod_support_apis.ui.c_library.winpipe"
local DLL = ".\\extensions\\tm_empire_diagnostics\\ui_c_library_winpipe_64.txt"
local PREFIX = "\\\\.\\pipe\\tm_empire_"
local state = {ready = false, reason = "native_pipe_unavailable"}

local function report(reason)
    state.reason = reason
    if DebugError then DebugError("TopManager native pipe: " .. reason) end
end

if package == nil or package.config:sub(1, 1) ~= "\\" then
    report("unsupported_platform")
elseif GetUISafeModeOption() ~= false then
    report("protected_ui")
else
    local provider = require(PROVIDER)
    if type(provider) ~= "table" or type(provider.open_pipe) ~= "function" then
        report("provider_unavailable")
    else
        local original = provider.open_pipe
        local ok, native = pcall(function()
            local entry, reason = package.loadlib(DLL, "luaopen_winpipe")
            if not entry then error(reason or "missing_entrypoint") end
            return entry()
        end)
        if not ok or type(native) ~= "table" or type(native.open_pipe) ~= "function"
            or type(native.GetLastError) ~= "function"
            or native.ERROR_NO_DATA ~= provider.ERROR_NO_DATA
            or native.ERROR_IO_PENDING ~= provider.ERROR_IO_PENDING then
            report("native_pipe_load_failed")
        else
            provider.open_pipe = function(name, ...)
                if type(name) == "string" and name:sub(1, #PREFIX) == PREFIX then
                    return native.open_pipe(name, ...)
                end
                return original(name, ...)
            end
            state.ready = true
            report("ready/registry-buffer-utf8-v1")
        end
        -- Missing repair must never silently open a known unsafe native File.
        if not state.ready then
            provider.open_pipe = function(name, ...)
                if type(name) == "string" and name:sub(1, #PREFIX) == PREFIX then
                    error("TopManager native_pipe_unavailable")
                end
                return original(name, ...)
            end
        end
    end
end

Register_Require_Response("extensions.tm_empire_diagnostics.ui.native_pipe", state)

