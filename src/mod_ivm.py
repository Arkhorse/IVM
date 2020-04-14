#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path

#Game Imports
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta
#Hints Panel
from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin
#Sounds
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel
from SoundGroups import g_instance as SoundGroups_g_instance
from gui import SystemMessages
from Account import PlayerAccount
from PYmodsCore import PYmodsConfigInterface

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
    
    def init(self):
        self.ID = 'IVM'
        self.version = '0.2 (13/04/2020)'
        self.author += ' (The Illusion)'
        self.data = {
            'enabled': True,
            'carEnabled': False,
            'carRows': 1,
            'questHintEnabled': True,
            'soundStun1': False,
            'soundFire1': False
        }
        self.i18n = {
            'name': 'Improved Visuals and Sounds',
            'UI_setting_carEnabled_text': 'Enable Carousel Module, you will need to reload to see the effect.',
            'UI_setting_carRows_text': 'Number of rows you want',
            'UI_setting_questHintEnabled_text': 'Turn this off if you dont want the mission hint at the start of battle',
            'UI_setting_soundStun1_text': 'Enable for a Voice Over when you are stunned',
            'UI_setting_soundFire1_text': 'Enable for a Voice Over when you are on fire'
        }
        super(ConfigInterface, self).init()

    def createTemplate(self):
        return {'modDisplayName': self.i18n['name'],
         'enabled': self.data['enabled'],
         'column1': [self.tb.createControl('questHintEnabled'), self.tb.createControl('soundStun1'), self.tb.createControl('soundFire1')],
         'column2': [self.tb.createControl('carEnabled'), self.tb.createStepper('carRows', 1.0, 12.0, 1.0, True)]}

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

if config.data['soundStun1'] == True:
    #assign old event
    old_DestroyTimersPanel__showStunTimer = DestroyTimersPanel._DestroyTimersPanel__showStunTimer
    #define new event
    def illusion_stunSound_DestroyTimersPanel__showStunTimer(self, value):
        #call old event
        old_DestroyTimersPanel__showStunTimer(self, value)
        try:
            if value.duration > 0.0:
                #play sound at event 'battle_event_stun'
                SoundGroups_g_instance.playSound2D('battle_event_stun')
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
if config.data['soundFire1'] == True:
    #assign old event
    old_DestroyTimersPanel__setFireInVehicle = DestroyTimersPanel._DestroyTimersPanel__setFireInVehicle

    def IVM_new__setFireInVehicle(self, isInFire):
        old_DestroyTimersPanel__setFireInVehicle(self, isInFire)
        try:
            if isInFire:
                #play sound at event 'battle_event_fire'
                SoundGroups_g_instance.playSound2D('battle_event_fire')
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

#_LOAD_ = '[IVM][LOAD] IVM loaded with: ' + 'Carousels Enabled:', str(_config.carouselsEnabled), 'Rows:', str(_config.tankrows), 'Fire Sound Enabled:', str(_config.fireEnabled), 'Stun Sound Enabled:', str(_config.stunEnabled), 'Replays Enabled:', str(_config.replayEnabled)
#if _config.Credits == True:
#    print _LOAD_, __credits__
#else:
#    print _LOAD_
