#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
import glob
import traceback
import re

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
from PYmodsCore import PYmodsConfigInterface, loadJson, remDups
#Repair
from gui import InputHandler
from gui.battle_control.battle_constants import DEVICE_STATE_DESTROYED, VEHICLE_VIEW_STATE, DEVICE_STATE_NORMAL
from gui.shared.gui_items import Vehicle
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.shared import g_eventBus, events, EVENT_BUS_SCOPE

__name__ = 'IVM '
__author__ = 'The Illusion '
__copyright__ = 'Copyright 2020, The Illusion'
__credits__ = ['The Illusion', 'RaJCel']
__maintainer__ = 'The Illusion'
__status__ = 'Dev'
__version__ = '0.2'
_DIR_ = './mods/configs/IVM'
_FILE_ = './mods/configs/IVM/IVM.json'

print '[IVM] ' + str(__name__) + 'By ' + str(__maintainer__) + ' Version ' + str(__status__), str(__version__)

class ConfigInterface(PYmodsConfigInterface):

    def __init__(self):
        self.textStack = {}
        self.wasReplaced = {}
        self.textId = {}
        self.configsList = []
        self.confMeta = {}
        self.sectDict = {}
        self.settings = {}
        self.enabled = True
        self.carEnabled = False
        self.carRows = 1
        self.questHintEnabled = True
        self.stun = False
        self.stunEvent = 'battle_event_stun'
        self.fire = False
        self.fireEvent = 'battle_event_fire'
        self.fixEffects = False
        self.emptyShellsEnabled = False
        self.emptyShellsEvent = 'IVM_emptyShellsEvent'
        self.almostOutEvent = 'IVM_almostOutEvent'
        self.TESTER = True
        self.fixVehicleTransparency = False
        self.repairEnabled = False
        super(ConfigInterface, self).__init__()

    def init(self):
        self.ID = 'IVM'
        self.version = '0.2 (13/04/2020)'
        self.author = '(The Illusion)'
        self.buttons = {
            'buttonRepair' : [Keys.KEY_SPACE],
            'buttonChassis': [[Keys.KEY_LALT, Keys.KEY_RALT]]
        }
        self.data = {
            'enabled': True,
            'carEnabled': False,
            'carRows': 1,
            'questHintEnabled': True,
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
            'buttonChassis' : self.buttons['buttonChassis'],
            'buttonRepair'  : self.buttons['buttonRepair'],
            'removeStun'    : True,
            'extinguishFire': True,
            'healCrew': True,
            'repairDevices': True,
            'restoreChassis': False,
            'useGoldKits'   : True,
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
        }
        self.i18n = {
            'name': 'Improved Visuals and Sounds',
            'UI_setting_carEnabled_text': 'Enable Carousel Module, you will need to reload to see the effect.',
            'UI_setting_carRows_text': 'Number of rows you want',
            'UI_setting_questHintEnabled_text': 'Turn this off if you dont want the mission hint at the start of battle',
            'UI_setting_stunEnabled_text': 'Enable for a Voice Over when you are stunned',
            'UI_setting_stunEnabled_tooltip': 'This can be altered in the config, requires WWISE',
            'UI_setting_fireEnabled_text': 'Enable for a Voice Over when you are on fire',
            'UI_setting_fireEnabled_tooltip': 'This can be altered in the config, requires WWISE',
            'UI_setting_fixEffects_text': 'Disable Effects List Spam',
            'UI_setting_fixEffects_tooltip': 'This is mostly for the python.log',
            'UI_setting_fixVehicleTransparency_text': 'Fix Vehicle Model Transparency',
            'UI_setting_NDA_text': ' \xe2\x80\xa2 No data available or provided.',
            'UI_setting_emptyShellsEnabled_text': 'Enable No Shell Sound and 5 shell warning',
            'UI_setting_emptyShellsEnabled_tooltip': 'This can be altered in the config, requires WWISE',
            'UI_setting_TESTER_text': 'Tester',
            'UI_setting_TESTER_tooltip': 'Enable this if you want to test new features',
            'UI_setting_UI_changes_text': 'UI Changes',
            'UI_setting_Sounds_text': 'Sounds',
            'UI_setting_Fixes_text': 'Fixes',
            'UI_setting_Carousel_Options_text': 'Carousel Options',
            'UI_setting_Repair_text': 'Repair Options',
            'UI_setting_repairEnabled_text': 'Enable',
            'UI_setting_buttonChassis_text'   : 'Button: Restore Tracks and Wheels',
            'UI_setting_buttonChassis_tooltip': '',
            'UI_setting_buttonRepair_text'    : 'Button: Smart Repair',
            'UI_setting_buttonRepair_tooltip' : '',
            'UI_setting_removeStun_text'      : 'Remove Stun',
            'UI_setting_removeStun_tooltip'   : '',
            'UI_setting_useGoldKits_text'     : 'Use Premium Kits',
            'UI_setting_useGoldKits_tooltip'  : '',
            'UI_setting_extinguishFire_text'   : 'Extinguish Fire',
            'UI_setting_extinguishFire_tooltip': '',
            'UI_setting_healCrew_text'   : 'Heal Cew',
            'UI_setting_healCrew_tooltip': '',
            'UI_setting_restoreChassis_text'   : 'Restore Tracks and Wheels',
            'UI_setting_restoreChassis_tooltip': '',
            'UI_setting_repairDevices_text'   : 'Repair Devices',
            'UI_setting_repairDevices_tooltip': ''
        }
        super(ConfigInterface, self).init()
    
    def onApplySettings(self, settings):
        super(ConfigInterface, self).onApplySettings(settings)
        self.carEnabled = self.data['enabled'] and self.carEnabled
        self.carRows = self.data['carRows'] and self.carRows
        self.questHintEnabled = self.data['questHintEnabled'] and self.questHintEnabled
        self.stun = self.data['stunEnabled'] and self.stun
        self.fire = self.data['fireEnabled'] and self.fire
        self.emptyShellsEnabled = self.data['emptyShellsEnabled'] and self.emptyShellsEnabled
        self.almostOutEvent = self.data['almostOutEvent'] and self.almostOutEvent
        self.fixEffects = self.data['fixEffects'] and self.fixEffects
        self.fixVehicleTransparency = self.data['fixVehicleTransparency'] and self.fixVehicleTransparency
        self.TESTER = self.data['TESTER'] and self.TESTER

    def loadLang(self):
        pass

    def createTemplate(self):
        """
        createTooltip
        createLabel
        createControl
        createOptions
        createHotKey
        _createNumeric
        createStepper
        createSlider
        createRangeSlider
        """
        return {'modDisplayName': self.i18n['name'],
         'enabled': self.data['enabled'],
         'column1': [self.tb.createControl('TESTER') ,self.tb.createLabel('UI_changes') ,self.tb.createControl('questHintEnabled'), self.tb.createLabel('Sounds'), self.tb.createControl('stunEnabled'), self.tb.createControl('fireEnabled'), self.tb.createControl('emptyShellsEnabled') ,self.tb.createLabel('Fixes'), self.tb.createControl('fixEffects'), self.tb.createControl('fixVehicleTransparency')],
         'column2': [self.tb.createLabel('Carousel_Options'), self.tb.createControl('carEnabled'), self.tb.createStepper('carRows', 1.0, 12.0, 1.0, True), self.tb.createLabel('Repair'), self.tb.createControl('repairEnabled'), self.tb.createHotKey('buttonChassis'),self.tb.createHotKey('buttonRepair'), self.tb.createControl('useGoldKits'), self.tb.createControl('removeStun'), self.tb.createControl('healCrew'), self.tb.createControl('repairDevices'), self.tb.createControl('restoreChassis'), self.tb.createControl('extinguishFire')]}

    def readCurrentSettings(self, quiet=True):
        super(ConfigInterface, self).readCurrentSettings(quiet)
        self.settings = loadJson(self.ID, 'settings', self.settings, self.configPath)
        loadJson(self.ID, 'settings', self.settings, self.configPath, True, quiet=quiet)
        self.updateMod()

config = ConfigInterface()

"""
IVM Carousel Handler
"""

if config.data['carEnabled'] == True:
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS
    tankrows = config.data['carRows']
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

    print '[IVM] Tank Carousels Loaded with ' + str(config.data['carRows']) + ' rows'
else:
    print '[IVM] Tank Carousels Not Enabled'
    pass

"""
IVM Battle Hints Handler
"""
#Mission Hint Panel
if config.data['questHintEnabled'] == False:
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

if config.data['stunEnabled'] == True:
    #assign old event
    old_DestroyTimersPanel__showStunTimer = DestroyTimersPanel._DestroyTimersPanel__showStunTimer
    #define new event
    def illusion_stunSound_DestroyTimersPanel__showStunTimer(self, value):
        #call old event
        old_DestroyTimersPanel__showStunTimer(self, value)
        try:
            if value.duration > 0.0:
                #play sound at event 'battle_event_stun'
                SoundGroups_g_instance.playSound2D(config.data['stunEvent'])
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
if config.data['fireEnabled'] == True:
    #assign old event
    old_DestroyTimersPanel__setFireInVehicle = DestroyTimersPanel._DestroyTimersPanel__setFireInVehicle

    def IVM_new__setFireInVehicle(self, isInFire):
        old_DestroyTimersPanel__setFireInVehicle(self, isInFire)
        try:
            if isInFire:
                #play sound at event 'battle_event_fire'
                SoundGroups_g_instance.playSound2D(config.data['fireEvent'])
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
if config.data['emptyShellsEnabled'] == True and config.TESTER == True:
    from helpers.CallbackDelayer import CallbackDelayer
    class IVM_SoundEvent(CallbackDelayer):
        def __init__(self, effectDesc):
            CallbackDelayer.__init__(self)
            self._desc = effectDesc
            self.sound = None
            return

        def __del__(self):
            if self._sound is not None:
                self._sound.stop()
                self._sound = None
            CallbackDelayer.destroy(self)
            return

        def start(self, shellCount, lastShell, reloadStart, shellReloadTime):
            if reloadStart:
                if shellCount == 0:
                    SoundGroups_g_instance.playSound2D(config.data['emptyShellEvent'])
                    print '[IVM] Player out of ammo!'
                elif shellCount == 5:
                    SoundGroups_g_instance.playSound2D(config.data['almostOutEvent'])
                    print '[IVM] Player is almost out of ammo!'
                else:
                    pass
                time = shellReloadTime - self._desc.duration
                self.delayCallback(time, shellCount, BigWorld.time() + time)
                return

        def stop(self):
            if self._sound is not None:
                self._sound.stop()
                self._sound = None
            return

else:
    pass            
"""
IVM Fixes
"""
# Effects List Spam Fix
if config.data['fixEffects'] == True:
    from helpers import EffectsList
    EffectsList.LOG_WARNING = lambda *_, **__: None
    print 'Effects List Spam Fix by ' + str(__name__), str(__version__) + ' done.'
else:
    pass

# Vehicle Model Transparency Fix
if config.data['fixVehicleTransparency'] == True:
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
        self.checkBattleStarted()

    def stopBattle(self):
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
        if not config.data['repairEnabled']: return
        if BattleReplay.g_replayCtrl.isPlaying: return
        if self.ctrl is None:
            return
        equipment = self.ctrl.equipments.getEquipment(self.items[equipmentTag][0]) if self.ctrl.equipments.hasEquipment(self.items[equipmentTag][0]) else None
        if equipment is not None and equipment.isReady and equipment.isAvailableToUse:
            self.consumablesPanel._ConsumablesPanel__handleEquipmentPressed(self.items[equipmentTag][0], item)
            sound = SoundGroups.g_instance.getSound2D('vo_flt_repair')
            BigWorld.callback(1.0, sound.play)

    def useItemGold(self, equipmentTag):
        if not config.data['repairEnabled']: return
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
            elif config.data['useGoldKits'] and self.items[equipmentTag][3]:
                self.useItemGold(equipmentTag)

    def repair(self, equipmentTag):
        specific = config.data['repairPriority'][Vehicle.getVehicleClassTag(BigWorld.player().vehicleTypeDescriptor.type.tags)][equipmentTag]
        if config.data['useGoldKits'] and self.items[equipmentTag][3]:
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
        if config.data['extinguishFire']:
            self.extinguishFire()
        if config.data['repairDevices']:
            self.repair('repairkit')
        if config.data['healCrew']:
            self.repair('medkit')
        if config.data['removeStun']:
            self.removeStun()
        if config.data['restoreChassis']:
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