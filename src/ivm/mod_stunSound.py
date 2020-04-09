#imports
from SoundGroups import g_instance as SoundGroups_g_instance
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel

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
        print('[illusion.stunSound] Error on playing stun sound')
        LOG_CURRENT_EXCEPTION()
#replace old event with new one
DestroyTimersPanel._DestroyTimersPanel__showStunTimer = illusion_stunSound_DestroyTimersPanel__showStunTimer

print('Loading mod: illusion.stunSound 2020-04-06; scripted by RaJCeL')