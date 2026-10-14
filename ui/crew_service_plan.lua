-- Read the same installed components used by the stock ship configuration
-- menu. No equipment order may be submitted from an incomplete snapshot.
local ffi = require('ffi')
local M = {}

local function str(value)
    return value ~= nil and ffi.string(value) or ''
end

local function currentMacroSlots(plan, shipid, typeid)
    local entries = {}
    local count = tonumber(ffi.C.GetNumUpgradeSlots(shipid, '', typeid))
    for slot = 1, count do
        local group = ffi.C.GetUpgradeSlotGroup(shipid, '', typeid, slot)
        if typeid == 'engine' or (str(group.path) == '..' and str(group.group) == '') then
            local macro = str(ffi.C.GetUpgradeSlotCurrentMacro(shipid, 0, typeid, slot))
            local entry = {macro=macro, ammomacro='', weaponmode=''}
            local component = ffi.C.GetUpgradeSlotCurrentComponent(shipid, typeid, slot)
            if component ~= 0 and ffi.C.IsComponentClass(component, 'weapon') then
                entry.weaponmode = str(ffi.C.GetWeaponMode(component))
                if ffi.C.IsComponentClass(component, 'missilelauncher') then
                    entry.ammomacro = str(ffi.C.GetCurrentAmmoOfWeapon(component))
                end
            end
            entries[slot] = entry
        else
            entries[slot] = {macro='', ammomacro='', weaponmode=''}
        end
    end
    plan[typeid] = entries
end

local function currentGroups(plan, shipid)
    local count = tonumber(ffi.C.GetNumUpgradeGroups(shipid, ''))
    local groups = ffi.new('UpgradeGroup[?]', count)
    count = tonumber(ffi.C.GetUpgradeGroups(groups, count, shipid, ''))
    local sorted = {}
    for i = 0, count - 1 do
        local path, group = str(groups[i].path), str(groups[i].group)
        if path ~= '..' or group ~= '' then
            table.insert(sorted, {path=path, group=group})
        end
    end
    table.sort(sorted, function(a, b) return a.group < b.group end)
    plan.enginegroup, plan.shieldgroup, plan.turretgroup = {}, {}, {}
    for index, key in ipairs(sorted) do
            local path, group = key.path, key.group
            for _, pair in ipairs({{'enginegroup','engine'}, {'shieldgroup','shield'}, {'turretgroup','turret'}}) do
                local info = ffi.C.GetUpgradeGroupInfo(shipid, '', path, group, pair[2])
                local macro = str(info.currentmacro)
                local mode = ''
                if pair[2] == 'turret' and info.currentcomponent ~= 0 then
                    mode = str(ffi.C.GetTurretGroupMode2(shipid, 0, path, group))
                end
                plan[pair[1]][index] = {macro=macro, count=tonumber(info.count),
                    path=path, group=group, ammomacro='', weaponmode=mode}
            end
    end
end

local function currentAmmo(plan, shipid)
    for _, source in ipairs({
        {'missile', 'GetNumAllMissiles', 'GetAllMissiles'},
        {'deployable', 'GetNumAllLaserTowers', 'GetAllLaserTowers'},
        {'deployable', 'GetNumAllSatellites', 'GetAllSatellites'},
        {'deployable', 'GetNumAllMines', 'GetAllMines'},
        {'deployable', 'GetNumAllNavBeacons', 'GetAllNavBeacons'},
        {'deployable', 'GetNumAllResourceProbes', 'GetAllResourceProbes'},
        {'countermeasure', 'GetNumAllCountermeasures', 'GetAllCountermeasures'},
    }) do
        local count = tonumber(ffi.C[source[2]](shipid))
        local buffer = ffi.new('AmmoData[?]', count)
        count = tonumber(ffi.C[source[3]](buffer, count, shipid))
        for i = 0, count - 1 do
            local macro = str(buffer[i].macro)
            if macro == '' or plan[source[1]][macro] then return false end
            plan[source[1]][macro] = tonumber(buffer[i].amount)
        end
    end
    local count = tonumber(ffi.C.GetNumAllUnits(shipid, false))
    local buffer = ffi.new('UnitData[?]', count)
    count = tonumber(ffi.C.GetAllUnits(buffer, count, shipid, false))
    for i = 0, count - 1 do
        local macro, category = str(buffer[i].macro), str(buffer[i].category)
        if macro == '' or plan.drone[macro] then return false end
        -- Stock ship configuration excludes these two unit categories.
        if category ~= 'marine' and category ~= 'police' then
            plan.drone[macro] = tonumber(buffer[i].amount)
        end
    end
    return true
end

function M.snapshot(ship, added)
    if type(ship) ~= 'userdata' or type(added) ~= 'number' or added < 1
        or added > 16 or added % 1 ~= 0 then return nil, 'invalid_crew_service_target' end
    local shipid = ConvertIDTo64Bit(ship)
    local plan = {missile={}, drone={}, deployable={}, countermeasure={}}
    if not currentAmmo(plan, shipid) then return nil, 'current_ammo_ambiguous' end
    for _, typeid in ipairs({'engine', 'shield', 'weapon', 'turret'}) do
        currentMacroSlots(plan, shipid, typeid)
    end
    currentGroups(plan, shipid)
    plan.thruster = {}
    local thrusters = tonumber(ffi.C.GetNumVirtualUpgradeSlots(shipid, '', 'thruster'))
    for slot = 1, thrusters do
        plan.thruster[slot] = {macro=str(ffi.C.GetVirtualUpgradeSlotCurrentMacro(shipid, 'thruster', slot))}
    end
    plan.software = {}
    local slots = tonumber(ffi.C.GetNumSoftwareSlots(shipid, ''))
    local software = ffi.new('SoftwareSlot[?]', slots)
    slots = tonumber(ffi.C.GetSoftwareSlots(software, slots, shipid, ''))
    for i = 0, slots - 1 do plan.software[i + 1] = str(software[i].current) end
    plan.crew = {}
    local roles = tonumber(ffi.C.GetNumAllRoles())
    local people = ffi.new('PeopleInfo[?]', roles)
    roles = tonumber(ffi.C.GetPeople2(people, roles, shipid, true))
    for i = 0, roles - 1 do
        local role = str(people[i].id)
        if role == 'service' or role == 'marine' then
            plan.crew[role] = tonumber(people[i].amount)
        end
    end
    plan.crew.service = (plan.crew.service or 0) + added
    local engine = plan.engine[1] and plan.engine[1].macro
    if not engine or engine == '' then return nil, 'current_engine_unavailable' end
    return plan, nil, {engine=engine, crew=plan.crew.service,
        software=#plan.software, added=added}
end

Register_Require_With_Init('extensions.tm_empire_management.ui.crew_service_plan', M, function() end)
return M
