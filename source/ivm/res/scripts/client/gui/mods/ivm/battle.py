import BigWorld
# Disable Starting hint
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin
# Disable destroyed messages imports
from gui.Scaleform.daapi.view.battle.shared.messages.fading_messages import FadingMessages
from constants import ARENA_GUI_TYPE
from Vehicle import Vehicle
from gui.Scaleform.daapi.view.battle.shared.battle_timers import PreBattleTimer
from constants import VEHICLE_SETTING

from ..mod_ivm import Version
from utils import overrideMethod, registerEvent
from PYmodsCore import PYmodsConfigInterface

class ivmBattle(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmBattle'
        self.version = Version
        self.modsGroups = 'IVM'
        self.data = {'enabled': True, 'questHintEnabled': True, 'notShowBattleMessage': True, 'enableAutoSpeed': True}
        super(ivmBattle, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                # UI_setting__text
                # UI_setting__tooltip
                'name': 'Battle Options',
                'UI_setting_questHintEnabled_text': 'Disable Mission Popup.',
                'UI_setting_questHintEnabled_tooltip': 'This will disable the mission popup at the start of battle.',
                'UI_setting_notShowBattleMessage_text': 'Disable Destroyed Tanks Message.',
                'UI_setting_notShowBattleMessage_tooltip': 'This will disable the messages for destroyed tanks above the minimap.',
                'UI_setting_enableAutoSpeed_text': 'Start Battle In Speed Mode For Wheeled \"Tanks\".',
                'UI_setting_enableAutoSpeed_tooltip': 'Always start in the speed mode for wheeled tanks with this.'
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('questHintEnabled'), self.tb.createControl('notShowBattleMessage')],
            'column2': [self.tb.createControl('enableAutoSpeed')]
        }

config = ivmBattle()
questHintEnabled = config.data['questHintEnabled']
notShowBattleMessage = config.data['notShowBattleMessage']
enableAutoSpeed = config.data['enableAutoSpeed']

#oldQuestHint_WG = PreBattleHintPlugin._PreBattleHintPlugin__canDisplayQuestHint
@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
def ivmQuestHint(base, self):
    #oldQuestHint_WG(self)
    if not questHintEnabled:
        print '[IVM] Quest Hint Skipped'
        return base(self)
    else:
        print '[IVM][LOAD] Missions Hint Panel Disabled'
        return None
#PreBattleHintPlugin._PreBattleHintPlugin__canDisplayQuestHint = ivmQuestHint


isFrontLine = False

# @registerEvent(Vehicle, 'onEnterWorld')
# def Vehicle_onEnterWorld(self, prereqs):
#     global isFrontLine
#     if self.isPlayerVehicle:
#         isFrontLine = BigWorld.player().arenaGuiType == ARENA_GUI_TYPE.EPIC_BATTLE


@overrideMethod(FadingMessages, 'showMessage')
def FadingMessages_showMessage(base, self, key, args=None, extra=None, postfix=''):
    if not notShowBattleMessage:
        return
    # if not isFrontLine:
    #     return base(self, key, args, extra, postfix)
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
