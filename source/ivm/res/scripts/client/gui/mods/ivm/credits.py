import BigWorld

from .Core import CORE

from PYmodsCore import PYmodsConfigInterface

class Credits(PYmodsConfigInterface):

    def init(self):
        self.ID = 'Credits'
        self.version = CORE.Version[1]
        self.data = {'enabled': True}
        super(Credits, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                'name': 'Credits',
                'UI_setting_translations_text': 'Translators:',
                'UI_setting_translator_RU_DRWEB7_1_text': 'Russian Translation: DrWeb7_1',
                'UI_setting_translator_ES_LordFelix_text': 'Spanish Translation: LordFelix'
            }

    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [
                self.tb.createLabel('UI_setting_translations_text'), 
                self.tb.createLabel('UI_setting_translator_RU_DRWEB7_1_text'), 
                self.tb.createLabel('UI_setting_translator_ES_LordFelix_text')
                ]
        }

    def onApplySettings(self, settings):
        pass

Credits()