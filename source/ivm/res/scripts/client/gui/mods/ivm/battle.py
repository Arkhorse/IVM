import BigWorld
# Disable Starting hint
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import TrajectoryViewHintPlugin, SiegeIndicatorHintPlugin, PreBattleHintPlugin
# Disable destroyed messages imports
from gui.Scaleform.daapi.view.battle.shared.messages.fading_messages import FadingMessages
from constants import ARENA_GUI_TYPE
from Vehicle import Vehicle
from gui.Scaleform.daapi.view.battle.shared.battle_timers import PreBattleTimer
from constants import VEHICLE_SETTING
from gui.Scaleform.daapi.view.lobby.techtree.techtree_dp import _TechTreeDataProvider
from gui.Scaleform.daapi.view.meta.ModuleInfoMeta import ModuleInfoMeta
from helpers import dependency
from skeletons.gui.shared import IItemsCache
import traceback
from xml.etree import ElementTree as ET

from .Core import overrideMethod, registerEvent, _getRanges, CORE
from PYmodsCore import PYmodsConfigInterface

class ivmBattle(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmBattle'
        self.version = CORE.Version
        self.modsGroups = 'IVM'
        self.currentFPS = CORE.MaxFPS
        self.data = {'enabled': True, 
        'questHintEnabled': True, 
        'notShowBattleMessage': True, 
        'enableAutoSpeed': True,
        'hideTrajectoryView': False,
        'hideSiegeIndicator': False,
        'hideHelpScreen': False
        }#, 'setMaxFPS': self.currentFPS}
        super(ivmBattle, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                # 'UI_setting_hideHelpScreen_text': '',
                # 'UI_setting_hideHelpScreen_tooltip': ''
                'name': 'Battle Options',
                'UI_setting_questHintEnabled_text': 'Disable Mission Popup.',
                'UI_setting_questHintEnabled_tooltip': 'This will disable the mission popup at the start of battle.',
                'UI_setting_notShowBattleMessage_text': 'Disable Destroyed Tanks Message.',
                'UI_setting_notShowBattleMessage_tooltip': 'This will disable the messages for destroyed tanks above the minimap.',
                'UI_setting_enableAutoSpeed_text': 'Start Battle In Speed Mode For Wheeled \"Tanks\".',
                'UI_setting_enableAutoSpeed_tooltip': 'Always start in the speed mode for wheeled tanks with this.',
                'UI_setting_hideTrajectoryView_text': 'Hide Arty Trajectory View',
                'UI_setting_hideTrajectoryView_tooltip': '',
                'UI_setting_hideSiegeIndicator_text': 'Hide Siegemode Indicator',
                'UI_setting_hideSiegeIndicator_tooltip': '',
                'UI_setting_hideHelpScreen_text': 'Hide Help Screen',
                'UI_setting_hideHelpScreen_tooltip': ''
                #'UI_setting_setMaxFPS_text': 'Max Framerate',
                #'UI_setting_setMaxFPS_tooltip': 'This will allow you to set your max framerate. This is something alot of people want. The default is 1000, or unlimited.'
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('questHintEnabled'), self.tb.createControl('notShowBattleMessage'), self.tb.createControl('hideTrajectoryView'), self.tb.createControl('hideSiegeIndicator'), self.tb.createControl('hideHelpScreen')],
            'column2': [self.tb.createControl('enableAutoSpeed')]#, self.tb.createControl('setMaxFPS', self.tb.types.TextInput, 80)]
        }

config = ivmBattle()
questHintEnabled = config.data['questHintEnabled']
notShowBattleMessage = config.data['notShowBattleMessage']
enableAutoSpeed = config.data['enableAutoSpeed']
hideTrajectoryView = config.data['hideTrajectoryView']
hideSiegeIndicator = config.data['hideSiegeIndicator']
hideHelpScreen = config.data['hideHelpScreen']
# setMaxFPS = config.data['setMaxFPS']

# https://gitlab.com/xvm/xvm/-/blob/master/src/xpm/xvm_battle/battle.py
@overrideMethod(TrajectoryViewHintPlugin, '_TrajectoryViewHintPlugin__addHint')
def addHint(base, self):
    if hideTrajectoryView:
        return
    base(self)

@overrideMethod(SiegeIndicatorHintPlugin, '_SiegeIndicatorHintPlugin__updateHint')
def updateHint(base, self):
    if hideSiegeIndicator:
        return
    base(self)

@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
def canDisplayQuestHint(base, self):
    if questHintEnabled:
        return False
    base(self)

@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayHelpHint')
def canDisplayHelpHint(base, self, typeDescriptor):
    if hideHelpScreen:
        return False
    base(self, typeDescriptor)


@overrideMethod(FadingMessages, 'showMessage')
def FadingMessages_showMessage(base, self, key, args=None, extra=None, postfix=''):
    if not notShowBattleMessage or CORE.FrontlineBattleType:
        return base(self, key, args=None, extra=None, postfix='')
    pass

isWheeledTech = False
@registerEvent(Vehicle, 'onEnterWorld')
def Vehicle_onEnterWorld(self, prereqs):
    if not enableAutoSpeed:
        return
    global isWheeledTech
    if self.isPlayerVehicle:
        isWheeledTech = self.isWheeledTech and self.typeDescriptor.hasSiegeMode
        if isWheeledTech:
            arenaPeriod = BigWorld.player().guiSessionProvider.shared.arenaPeriod
            startBattle = arenaPeriod.getPeriod() if arenaPeriod is not None else 0
            if startBattle >= 3:
                BigWorld.player().enableOwnVehicleAutorotation(True)

@registerEvent(PreBattleTimer, 'hideCountdown')
def hideCountdown(self, state, speed):
    if not enableAutoSpeed:
        return
    if state == 3 and isWheeledTech:
        BigWorld.player().base.vehicle_changeSetting(VEHICLE_SETTING.SIEGE_MODE_ENABLED, True)

# add shooting range in gun info window for SPG/machine guns
@overrideMethod(ModuleInfoMeta, 'as_setModuleInfoS')
def ModuleInfoWindow_as_setModuleInfoS(base, self, moduleInfo):
    try:
        if moduleInfo['type'] == 'vehicleGun':
            veh_id = self._ModuleInfoWindow__vehicleDescr.type.compactDescr
            itemsCache = dependency.instance(IItemsCache)
            vehicle = itemsCache.items.getItemByCD(veh_id)
            gun = itemsCache.items.getItemByCD(self.moduleCompactDescr).descriptor
            turret = self._ModuleInfoWindow__vehicleDescr.turret    # not accurate, but not relevant here
            (viewRange, shellRadius, artiRadius) = _getRanges(turret, gun, vehicle.nationName, vehicle.type)
            if vehicle.type == 'SPG':   # arti
                moduleInfo['parameters']['params'].append({'type': '<h>' + 'shootingRadius' + ' <p>' +'(m)' + '</p></h>', 'value': '<h>' + str(artiRadius) + '</h>'})
            elif shellRadius < 707:     # not arti, short range weapons
                moduleInfo['parameters']['params'].append({'type': '<h>' + 'shootingRadius' + ' <p>' + '(m)' + '</p></h>', 'value': '<h>' + str(shellRadius) + '</h>'})
    except Exception, ex:
        print(traceback.format_exc())
    return base(self, moduleInfo)

# def ivmMaxFPS():
    #tree = ET.parse(CORE.engineXML)
    #root = tree.getroot()
#
#    if CORE.debug:
#        print '%s setting maxFPS to %s' % (CORE.ModIDShort, setMaxFPS)
#
#    tree.find('renderer/maxFrameRate').text = setMaxFPS
#    tree.write(CORE.engineXML)

#ivmMaxFPS()