#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
from debug_utils import LOG_CURRENT_EXCEPTION

#Game Imports
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

class _Config(object):

    def __init__(self):
        self.carouselsEnabled = True
        self.carouselsSize = 'Large'
        self.tankrows = 3
        self.questhintPanelEnabled = True
        self.fireEnabled = True
        self.stunEnabled = True
        self.replayEnabled = True
        self.debug = True
        self.credits = True
        self.Cdebug = False
        self.confdata = {
            'Credits': False,
            'debug': False,
            'Replays': True,
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
        self.cdata = jsonDumps(self.confdata, indent=4, sort_keys=False)

_config = _Config()

def _makeconfig():
    data = {}
    if _config.confdata:
        if _config.Cdebug:
            print '[IVM] _config.confdata found'
        try:
            os.makedirs(_DIR_)
        except:
            LOG_CURRENT_EXCEPTION()
            print '[ERROR][IVM] ' + str(_DIR_) + ' Failed to create, or already created'
            pass
        with open(_FILE_, 'w') as json_file:
            jsonDump(_config.confdata, json_file, separators=(',', ': '), indent=4, sort_keys=False)
            json_file.write('\n')
            if _config.debug:
                print '[IVM] New Config file created from default settings!'
                print '[IVM] IVM config file can be found at {default wot folder}' + str(_FILE_)
    else:
        if _config.Cdebug:
            print '[IVM] _config.confdata not found'
        if _config.debug:
            print '[IVM] Python file corrupted REDOWNLOAD MOD!!!!!'

def _chkfile():
    if path.exists(_FILE_):
        if _config.Cdebug:
            print '[IVM] config file found'
        with open(_FILE_) as f:
            data = jsonLoad(f)
            _config.carouselsEnabled = data['Carousels']['Enabled']
#            _config.carouselsSize = data['Carousels']['Large']
            _config.tankrows = data['Carousels']['Rows']
            _config.stunEnabled = data['Sounds']['stunSoundEnabled']
            _config.fireEnabled = data['Sounds']['fireSoundEnabled']
            _config.replayEnabled = data['Replays']
            _config.credits = data['Credits']
            _config.questhintPanelEnabled = data['Battle']['questHint']
            if data['debug']:
                _config.debug = True
            else:
                _config.debug = False
    else:
        if _config.debug:
            print '[IVM] config file not found creating one...'
        _makeconfig()

_chkfile()
if _config.replayEnabled == True:
    import BattleReplay
    print '[IVM] Battle Replays Enabled'

"""
IVM Carousel Handler
"""

if _config.carouselsEnabled == True: #and _config.carouselsSize == False:
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
if _config.questhintPanelEnabled == False:
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
