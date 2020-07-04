import BigWorld
<<<<<<< Updated upstream
from ..mod_ivm import Version
from utils import overrideMethod
from PYmodsCore import PYmodsConfigInterface
=======
# Disable Starting hint
>>>>>>> Stashed changes
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin
# Disable destroyed messages imports
from gui.Scaleform.daapi.view.battle.shared.messages.fading_messages import FadingMessages
from constants import ARENA_GUI_TYPE
from Vehicle import Vehicle

from ..mod_ivm import Version
from utils import overrideMethod, registerEvent
from PYmodsCore import PYmodsConfigInterface

class ivmBattle(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmBattle'
        self.version = Version
        self.modsGroups = 'IVM'
        self.data = {'enabled': True, 'questHintEnabled': True, 'notShowBattleMessage': True}
        super(ivmBattle, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                'name': 'Battle Options',
                'UI_setting_questHintEnabled_text': 'This will disable the mission popup at the start of battle.',
                'UI_setting_notShowBattleMessage_text': 'This will disable the messages for destroyed tanks above the minimap.'
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('questHintEnabled'), self.tb.createControl('notShowBattleMessage')]
        }

config = ivmBattle()
questHintEnabled = config.data['questHintEnabled']
notShowBattleMessage = config.data['notShowBattleMessage']

<<<<<<< Updated upstream
@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
def ivmQuestHint(self):
=======
#oldQuestHint_WG = PreBattleHintPlugin._PreBattleHintPlugin__canDisplayQuestHint
@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
def ivmQuestHint(base, self):
    #oldQuestHint_WG(self)
>>>>>>> Stashed changes
    if not questHintEnabled:
        print '[IVM] Quest Hint Skipped'
        return base(self)
    else:
        print '[IVM][LOAD] Missions Hint Panel Disabled'
<<<<<<< Updated upstream
    return None
=======
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
>>>>>>> Stashed changes
