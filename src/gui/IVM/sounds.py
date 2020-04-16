from _config import config
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel
from SoundGroups import g_instance as SoundGroups_g_instance
from debug_utils import LOG_CURRENT_EXCEPTION

# Stun Sound
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

# Fire Sound
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

#Empty Shells Sound
if config.data['emptyShellsEnabled'] == True and config.TESTER == True:
    from gui.battle_control.battle_constants import CANT_SHOOT_ERROR
    def ivmEmptyShells(self):
        if CANT_SHOOT_ERROR:
            count = 0
            SoundGroups_g_instance.playSound2D(config.data['emptyShellsEvent'])
            count += 1
            print '[IVM] Player is out of shells! #' + count

        #if (shellsInClip == 0 and not timeLeft == 0 and self.__gunSettings.hasAutoReload() or not shellsInClip >= 1 and timeLeft != 0):
            #SoundGroups_g_instance.playSound2D(config.data['almostOutEvent'])