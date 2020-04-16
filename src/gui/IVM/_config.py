from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
import glob
import traceback
import re

import mod_constants

from PYmodsCore import PYmodsConfigInterface, loadJson, remDups

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
        super(ConfigInterface, self).__init__()

    def init(self):
        self.ID = 'IVM'
        self.version = '0.2 (13/04/2020)'
        self.author = '(The Illusion)'
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
            'TESTER': True
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
         'column2': [self.tb.createLabel('Carousel_Options') ,self.tb.createControl('carEnabled'), self.tb.createStepper('carRows', 1.0, 12.0, 1.0, True)]}

    def readCurrentSettings(self, quiet=True):
        super(ConfigInterface, self).readCurrentSettings(quiet)
        self.settings = loadJson(self.ID, 'settings', self.settings, self.configPath)
        loadJson(self.ID, 'settings', self.settings, self.configPath, True, quiet=quiet)
        self.updateMod()

config = ConfigInterface()