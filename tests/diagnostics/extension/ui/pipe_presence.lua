-- Try TopManager pipes without asking the provider to log missing servers.
-- A successful handle is passed to the same provider for normal I/O.
local ffi = require("ffi")
local Time = require("extensions.sn_mod_support_apis.ui.time.Interface")
local Pipes = require("extensions.sn_mod_support_apis.ui.named_pipes.Interface")
local winpipe = require("extensions.sn_mod_support_apis.ui.c_library.winpipe")
ffi.cdef[[
    typedef unsigned long long UniverseID;
    UniverseID GetPlayerID(void);
]]

local waiting = {}
local md_pipes = {}
local last_md = {}
local next_poll = 0

local function available(pipe)
    if not winpipe then return false end
    Pipes.Declare_Pipe(pipe)
    local state = Pipes.pipes[pipe]
    if state.file then return true end
    local ok, file = pcall(winpipe.open_pipe, Pipes.pipe_path_prefix .. pipe)
    if not ok or not file then return false end
    state.file = file
    state.retry_allowed = false
    return true
end

local function when_ready(pipe, callback)
    if available(pipe) then callback(); return end
    waiting[pipe] = callback -- One pending client per pipe.
end

local function poll(now)
    if now < next_poll then return end
    next_poll = now + 2
    for pipe, callback in pairs(waiting) do
        if available(pipe) then
            waiting[pipe] = nil
            callback()
        end
    end
    local player = ffi.C.GetPlayerID()
    if player == 0 then return end
    for _, entry in ipairs(md_pipes) do
        local ready = available(entry[1])
        if last_md[entry[1]] ~= ready then
            SetNPCBlackboard(player, entry[2], ready)
            last_md[entry[1]] = ready
        end
    end
end

local function init()
    next_poll = 0
    last_md = {}
    Time.Unregister_NewFrame_Callback(poll)
    Time.Register_NewFrame_Callback(poll)
end

Register_Require_With_Init("extensions.tm_empire_diagnostics.ui.pipe_presence", {
    available = available,
    when_ready = when_ready,
}, init)

