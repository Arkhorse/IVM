#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
import glob
import traceback
import re
from math import fabs
import inspect
from functools import partial, update_wrapper
import sys
#Game Imports
import BigWorld
import BattleReplay
import Keys
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta
#Hints Panel
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin
#Sounds
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel
from SoundGroups import g_instance as SoundGroups_g_instance
from gui import SystemMessages
from Account import PlayerAccount
#Repair
from gui import InputHandler
from gui.battle_control.battle_constants import DEVICE_STATE_DESTROYED, VEHICLE_VIEW_STATE, DEVICE_STATE_NORMAL
from gui.shared.gui_items import Vehicle
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.shared import g_eventBus, events, EVENT_BUS_SCOPE
#Ingame GUI
from gui.modsSettingsApi import g_modsSettingsApi
from gui.modsSettingsApi.skeleton import IModsSettingsApi

modLinkage = 'mod_ivm'

__name__ = 'IVM '
MOD_NAME = 'IVM'
__author__ = 'The Illusion '
__copyright__ = 'Copyright 2020, The Illusion'
__credits__ = ['The Illusion', 'RaJCel']
__maintainer__ = 'The Illusion'
__status__ = 'Dev'
__version__ = '0.2'
_DIR_ = './mods/configs/IVM'
_FILE_ = './mods/configs/IVM/IVM.json'

print '[IVM] ' + str(__name__) + 'By ' + str(__maintainer__) + ' Version ' + str(__status__), str(__version__)

class AbstractSettings(object):
    
    def __init__(self, name):
        self.__name = name
        self.__registerModSettings()

    def __registerModSettings(self):
        settingsTemplate = self.getSettingsTemplate()
        savedSettings = g_modsSettingsApi.getModSettings(self.__name, settingsTemplate)
        if savedSettings:
            settings = savedSettings
            g_modsSettingsApi.registerCallback(self.__name, self.__onModSettingsChanged)
        else:
            settings = g_modsSettingsApi.setModTemplate(self.__name, settingsTemplate, self.__onModSettingsChanged)
        self.__onModSettingsChanged(self.__name, settings, True)

    def __onModSettingsChanged(self, linkage, settings, isFirst=False):
        if linkage == self.__name:
            self.onSettingsUpdated(settings, isFirst)

    def onSettingsUpdated(self, settings, isFirst):
        pass

    def getSettingsTemplate(self):
        pass

class ConfigInterface(AbstractSettings):


    def __init__(self):
        self.ID = 'IVM'
        self.version = '0.2 (13/04/2020)'
        self.author = '(The Illusion)'
        self.defaultKeys = {
            'buttonRepair' : [Keys.KEY_SPACE],
            'buttonChassis': [[Keys.KEY_LALT, Keys.KEY_RALT]]
        }
        self.config = {'templates': {
                'modDisplayName': 'Improved Visuals and Sounds',
                'settingsVersion': 0.2,
                'enabled': True,
                'column1': [
                    {
                        'type': 'Label',
                        'text': 'In Battle Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Missions Hint UI',
                        'value': False,
                        'tooltip': '{BODY} Turn this off if you dont want the missions hint UI at the start of the battle {/ BODY}',
                        'varName': 'questHintEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'Sound Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Stun Sound',
                        'value': False,
                        'tooltip': '{HEADER} Turn this on if you want a Voice Over for when you are stunned. {/ HEADER} {BODY} This is the DeadPool one {/ BODY}',
                        'varName': 'stunEnabled'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Fire Sound',
                        'value': False,
                        'tooltip': '{HEADER} Turn this on if you want a Voice Over for when you are set on fire. {/ HEADER} {BODY} This is the DeadPool one. {/ BODY}',
                        'varName': 'fireEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'In Garage Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable Carousel Function',
                        'value': False,
                        'tooltip': '{BODY} Turn this on if you want to use the carousel stuff{/ BODY}',
                        'varName': 'carEnabled'
                    },
                    {
                        'type': 'Slider',
                        'text': 'The number of carousel rows you want',
                        'minimum': 1,
                        'maximum': 12,
                        'snapInterval': 1,
                        'value': 1,
                        'format': '{{{1}}}',
                        'varName': 'carRows'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable Garage Counters',
                        'value': True,
                        'varName': 'counterEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'Fixes, Ect'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Effects List Spam',
                        'tooltip': 'Removes the effects list spam from the python.log. This can cause this log to be very large. #WG',
                        'value': False,
                        'varName': 'fixEffects'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Vehicle Model Transparency',
                        'tooltip': 'Fixes a rare issue where the vehicle model isnt shown correctly',
                        'value': False,
                        'varName': 'fixVehicleTransparency'
                    },
                ],
                'column2': [
                    {
                        'type': 'Label',
                        'text': 'Repair Options'
                    },
                    {
                        'type': 'Label',
                        'text': 'Repair Options is legal. None of these options are automatic.'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable',
                        'value': False,
                        'varName': 'repairEnabled'
                    },
                    {
                        'type': 'HotKey',
                        'text': 'Repair Tracks and Wheels',
                        'value': [Keys.KEY_SPACE],
                        'varName': 'buttonChassis'
                    },
                    {
                        'type': 'HotKey',
                        'text': 'Smart Repair',
                        'value': [[Keys.KEY_LALT, Keys.KEY_RALT]],
                        'varName': 'buttonRepair'
                    },
                    {
                        'type': 'Label',
                        'text': 'Smart Repair Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Use Gold Kits',
                        'value': False,
                        'varName': 'useGoldKits'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Repair Tracks and Wheels',
                        'value': False,
                        'varName': 'restoreChassis'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Repair all Devices (Optics, Turret, Gun, Ect)',
                        'value': False,
                        'varName': 'repairDevices'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Heal Crew',
                        'value': False,
                        'varName': 'healCrew'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Extinguish Fires',
                        'value': False,
                        'varName': 'extinguishFire'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Remove Stun',
                        'value': False,
                        'varName': 'removeStun'
                    }]
                }, 'settings': {
                'enabled': True,
                'carEnabled': False,
                'carRows': 1,
                'questHintEnabled': True,
                'counterEnabled': True,
                'stunEnabled': False,
                'stunEvent': 'battle_event_stun',
                'fireEnabled': False,
                'fireEvent': 'battle_event_fire',
                'fixEffects': False,
                'fixVehicleTransparency': False,
                'emptyShellsEnabled': False,
                'emptyShellsEvent': 'IVM_emptyShellsEvent',
                'almostOutEvent': 'IVM_almostOutEvent',
                'TESTER': True,
                'repairEnabled': False,
                'buttonChassis' : self.defaultKeys['buttonChassis'],
                'buttonRepair'  : self.defaultKeys['buttonRepair'],
                'removeStun'    : True,
                'extinguishFire': True,
                'healCrew': True,
                'repairDevices': True,
                'restoreChassis': True,
                'useGoldKits'   : False,
                'repairPriority': {
                    'lightTank'            : {
                        'medkit'   : ['commander', 'driver', 'gunner', 'loader'],
                        'repairkit': ['ammoBay', 'engine', 'gun', 'turretRotator', 'fuelTank']
                    },
                    'mediumTank'           : {
                        'medkit'   : ['commander', 'loader', 'driver', 'gunner'],
                        'repairkit': ['ammoBay', 'turretRotator', 'engine', 'gun', 'fuelTank']
                    },
                    'heavyTank'            : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'turretRotator', 'engine', 'fuelTank']
                    },
                    'SPG'                  : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'engine', 'turretRotator', 'fuelTank']
                    },
                    'AT-SPG'               : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'engine', 'turretRotator', 'fuelTank']
                    },
                    'AllAvailableVariables': {
                        'medkit'   : ['commander', 'gunner', 'driver', 'radioman', 'loader'],
                        'repairkit': ['engine', 'ammoBay', 'gun', 'turretRotator', 'chassis', 'surveyingDevice', 'radio', 'fuelTank', 'wheel']
                    }
                }
            }}
        AbstractSettings.__init__(self, MOD_NAME)

    #def getSettingsTemplate(self):
        #return self.config['templates']
    
    def onSettingsUpdated(self, settings, isFirst=False):
        self.settings = settings
        if not isFirst:
            settings = newSettings

config = ConfigInterface()

def ivm_createConfig():
        data = {}
        try:
            os.makedirs(_DIR_)
        except:
            LOG_CURRENT_EXCEPTION()
        with open(_FILE_, 'w') as json_file:
            jsonDump(config.config['settings'], json_file, separators=(',', ': '), indent=4, sort_keys=False)
            json_file.write('\n')
            print '[IVM] Config Not Found, New Config Generated'

def ivm_checkConfig():
        if path.exists(_FILE_):
            with open(_FILE_, 'r+') as f:
                data = jsonLoad(f)
                enabled = config.config['settings']['enabled']
                carEnabled = config.config['settings']['carEnabled']
                carRows = config.config['settings']['carRows']
                counterEnabled = config.config['settings']['counterEnabled']
                questHintEnabled = config.config['settings']['questHintEnabled']
                stunEnabled = config.config['settings']['stunEnabled']
                stunEvent = config.config['settings']['stunEvent']
                fireEnabled = config.config['settings']['fireEnabled']
                fireEvent = config.config['settings']['fireEvent']
                fixEffects = config.config['settings']['fixEffects']
                emptyShellsEnabled = config.config['settings']['emptyShellsEnabled']
                emptyShellsEvent = config.config['settings']['emptyShellsEvent']
                almostOutEvent = config.config['settings']['almostOutEvent']
                fixVehicleTransparency = config.config['settings']['fixVehicleTransparency']
                repairEnabled = config.config['settings']['repairEnabled']
                removeStun = config.config['settings']['removeStun']
                extinguishFire = config.config['settings']['extinguishFire']
                repairPriority = config.config['settings']['repairPriority']
                healCrew = config.config['settings']['healCrew']
                repairDevices = config.config['settings']['repairDevices']
                restoreChassis = config.config['settings']['restoreChassis']
                useGoldKits = config.config['settings']['useGoldKits']
                repairPriority = config.config['settings']['repairPriority']
                print '[IVM] Config Found'
        else:
            LOG_CURRENT_EXCEPTION()
            print '[IVM] Config not found'
            ivm_createConfig()
            pass

ivm_checkConfig()

enabled = config.config['settings']['enabled']
carEnabled = config.config['settings']['carEnabled']
carRows = config.config['settings']['carRows']
counterEnabled = config.config['settings']['counterEnabled']
questHintEnabled = config.config['settings']['questHintEnabled']
stunEnabled = config.config['settings']['stunEnabled']
stunEvent = config.config['settings']['stunEvent']
fireEnabled = config.config['settings']['fireEnabled']
fireEvent = config.config['settings']['fireEvent']
fixEffects = config.config['settings']['fixEffects']
emptyShellsEnabled = config.config['settings']['emptyShellsEnabled']
emptyShellsEvent = config.config['settings']['emptyShellsEvent']
almostOutEvent = config.config['settings']['almostOutEvent']
fixVehicleTransparency = config.config['settings']['fixVehicleTransparency']
repairEnabled = config.config['settings']['repairEnabled']
removeStun = config.config['settings']['removeStun']
extinguishFire = config.config['settings']['extinguishFire']
repairPriority = config.config['settings']['repairPriority']
healCrew = config.config['settings']['healCrew']
repairDevices = config.config['settings']['repairDevices']
restoreChassis = config.config['settings']['restoreChassis']
useGoldKits = config.config['settings']['useGoldKits']
repairPriority = config.config['settings']['repairPriority']

#@overrideMethod
def overrideMethod(obj, prop, getter=None, setter=None, deleter=None):
    """
    :param obj: object, which attribute needs overriding
    :param prop: attribute name (can be not mangled), attribute must be callable
    :param getter: fget function or None
    :param setter: fset function or None
    :param deleter: fdel function or None
    :return function: unmodified getter or, if getter is None and src is not property, decorator"""

    if inspect.isclass(obj) and prop.startswith('__') and prop not in dir(obj) + dir(type(obj)):
        prop = obj.__name__ + prop
        if not prop.startswith('_'):
            prop = '_' + prop
    src = getattr(obj, prop)
    if type(src) is property and (getter or setter or deleter):
        props = []
        for func, fType in ((getter, 'fget'), (setter, 'fset'), (deleter, 'fdel')):
            assert func is None or callable(func), fType + ' is not callable!'
            props.append(partial(func, getattr(src, fType)) if func else getattr(src, fType))
        setattr(obj, prop, property(*props))
        return getter
    elif getter:
        getter_orig = getter
        assert callable(src), 'Source property is not callable!'
        assert callable(getter_orig), 'Handler is not callable!'
        while isinstance(getter, partial):
            getter = getter.func

        def getter_new(*a, **k):  # noinspection PyUnusedLocal
            info = None
            try:
                return getter_orig(src, *a, **k)
            except Exception:  # Code to remove this wrapper from traceback
                info = sys.exc_info()
                new_tb = info[2].tb_next  # https://stackoverflow.com/q/44813333
                if new_tb is None:  # exception occurs inside this wrapper, not inside of getter_orig
                    new_tb = _generate_new_tb(getter.func_code)
                raise info[0], info[1], new_tb
            finally:
                del info

        try:
            update_wrapper(getter_new, getter)
        except AttributeError:
            pass
        if inspect.isclass(obj):
            if inspect.isfunction(src):
                getter_new = staticmethod(getter_new)
            elif getattr(src, '__self__', None) is not None:
                getter_new = classmethod(getter_new)
        setattr(obj, prop, getter_new)
        return getter_orig
    else:
        return partial(overrideMethod, obj, prop)

"""
IVM Carousel Handler
"""

if carEnabled == True:
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS
    tankrows = carRows
    def new_as_rowCountS(self, value):
        old_as_rowsCountS(self, value)
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(tankrows)
    
    TankCarouselMeta.as_rowCountS = new_as_rowCountS
    from gui.Scaleform.daapi.view.common.vehicle_carousel import carousel_environment
    def updateVehicles(self, vehicles=None, filterCriteria=None):
        self.new_as_rowCountS()
        self._carouselDP.updateVehicles(vehicles, filterCriteria)
        self.applyFilter()

    print '[IVM] Tank Carousels Loaded with ' + str(carRows) + ' rows'
else:
    print '[IVM] Tank Carousels Not Enabled'
    pass

"""
IVM Garage Counters
"""
if counterEnabled == True:
    from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
    @overrideMethod(LobbyHeader, '_LobbyHeader__setCounter')
    def ivm_setCounter(base, self, alias, counter=None):
        base(self, alias, counter)

"""
IVM Battle Hints Handler
"""
#Mission Hint Panel
if questHintEnabled == False:
    old_quest_Hint = PreBattleHintPlugin._PreBattleHintPlugin__canDisplayQuestHint
    def ivm_questHint(self):
        old_quest_Hint(self)
        return None
    PreBattleHintPlugin._PreBattleHintPlugin__canDisplayQuestHint = ivm_questHint
    print '[IVM][LOAD] Missions Hint Panel Disabled'
else:
    print '[IVM] Missions Hint Panel Enabled'
    pass

"""
IVM Stun Sound Handler
"""

if stunEnabled == True:
    #assign old event
    old_DestroyTimersPanel__showStunTimer = DestroyTimersPanel._DestroyTimersPanel__showStunTimer
    #define new event
    def illusion_stunSound_DestroyTimersPanel__showStunTimer(self, value):
        #call old event
        old_DestroyTimersPanel__showStunTimer(self, value)
        try:
            if value.duration > 0.0:
                #play sound at event 'battle_event_stun'
                SoundGroups_g_instance.playSound2D(stunEvent)
        except:
            #if that doesnt work, log the error
            print '[ERROR][IVM] Stun Sound Not Played'
            LOG_CURRENT_EXCEPTION()
    #replace old event with new one
    DestroyTimersPanel._DestroyTimersPanel__showStunTimer = illusion_stunSound_DestroyTimersPanel__showStunTimer

    print '[IVM][LOAD] IVM Stun Sound Loaded'
else:
    print '[IVM] Stun Sound Not Loaded'
    pass

"""
IVM fire sound handler
"""
if fireEnabled == True:
    #assign old event
    old_DestroyTimersPanel__setFireInVehicle = DestroyTimersPanel._DestroyTimersPanel__setFireInVehicle

    def IVM_new__setFireInVehicle(self, isInFire):
        old_DestroyTimersPanel__setFireInVehicle(self, isInFire)
        try:
            if isInFire:
                #play sound at event 'battle_event_fire'
                SoundGroups_g_instance.playSound2D(fireEvent)
            else:
                self._hideTimer(_TIMER_STATES.FIRE)
            return
        except:
            #if that doesnt work, log the exception
            print('Failed to play fire sound')
            LOG_CURRENT_EXCEPTION()
    #replace old event with new
    DestroyTimersPanel._DestroyTimersPanel__setFireInVehicle = IVM_new__setFireInVehicle

    print '[IVM][LOAD] IVM Fire Sound Loaded'
else:
    print '[IVM] Fire Sound Not Loaded'
    pass

"""
IVM Empty Shells
"""
if emptyShellsEnabled == True:
    #Debug
        from gui.battle_control.controllers.consumables import ammo_ctrl
        old_getShells = ammo_ctrl.AmmoController_getShells
            #def getShells(self, intCD):
                #try:
                    #quantity, quantityInClip = self.__ammo[intCD]
                #except KeyError:
                    #LOG_ERROR('Shell is not found.', intCD)
                    #quantity, quantityInClip = (SHELL_QUANTITY_UNKNOWN,) * 2

        def ivm_getShells(self, intCD):
            old_getShells(self, intCD)
            try:
                quantity, quantitInClip = self.__ammo[intCD]
                if quantity == 0 or quantitInClip == 0:
                    SoundGroups_g_instance.playSound2D(emptyShellsEvent)
                if quantity == 5 or quantitInClip == 5:
                    SoundGroups_g_instance.playSound2D(almostOutEvent)
            except KeyError :
                LOG_ERROR('Shell is not found.', intCD)
                quantity, quantityInClip = (SHELL_QUANTITY_UNKNOWN,) * 2

        ammo_ctrl.AmmoController_getShells = ivm_getShells
else:
    pass            
"""
IVM Fixes
"""
# Effects List Spam Fix
if fixEffects == True:
    from helpers import EffectsList
    EffectsList.LOG_WARNING = lambda *_, **__: None
    print 'Effects List Spam Fix by ' + str(__name__), str(__version__) + ' done.'
else:
    pass

# Vehicle Model Transparency Fix
if fixVehicleTransparency == True:
    from vehicle_systems.components.highlighter import Highlighter
    def IVM_doHighlight(self, status, args):
        if self._Highlighter__isPlayersVehicle:
            status &= ~self.HIGHLIGHT_SIMPLE & ~self.HIGHLIGHT_ON
        old_doHighlight(self, status, args)
    old_doHighlight = Highlighter._Highlighter__doHighlightOperation
    Highlighter._Highlighter__doHighlightOperation = IVM_doHighlight
    print 'Vehicle Model Transparency Fix by ' + str(__name__), str(__version__) + ' done.'
else:
    pass

"""
IVM Repair
"""

COMPLEX_ITEM = {
    'leftTrack' : 'chassis',
    'rightTrack': 'chassis',
    'gunner1'   : 'gunner',
    'gunner2'   : 'gunner',
    'radioman1' : 'radioman',
    'radioman2' : 'radioman',
    'loader1'   : 'loader',
    'loader2'   : 'loader',
    'wheel0': 'wheel',
    'wheel1': 'wheel',
    'wheel2': 'wheel',
    'wheel3': 'wheel',
    'wheel4': 'wheel',
    'wheel5': 'wheel',
    'wheel6': 'wheel',
    'wheel7': 'wheel'
}

CHASSIS = ['chassis', 'leftTrack', 'rightTrack', 'wheel', 'wheel0', 'wheel1', 'wheel2', 'wheel3', 'wheel4', 'wheel5', 'wheel6', 'wheel7']

class IVM_Repair(object):
    def __init__(self):
        self.ctrl = None
        self.consumablesPanel = None
        self.items = {
            'extinguisher': [251, 251, None, None],
            'medkit'      : [763, 1019, None, None],
            'repairkit'   : [1275, 1531, None, None]
        }
        g_eventBus.addListener(events.ComponentEvent.COMPONENT_REGISTERED, self.__onComponentRegistered, EVENT_BUS_SCOPE.GLOBAL)
        g_eventBus.addListener(events.ComponentEvent.COMPONENT_UNREGISTERED, self.__onComponentUnregistered, EVENT_BUS_SCOPE.GLOBAL)

    def startBattle(self):
        self.ctrl = BigWorld.player().guiSessionProvider.shared
        InputHandler.g_instance.onKeyDown += self.injectButton
        InputHandler.g_instance.onKeyUp += self.injectButton
        self.checkBattleStarted()

    def stopBattle(self):
        InputHandler.g_instance.onKeyDown -= self.injectButton
        InputHandler.g_instance.onKeyUp -= self.injectButton
        for equipmentTag in self.items:
            self.items[equipmentTag][2] = None
            self.items[equipmentTag][3] = None
        self.items['repairkit'][1] = 1531

    def checkBattleStarted(self):
        if hasattr(BigWorld.player(), 'arena') and BigWorld.player().arena.period is 3:
            for equipmentTag in self.items:
                self.items[equipmentTag][2] = self.ctrl.equipments.getEquipment(self.items[equipmentTag][0]) if self.ctrl.equipments.hasEquipment(self.items[equipmentTag][0]) else None
                self.items[equipmentTag][3] = self.ctrl.equipments.getEquipment(self.items[equipmentTag][1]) if self.ctrl.equipments.hasEquipment(self.items[equipmentTag][1]) else None
            equipmentTag = 'repairkit'
            if self.ctrl.equipments.hasEquipment(46331):
                self.items[equipmentTag][1] = 46331
                self.items[equipmentTag][3] = self.ctrl.equipments.getEquipment(self.items[equipmentTag][1]) if self.ctrl.equipments.hasEquipment(self.items[equipmentTag][1]) else None
        else:
            BigWorld.callback(0.1, self.checkBattleStarted)

    def useItem(self, equipmentTag, item=None):
        if not repairEnabled: return
        if BattleReplay.g_replayCtrl.isPlaying: return
        if self.ctrl is None:
            return
        equipment = self.ctrl.equipments.getEquipment(self.items[equipmentTag][0]) if self.ctrl.equipments.hasEquipment(self.items[equipmentTag][0]) else None
        if equipment is not None and equipment.isReady and equipment.isAvailableToUse:
            self.consumablesPanel._ConsumablesPanel__handleEquipmentPressed(self.items[equipmentTag][0], item)
            sound = SoundGroups.g_instance.getSound2D('vo_flt_repair')
            BigWorld.callback(1.0, sound.play)

    def useItemGold(self, equipmentTag):
        if not repairEnabled: return
        if BattleReplay.g_replayCtrl.isPlaying: return
        if self.ctrl is None:
            return
        equipment = self.ctrl.equipments.getEquipment(self.items[equipmentTag][1]) if self.ctrl.equipments.hasEquipment(self.items[equipmentTag][1]) else None
        if equipment is not None and equipment.isReady and equipment.isAvailableToUse:
            self.consumablesPanel._ConsumablesPanel__handleEquipmentPressed(self.items[equipmentTag][1])
            sound = SoundGroups.g_instance.getSound2D('vo_flt_repair')
            BigWorld.callback(1.0, sound.play)

    def extinguishFire(self):
        if self.ctrl.vehicleState.getStateValue(VEHICLE_VIEW_STATE.FIRE):
            equipmentTag = 'extinguisher'
            if self.items[equipmentTag][2]:
                self.useItem(equipmentTag)

    def removeStun(self):
        if self.ctrl.vehicleState.getStateValue(VEHICLE_VIEW_STATE.STUN):
            equipmentTag = 'medkit'
            if self.items[equipmentTag][2]:
                self.useItem(equipmentTag)
            elif useGoldKits and self.items[equipmentTag][3]:
                self.useItemGold(equipmentTag)

    def repair(self, equipmentTag):
        specific = repairPriority[Vehicle.getVehicleClassTag(BigWorld.player().vehicleTypeDescriptor.type.tags)][equipmentTag]
        if useGoldKits and self.items[equipmentTag][3]:
            equipment = self.items[equipmentTag][3]
            if equipment is not None:
                devices = [name for name, state in equipment.getEntitiesIterator() if state and state != DEVICE_STATE_NORMAL]
                result = []
                for device in specific:
                    if device in COMPLEX_ITEM:
                        itemName = COMPLEX_ITEM[device]
                    else:
                        itemName = device
                    if itemName in devices:
                        result.append(device)
                if len(result) > 1:
                    self.useItemGold(equipmentTag)
                elif result:
                    self.useItem(equipmentTag, result[0])
        elif self.items[equipmentTag][2]:
            equipment = self.items[equipmentTag][2]
            if equipment is not None:
                devices = [name for name, state in equipment.getEntitiesIterator() if state and state != DEVICE_STATE_NORMAL]
                result = []
                for device in specific:
                    if device in COMPLEX_ITEM:
                        itemName = COMPLEX_ITEM[device]
                    else:
                        itemName = device
                    if itemName in devices:
                        result.append(device)
                if len(result) > 1:
                    self.useItemGold(equipmentTag)
                elif result:
                    self.useItem(equipmentTag, result[0])

    def repairAll(self):
        if self.ctrl is None:
            return
        if extinguishFire:
            self.extinguishFire()
        if repairDevices:
            self.repair('repairkit')
        if healCrew:
            self.repair('medkit')
        if removeStun:
            self.removeStun()
        if restoreChassis:
            self.repairChassis()

    def repairChassis(self):
        if self.ctrl is None:
            return
        equipmentTag = 'repairkit'
        for intCD, equipment in self.ctrl.equipments.iterEquipmentsByTag(equipmentTag):
            if equipment.isReady and equipment.isAvailableToUse:
                devices = [name for name, state in equipment.getEntitiesIterator() if state and state in DEVICE_STATE_DESTROYED]
                for name in devices:
                    if name in CHASSIS:
                        self.useItem(equipmentTag, name)
                        return

    def __onComponentRegistered(self, event):
        if event.alias == BATTLE_VIEW_ALIASES.CONSUMABLES_PANEL:
            self.consumablesPanel = event.componentPy
            self.startBattle()

    def __onComponentUnregistered(self, event):
        if event.alias == BATTLE_VIEW_ALIASES.CONSUMABLES_PANEL:
            self.stopBattle()
            
repair = IVM_Repair()
