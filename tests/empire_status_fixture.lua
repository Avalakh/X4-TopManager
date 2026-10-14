local callbacks = {}
local menu = {mode='empire', registerCallback=function(name, fn, id)
    assert(id and not callbacks[name]); callbacks[name]=fn
end}
local projection
local api
local projectionChanged
RegisterEvent = function(name, callback)
    assert(name=='TM_Empire.StatusUpdated'); projectionChanged=callback
end
getElapsedTime = function() return 100 end
ConvertStringToLuaID = function(value) return tonumber(value) end
package.preload.ffi = function() return {cdef=function() end, C={GetPlayerID=function() return 7 end}} end
Helper = {getMenu=function(name) assert(name=='PlayerInfoMenu'); return menu end}
GetNPCBlackboard = function(player, key)
    assert(player==7 and key=='$tm_empire_projection'); return projection
end
DebugError = function(message) error(message) end
Register_Require_With_Init = function(name, module, init) api=module; init() end
assert(loadfile('X4_TopManager/ui/empire_status.lua'))()
assert(callbacks.createPlayerInfo_on_start and callbacks.createInfoFrame_on_info_frame_mode)
menu.infoFrame={id=42}
projectionChanged()
assert(menu.refresh==nil)
menu.mode='tm_empire_status'
projectionChanged()
assert(menu.refresh==100.1)
menu.mode='empire'
local config={leftBar={{mode='empire'},{mode='stats'},{spacing=true},{mode='personnel'}}}
callbacks.createPlayerInfo_on_start(config)
callbacks.createPlayerInfo_on_start(config)
assert(#config.leftBar==5 and config.leftBar[1].mode=='empire'
    and config.leftBar[2].mode=='tm_empire_status' and config.leftBar[3].mode=='stats'
    and config.leftBar[4].spacing and config.leftBar[5].mode=='personnel')
assert(not config.leftBar[2].condition())
projection={schema=1,has_governor=0,active=0}
assert(api.snapshot() and not api.snapshot().has_governor)
projection={schema=1,has_governor=2,active=0}
assert(api.snapshot()==nil)
projection={schema=1, has_governor=true, active=true, governor_name='fixture real-person reference',
    station_name='station',module_name='module',reason='reason',updated=100,
    rows={{name='ship',state='unknown',reason='await read-back'}}}
assert(config.leftBar[2].condition())
local rendered={}
local restoredTop, restoredSelected
menu.playerInfoFullWidth=1150
menu.sideBarWidth=34
Helper.borderSize=1
local frame={addTable=function(_,count,properties)
    assert(count==3)
    -- The added mode must use the native empire page's available width,
    -- rather than the narrow default passed to third-party callbacks.
    assert(properties.width==1115 and properties.x==70 and properties.y==100)
    assert(properties.height==nil and properties.maxVisibleHeight==700)
    assert(properties.x + properties.width <= 1280)
    return {setColWidth=function() end, setTopRow=function(_,value) restoredTop=value end, setSelectedRow=function(_,value) restoredSelected=value end, addRow=function(_, rowdata)
        assert(rowdata == true) -- Nonselectable report rows exceed the native minimum height.
        local row={}
        for i=1,3 do row[i]={createText=function(_,str) rendered[#rendered+1]=str end} end
        return row
    end}
end}
callbacks.createInfoFrame_on_info_frame_mode(frame,{width=1000,x=70,y=100,height=700})
assert(#rendered==0) -- Стандартная страница остаётся в ведении игры.
menu.mode='tm_empire_status'
menu.settoprow=27
menu.setselectedrow=29
callbacks.createInfoFrame_on_info_frame_mode(frame,{width=1000,x=70,y=100,height=700})
assert(restoredTop==27 and restoredSelected==29)
assert(menu.settoprow==nil and menu.setselectedrow==nil)
assert(#rendered==15 and rendered[14]=='Исход неизвестен')
projection.tasks={{name='Перевод сотрудника',state='sent',reason='Ожидается прибытие',issued=99},
    {name='Снабжение корабля',state='quote_requested',reason='Запрос цены',issued=100}}
local snapshot=api.snapshot()
assert(snapshot.tasks[1].issued==99 and snapshot.tasks[2].state=='quote_requested')
rendered={}; callbacks.createInfoFrame_on_info_frame_mode(frame,{width=1000,x=70,y=100,height=700})
assert(rendered[19]=='Перевод сотрудника' and rendered[20]=='Отправлено'
    and rendered[23]=='Запрос цены')
projection.tasks[3]={name='Обучение сотрудника',state='unknown',
    reason='seminar_consumption_or_skill_unconfirmed',issued=100}
rendered={}; callbacks.createInfoFrame_on_info_frame_mode(frame,{width=1000,x=70,y=100,height=700})
assert(rendered[25]=='Обучение сотрудника' and rendered[26]=='Исход неизвестен'
    and rendered[27]=='Расход семинара или изменение навыка не подтверждены')
projection.tasks[4]={name='Персонал: Станция',state='waiting',
    reason='required_seminar_missing',issued=100}
rendered={}; callbacks.createInfoFrame_on_info_frame_mode(frame,{width=1000,x=70,y=100,height=700})
assert(rendered[28]=='Персонал: Станция' and rendered[29]=='Ожидание'
    and rendered[30]=='Для необходимого обучения нет подходящего семинара')
projection.tasks[1].issued=101; assert(not api.snapshot())
projection.tasks[1].issued=0/0; assert(not api.snapshot())
projection.tasks[1].issued=99; projection.tasks[1].reason=string.rep('x',1025)
assert(api.snapshot()) -- Native military explanations exceed 1024 UTF-8 bytes.
projection.tasks[1].reason=string.rep('Оборона; ',150)
assert(#projection.tasks[1].reason > 1024 and api.snapshot())
rendered={}
callbacks.createInfoFrame_on_info_frame_mode(frame,{width=1000,x=70,y=100,height=700})
local longReasonRendered=false
for _,value in ipairs(rendered) do
    if value==projection.tasks[1].reason then longReasonRendered=true end
end
assert(longReasonRendered) -- Preserve the full explanation in the actual renderer.
projection.tasks[1].reason=string.rep('x',4097)
assert(not api.snapshot())
projection.tasks=nil

-- Current station status replaces the retired rating/history contract.
local api
local projection={schema=1,has_governor=true,active=true,governor_name='Governor',station_name='HQ',module_name='Module',reason='Active',updated=100,rows={}}
local menu={registerCallback=function() end}
package.preload.ffi=function() return {cdef=function() end,C={GetPlayerID=function() return 7 end}} end
Helper={getMenu=function() return menu end}
RegisterEvent=function() end
Register_Require_With_Init=function(_,module,init) api=module;init() end
GetNPCBlackboard=function() return projection end
DebugError=function(message) error(message) end
ConvertStringToLuaID=function(value) return tonumber(value) end
projection.observations={{station='Factory',employee='Manager',state='unknown',workstate='needs_attention',reason='Resources missing',observed=95,
 production={total=1,complete=true,producing=0,resources=1,storage=0,manual=0,paused=0,other=0},
 trade_restricted=false,money=80,productionmoney=100,provision='insufficient_provision',provisionreason='Low budget',recommendation='Fund production',
 problems={{category='Production resources',ware='Energy Cells'}},problems_complete=true}}
assert(loadfile('X4_TopManager/ui/empire_status.lua'))()
local value=assert(api.snapshot()).observations[1]
assert(value.workstate=='needs_attention' and value.production.resources==1 and value.money==80)
assert(value.assessment==nil and value.previous_periods==nil and value.from==nil)
projection.observations[1].assessment={reason='Old rating'}
projection.observations[1].previous_periods={{employee='Old Manager'}}
value=assert(api.snapshot()).observations[1]
assert(value.assessment==nil and value.previous_periods==nil)
projection.observations[1].workstate='manager_decision'
assert(api.snapshot()==nil)
projection.observations[1].workstate='working'
projection.observations[1].production.producing=1
assert(api.snapshot()==nil) -- Mutually exclusive native flags must sum to total.
projection.observations[1].production.resources=0
assert(api.snapshot().observations[1].workstate=='working')
projection.observations[1].tradereason='Штатный Upkeep: нет торгового подчинённого'
assert(api.snapshot()==nil) -- An incomplete need must not become a valid report.
projection.observations[1].traderecommendation='Назначить торговый корабль'
value=assert(api.snapshot()).observations[1]
assert(value.tradereason==projection.observations[1].tradereason
    and value.traderecommendation==projection.observations[1].traderecommendation)
projection.observations[1].observed=101
assert(api.snapshot()==nil)
print('PASS current station state/needs without history; stale ratings ignored; invalid/current-time bounds rejected')
