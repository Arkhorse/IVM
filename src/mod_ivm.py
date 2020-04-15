#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
import glob
import traceback
import re

#Game Imports
import BigWorld
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
        self.fixVehicleTransparency = False
        super(ConfigInterface, self).__init__()

    def init(self):
        self.ID = 'IVM'
        self.version = '0.2 (13/04/2020)'
        self.author += ' (The Illusion)'
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
            'fixVehicleTransparency': False
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
            'UI_setting_UI_changes_text': 'UI Changes',
            'UI_setting_Sounds_text': 'Sounds',
            'UI_setting_Fixes_text': 'Fixes',
            'UI_setting_Carousel_Options_text': 'Carousel Options'
        }
        super(ConfigInterface, self).init()
    
    def onApplySettings(self, settings):
        super(ConfigInterface, self).onApplySettings(settings)
        self.carEnabled = self.data['enabled'] and self.carEnabled
        self.carRows = self.data['carRows'] and self.carRows
        self.questHintEnabled = self.data['questHintEnabled'] and self.questHintEnabled
        self.stun = self.data['stunEnabled'] and self.stun
        self.fire = self.data['fireEnabled'] and self.fire
        self.fixEffects = self.data['fixEffects'] and self.fixEffects
        self.fixVehicleTransparency = self.data['fixVehicleTransparency'] and self.fixVehicleTransparency

    def loadLang(self):
        pass

    def createTemplate(self):
        return {'modDisplayName': self.i18n['name'],
         'enabled': self.data['enabled'],
         'column1': [self.tb.createLabel('UI_changes') ,self.tb.createControl('questHintEnabled'), self.tb.createLabel('Sounds'), self.tb.createControl('stunEnabled'), self.tb.createControl('fireEnabled'), self.tb.createLabel('Fixes'), self.tb.createControl('fixEffects'), self.tb.createControl('fixVehicleTransparency')],
         'column2': [self.tb.createLabel('Carousel_Options') ,self.tb.createControl('carEnabled'), self.tb.createStepper('carRows', 1.0, 12.0, 1.0, True)]}

    def readCurrentSettings(self, quiet=True):
        super(ConfigInterface, self).readCurrentSettings(quiet)
        self.settings = loadJson(self.ID, 'settings', self.settings, self.configPath)
        loadJson(self.ID, 'settings', self.settings, self.configPath, True, quiet=quiet)
        self.updateMod()

config = ConfigInterface()

"""
IVM Carousel Handler
"""

if config.data['carEnabled'] == True: #and _config.carouselsSize == False:
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS

    def new_as_rowCountS(self, value):
        old_as_rowsCountS(self, value)
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(config.data['carRows'])

    TankCarouselMeta.as_rowCountS = new_as_rowCountS
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
