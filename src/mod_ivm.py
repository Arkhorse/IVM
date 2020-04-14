#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
import Keys

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

modLinkage = 'mod_ivm'
template = {
    'modDisplayName': 'Improved Visuals and Sounds',
    'settingsVersion': 0.2,
    'enabled': True,
    'column1:': [
        {
            'type': 'Label',
            'text': 'In Battle Options',
        },
        {
            'type': 'CheckBox',
            'text': 'Missions Hint UI',
            'value': False,
            'tooltip': '{BODY} Turn this off if you dont want the missions hint UI at the start of the battle {/ BODY}',
            'varName': 'questHint'
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
            'varName': 'stunSoundEnabled'
        },
        {
            'type': 'CheckBox',
            'text': 'Fire Sound',
            'value': False,
            'tooltip': '{HEADER} Turn this on if you want a Voice Over for when you are set on fire. {/ HEADER} {BODY} This is the DeadPool one. {/ BODY}',
            'varName': 'fireSoundEnabled'
        }, 
    ],
    'column2': [
        {
            'type': 'Label',
            'text': 'In Garage Options'
        },
        {
            'type': 'Slider',
            'text': 'The number of carousel rows you want',
            'minimum': 1,
            'maximum': 12,
            'value': 2,
            'format': '{{{1}}}',
            'varName': 'tankrows'
        }
    ]
}

settings = {
            'Credits': False,
            'debug': False,
            'Battle': {
                'questHint': True,
            },
            'Sounds': {
                'stunSoundEnabled': False, 
                'fireSoundEnabled': False, 
            },
            'Carousels': {
                'Enabled': False,
#                'Large': True,
                'Rows': 3, 
            }
        }
def onButtonClicked(linkage, varName, value):
    if linkage == modLinkage:
        print 'onButtonClicked', linkage, varName, value

def onModSettingsChanged(linkage, newSettings):
    if linkage == modLinkage:
        print 'onModSettingsChanged', newSettings

try:
    from gui.modsSettingsApi import g_modsSettingsApi
    savedSettings = g_modsSettingsApi.getModSettings((modLinkage, ), template)
    if savedSettings:
        settings = savedSettings
        g_modsSettingsApi.registerCallback((modLinkage, ), onModSettingsChanged, onButtonClicked)
    else:
        settings = g_modsSettingsApi.setModTemplate((modLinkage, ), template, onModSettingsChanged, onButtonClicked)
except:
    pass

_config = settings

"""
IVM Carousel Handler
"""

if _config.Carousels.Enabled == True: #and _config.carouselsSize == False:
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS

    def new_as_rowCountS(self, value):
        old_as_rowsCountS(self, value)
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(_config.tankrows)

    TankCarouselMeta.as_rowCountS = new_as_rowCountS
    print '[IVM] Tank Carousels Loaded with ' + str(_config.tankrows) + ' rows'
else:
    print '[IVM] Tank Carousels Not Enabled'
    pass

"""
IVM Battle Hints Handler
"""
#Mission Hint Panel
if _config.Battle.questhint == False:
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

if _config.stunEnabled == True:
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
if _config.fireEnabled == True:
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

_LOAD_ = '[IVM][LOAD] IVM loaded with: ' + 'Carousels Enabled:', str(_config.carouselsEnabled), 'Rows:', str(_config.tankrows), 'Fire Sound Enabled:', str(_config.fireEnabled), 'Stun Sound Enabled:', str(_config.stunEnabled), 'Replays Enabled:', str(_config.replayEnabled)
if _config.credits == True:
    print _LOAD_, __credits__
else:
    print _LOAD_
