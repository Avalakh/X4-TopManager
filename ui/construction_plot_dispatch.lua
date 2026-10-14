-- Typed MD plot request; native geometry mutation stays in MD.
local ffi = require('ffi')
local M = {}
local function owner()
    return ConvertStringToLuaID(tostring(ffi.C.GetPlayerID()))
end
function M.quote()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_plot_request')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'quote_requested'
        or type(request.key) ~= 'string' then return end
    local plot = require('extensions.tm_empire_management.ui.construction_plot')
    local quote, reason = plot.quote(request)
    local current = GetNPCBlackboard(player, '$tm_empire_plot_request')
    if type(current) ~= 'table' or current.state ~= 'quote_requested' or current.key ~= request.key then return end
    if quote then request.state, request.quote = 'quote_ready', quote
    else request.state, request.reason = 'quote_failed', reason end
    SetNPCBlackboard(player, '$tm_empire_plot_request', request)
    AddUITriggeredEvent('TM_Empire_Construction', 'PlotQuoteReady')
end
function M.license()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_plot_request')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'licence_approved'
        or type(request.key) ~= 'string' or type(request.quote) ~= 'table' then return end
    local function canAct()
        local current = GetNPCBlackboard(player, '$tm_empire_plot_request')
        return type(current) == 'table' and current.schema == 1 and current.state == 'licence_approved'
            and current.key == request.key and IsSameComponent(current.station, request.station)
            and current.budget == request.budget
            and current.newconstruction == request.newconstruction
    end
    local plot = require('extensions.tm_empire_management.ui.construction_plot')
    local receipt, reason = plot.license({key=request.key, station=request.station,
        budget=request.budget, expected=request.quote,newconstruction=request.newconstruction}, canAct)
    request.state = receipt and receipt.state or 'licence_failed'
    request.reason = receipt and receipt.reason or reason
    SetNPCBlackboard(player, '$tm_empire_plot_request', request)
    AddUITriggeredEvent('TM_Empire_Construction', 'PlotLicenceSubmitted')
end
function M.reserve()
    local player = owner()
    local request = GetNPCBlackboard(player, '$tm_empire_reservation_request')
    if type(request) ~= 'table' or request.schema ~= 1 or request.state ~= 'approved' then return end
    local function canAct()
        local current = GetNPCBlackboard(player, '$tm_empire_reservation_request')
        if type(current) ~= 'table' or current.schema ~= 1 or current.state ~= 'approved'
            or current.key ~= request.key or current.sector ~= request.sector or current.set ~= request.set then return false end
        for _, field in ipairs({'position', 'size'}) do
            if type(current[field]) ~= 'table' or type(request[field]) ~= 'table' then return false end
            for _, axis in ipairs({'x', 'y', 'z'}) do
                if current[field][axis] ~= request[field][axis] then return false end
            end
        end
        return true
    end
    local reserve = require('extensions.tm_empire_management.ui.construction_reserve')
    local receipt, reason = reserve.reserve(request, canAct)
    request.state = receipt and receipt.state or 'revoked'
    request.reason = receipt and receipt.reason or reason
    SetNPCBlackboard(player, '$tm_empire_reservation_request', request)
    AddUITriggeredEvent('TM_Empire_Construction', 'StationPlotSubmitted')
end
function M.init()
    RegisterEvent('TM_Empire.QuotePlot', M.quote)
    RegisterEvent('TM_Empire.LicensePlot', M.license)
    RegisterEvent('TM_Empire.ReserveStationPlot', M.reserve)
end
Register_Require_With_Init('extensions.tm_empire_management.ui.construction_plot_dispatch', M, M.init)
