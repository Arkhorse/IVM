"""
IVM fire sound handler
"""
#Global imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
#Game imports
from SoundGroups import g_instance as SoundGroups_g_instance
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel

_FILE_ = './mods/configs/IVM/fire.json'



if _config.enabled:
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

    print '[LOAD] IVM Fire Sound Loaded'
else:
    print '[IVM] Fire Sound not enabled'
    pass