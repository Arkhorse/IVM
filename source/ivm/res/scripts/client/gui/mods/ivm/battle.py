import BigWorld
from ..mod_ivm import Version
from utils import override
from PYmodsCore import PYmodsConfigInterface
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin


class ivmBattle(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmBattle'
        self.version = Version
        self.modsGroups = 'IVM'
        self.data = {'enabled': True, 'questHintEnabled': True}
        super(ivmBattle, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                'name': 'Battle Options',
                'UI_setting_questHintEnabled_text': 'This will disable the mission popup at the start of battle'
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('questHintEnabled')]
        }
    

config = ivmBattle()
questHintEnabled = config.data['questHintEnabled']

class IVMQuestHint(object):

    def __init__(self):
        override(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint', self.ivmQuestHint)
    
    # @overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
    def ivmQuestHint(self, baseFunc, baseSelf):
        if not questHintEnabled:
            print '[IVM] Quest Hint Skipped'
            return
        else:
            
            print '[IVM][LOAD] Missions Hint Panel Disabled'
            return None