from gui.battle_control.controllers.consumables import ammo_ctrl
from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController, _GunSettings
from gui.Scaleform.daapi.view.battle.shared import destroy_timers_panel
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel
from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import AmmoPlugin
from debug_utils import LOG_CURRENT_EXCEPTION
import BigWorld

from Core import overrideMethod, CORE
try:
    from PYmodsCore import PYmodsConfigInterface
except ImportError:
    print '%s Fatal Error! A dependency is not found' % (CORE.ModIDShort)

class ivmSound(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmSound'
        self.version = CORE.Version
        self.modsGroups = 'IVM'
        self.data = {
            'enabled': True,
            'fireEnabled': True,
            'fireEvent': 'battle_event_stun',
            'stunEnabled': True,
            'stunEvent': 'battle_event_fire',
            'emptyShellsEnabled': True,
            'emptyShellsEvent': 'IVM_emptyShellsEvent',
            'almostOutEvent': 'IVM_almostOutEvent'
        }
        super(ivmSound, self).init()
    
    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                'name': 'Sound Options',
                'UI_setting_fireEnabled_text': 'Enable Fire Sound',
                'UI_setting_stunEnabled_text': 'Enable Stun Sound',
                'UI_setting_emptyShellsEnabled_text': 'Enable Shell Alert Sounds',
                'UI_setting_fireEvent_text': 'Fire Event is ' + self.data['fireEvent'],
                'UI_setting_stunEvent_text': 'Stun Event is ' + self.data['stunEvent'],
                'UI_setting_almostOutEvent_text': 'Almost Out Event is ' + self.data['almostOutEvent'],
                'UI_setting_emptyShellsEvent_text': 'Empty Shells Event is ' + self.data['emptyShellsEvent']
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('fireEnabled'), self.tb.createControl('stunEnabled'), self.tb.createControl('emptyShellsEnabled')],
            'column2': [self.tb.createLabel('fireEvent'), self.tb.createLabel('stunEvent'), self.tb.createLabel('emptyShellsEvent'), self.tb.createLabel('almostOutEvent')]
        }

config = ivmSound()
fireEnabled = config.data['fireEnabled']
fireEvent = config.data['fireEvent']
stunEnabled = config.data['stunEnabled']
stunEvent = config.data['stunEvent']
emptyShellsEnabled = config.data['emptyShellsEnabled']
emptyShellsEvent = config.data['emptyShellsEvent']
almostOutEvent = config.data['almostOutEvent']

@overrideMethod(DestroyTimersPanel, '_DestroyTimersPanel__setFireInVehicle')
def ivm_setFireInVehicle(base, self, isInFire):
    try:
        if not fireEnabled:
            print '[IVM] Fire Event Skipped'
            return base(self, isInFire)
        if isInFire:
            # play sound at event 'battle_event_fire'
            CORE.send2DSoundEvent(fireEvent)
            print '[IVM] Player On Fire'
        else:
            self._hideTimer(_TIMER_STATES.FIRE)
        return
    except:
        # if that doesnt work, log the exception
        print('Failed to play fire sound')
        LOG_CURRENT_EXCEPTION()
    print '[IVM][LOAD] IVM Fire Sound Loaded'

@overrideMethod(DestroyTimersPanel, '_DestroyTimersPanel__showStunTimer')
def ivm_stunSound(base, self, value):
    try:
        if not stunEnabled:
            print '[IVM] Stun Event Skipped'
            return base(self, value)
        if value.duration > 0.0:
            # play sound at event 'battle_event_stun'
            CORE.send2DSoundEvent(stunEvent)
            print '[IVM] Player Stunned'
    except:
        # if that doesnt work, log the error
        print '[ERROR][IVM] Stun Sound Not Played'
        LOG_CURRENT_EXCEPTION()

from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController

@overrideMethod(AmmoController, 'getShells')
def ivm_getShells(base, self, intCD):
    if not emptyShellsEnabled:
        print '[IVM] Shells Events Skipped'
        return base(self, intCD)
    try:
        quantity = AmmoPlugin.quantity
        quantitInClip = AmmoPlugin.quantityInClip
        if quantity == 0 or quantitInClip == 0:
            CORE.send2DSoundEvent(emptyShellsEvent)
            print '[IVM] Player out of ammo'
        if quantity == 5 or quantitInClip == 5:
            CORE.send2DSoundEvent(almostOutEvent)
            print '[IVM] Player Almost out of ammo %s shells left' % (quantity)
    except KeyError:
        LOG_ERROR('Shell is not found.', intCD)
        quantity, quantityInClip = (SHELL_QUANTITY_UNKNOWN,) * 2
        