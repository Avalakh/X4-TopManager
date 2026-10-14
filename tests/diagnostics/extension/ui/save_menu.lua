-- Main-menu save selection over a dedicated, allow-listed pipe.
-- This file arms its read at UI startup: MD-backed on-load initialization
-- does not run until a game has been loaded.
local ffi = require("ffi")
local C = ffi.C
ffi.cdef[[
    bool IsStartmenu(void);
    bool IsSaveListLoadingComplete(void);
    bool IsSaveValid(const char* filename);
    void ReloadSaveList(void);
    const char* GetSaveFolderPath(void);
]]

local Pipes = require("extensions.sn_mod_support_apis.ui.named_pipes.Interface")
local Presence = require("extensions.tm_empire_diagnostics.ui.pipe_presence")
local PIPE = "tm_empire_save_menu"
local reconnect_delay = 1
local reconnect_at = nil
local reload_key = nil
local loading_filename = nil
local load_deadline = nil
local arm_read

local function encode(value)
    return tostring(value or ""):gsub("([^A-Za-z0-9_.%-])", function(char)
        return string.format("%%%02X", string.byte(char))
    end)
end

local function reply(key, status, detail)
    return table.concat({"tm_save_menu_result_v1", key, status, detail or "-"}, "|")
end

-- X4 9.00 gameoptions.lua uses this exact native API for its save location.
local function save_folder()
    local ok, value = pcall(function()
        local pointer = C.GetSaveFolderPath()
        if pointer == nil then return nil end
        return ffi.string(pointer)
    end)
    if not ok or type(value) ~= 'string' or value == '' or value:find('%z')
       or #encode(value) > 4096 then return nil end
    return value
end

-- Keep the extra development slot local; stock UI filenames stay unchanged.
local diagnosticSaveFilenames = {}
for name, value in pairs(Helper.validSaveFilenames) do diagnosticSaveFilenames[name] = value end
diagnosticSaveFilenames.save_011 = true
diagnosticSaveFilenames.save_012 = true
diagnosticSaveFilenames.save_013 = true
diagnosticSaveFilenames.save_014 = true
for i = 15, 39 do diagnosticSaveFilenames[string.format('save_%03d', i)] = true end

local function available_saves()
    local saves = GetSaveList(diagnosticSaveFilenames)
    local eligible = {}
    for _, save in ipairs(saves) do
        local filename = save.filename
        if type(filename) == "string" and diagnosticSaveFilenames[filename]
           and not save.error and not save.invalidversion
           and not save.invalidpatches and not save.invalidgameid
           and C.IsSaveValid(filename) then
            eligible[#eligible + 1] = save
        end
    end
    table.sort(eligible, function(a, b) return (a.rawtime or 0) > (b.rawtime or 0) end)
    return eligible
end

local function list_response(key)
    if reload_key ~= key then
        reload_key = key
        C.ReloadSaveList()
        return reply(key, "loading")
    end
    if not C.IsSaveListLoadingComplete() then return reply(key, "loading") end
    local entries = {}
    for _, save in ipairs(available_saves()) do
        local name = (type(save.name) == "string" and save.name ~= "" and save.name)
                     or save.description or save.location or save.filename
        entries[#entries + 1] = table.concat({
            encode(save.filename), encode(name), encode(save.description or save.location or ""),
            tostring(math.max(0, math.floor(tonumber(save.rawtime) or 0)))
        }, ",")
    end
    return reply(key, "list", table.concat(entries, ";"))
end

local function diagnostics_response(key)
    if reload_key ~= key then
        reload_key = key
        C.ReloadSaveList()
        return reply(key, "loading")
    end
    if not C.IsSaveListLoadingComplete() then return reply(key, "loading") end
    local rows = {}
    for _, save in ipairs(GetSaveList(diagnosticSaveFilenames)) do
        local filename = save.filename
        if type(filename) == "string" and diagnosticSaveFilenames[filename] then
            rows[#rows + 1] = table.concat({
                filename, tostring(save.error or ""),
                tostring(not not save.invalidversion), tostring(not not save.invalidpatches),
                tostring(not not save.invalidgameid), tostring(C.IsSaveValid(filename))
            }, ",")
        end
    end
    return reply(key, "diagnostics", table.concat(rows, ";"))
end

local function schedule_reconnect()
    if reconnect_at then return end
    reconnect_at = GetCurRealTime() + reconnect_delay
    reconnect_delay = math.min(reconnect_delay * 2, 10)
end

local function on_request(message)
    if message == "ERROR" then
        schedule_reconnect()
        return
    end
    reconnect_delay = 1
    reconnect_at = nil
    local key = tostring(message):match("^tm_save_menu_v1|([A-Za-z0-9_-]+)|list$")
    local verb = key and "list" or nil
    local argument = ""
    local expected_folder
    if not key then
        key = tostring(message):match("^tm_save_menu_v1|([A-Za-z0-9_-]+)|diagnostics$")
        if key then verb = "diagnostics" end
    end
    if not key then
        key, argument = tostring(message):match("^tm_save_menu_v1|([A-Za-z0-9_-]+)|load|([A-Za-z0-9_]+)$")
        if key then verb = "load" end
    end
    if not key then
        key = tostring(message):match('^tm_save_menu_v1|([A-Za-z0-9_-]+)|folder$')
        if key then verb = 'folder' end
    end
    if not key then
        key, argument, expected_folder = tostring(message):match(
            '^tm_save_menu_v1|([A-Za-z0-9_-]+)|load_bound|([A-Za-z0-9_]+)|([A-Za-z0-9_.%%%-]+)$')
        if key then verb = 'load_bound' end
    end
    local response
    local selected
    if not key or #key < 4 or #key > 64 or #message > (verb == 'load_bound' and 4300 or 256) then
        response = reply("-", "rejected", "malformed")
    elseif not C.IsStartmenu() then
        response = reply(key, "rejected", "not_main_menu")
    elseif verb == "list" and argument == "" then
        response = list_response(key)
    elseif verb == "diagnostics" and argument == "" then
        response = diagnostics_response(key)
    elseif verb == 'folder' then
        local folder = save_folder()
        response = folder and reply(key, 'folder', encode(folder))
                   or reply(key, 'rejected', 'save_folder_unavailable')
    elseif (verb == "load" or verb == 'load_bound') and loading_filename == nil and type(argument) == "string"
           and diagnosticSaveFilenames[argument] and C.IsSaveListLoadingComplete() then
        local folder = verb == 'load_bound' and save_folder() or nil
        local folder_matches = verb ~= 'load_bound' or (folder and encode(folder) == expected_folder)
        if folder_matches then
            for _, save in ipairs(available_saves()) do
                if save.filename == argument then selected = argument; break end
            end
        end
        if selected then
            loading_filename = selected
            response = reply(key, "accepted", encode(selected) .. (verb == 'load_bound' and ',' .. encode(folder) or ''))
        else
            response = reply(key, "rejected", folder_matches and "save_unavailable" or 'save_folder_changed_or_unavailable')
        end
    else
        response = reply(key, "rejected", "unsupported_or_unavailable")
    end
    Pipes.Schedule_Write(PIPE, function(write_result)
        if write_result ~= "SUCCESS" then
            loading_filename = nil
            load_deadline = nil
            schedule_reconnect()
        elseif selected then
            -- Match vanilla's deferred call so the triggering UI operation ends first.
            Helper.addDelayedOneTimeCallbackOnUpdate(function()
                if expected_folder then
                    local current = save_folder()
                    if not C.IsStartmenu() or not current or encode(current) ~= expected_folder then
                        loading_filename = nil
                        load_deadline = nil
                        arm_read()
                        return
                    end
                end
                LoadGame(selected)
            end, true, getElapsedTime() + 0.1)
            -- A failed native load must not leave this UI instance permanently locked.
            load_deadline = GetCurRealTime() + 30
        else
            arm_read()
        end
    end, response)
end

arm_read = function()
    if not Presence.available(PIPE) then
        reconnect_at = GetCurRealTime() + 2
        return
    end
    Pipes.Schedule_Read(PIPE, on_request, false)
end

-- The Mod Support APIs frame timer starts only after MD game initialization.
-- At the start menu, drive its pending pipe operations and retries with the
-- native UI update event. Do no pipe polling once gameplay has started.
local function on_update()
    if not C.IsStartmenu() then return end
    local now = GetCurRealTime()
    if load_deadline and now >= load_deadline then
        load_deadline = nil
        loading_filename = nil
        arm_read()
    end
    if reconnect_at and now >= reconnect_at then
        reconnect_at = nil
        arm_read()
    end
    if Pipes.read_polling_active then Pipes.Poll_For_Reads() end
    if Pipes.write_polling_active then Pipes.Poll_For_Writes() end
end

SetScript("onUpdate", on_update)
arm_read()

