import BigWorld
from gui.battle_control.controllers.consumables import ammo_ctrl
from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController, _GunSettings
from gui.Scaleform.daapi.view.battle.shared import timers_panel
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import AmmoPlugin
from debug_utils import LOG_CURRENT_EXCEPTION

from .Core import overrideMethod, CORE
from PYmodsCore import PYmodsConfigInterface

class ivmSound(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmSound'
        self.version = CORE.Version
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
                'UI_setting_fireEvent_text': 'Fire Event',
                'UI_setting_fireEvent_tooltip': 'Dont change this unless you know what you are doing!',
                'UI_setting_stunEvent_text': 'Stun Event',
                'UI_setting_stunEvent_tooltip': 'Dont change this unless you know what you are doing!',
                'UI_setting_almostOutEvent_text': 'Almost Out Event',
                'UI_setting_almostOutEvent_tooltip': 'Dont change this unless you know what you are doing!',
                'UI_setting_emptyShellsEvent_text': 'Empty Shells Event',
                'UI_setting_emptyShellsEvent_tooltip': 'Dont change this unless you know what you are doing!',
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [
                self.tb.createControl('fireEnabled'), 
                self.tb.createControl('stunEnabled'), 
                self.tb.createControl('emptyShellsEnabled')
                ],
            'column2': [
                self.tb.createControl('fireEvent', self.tb.types.TextInput, 400), 
                self.tb.createControl('stunEvent', self.tb.types.TextInput, 400), 
                self.tb.createControl('emptyShellsEvent', self.tb.types.TextInput, 400), 
                self.tb.createControl('almostOutEvent', self.tb.types.TextInput, 400)
                ]
        }

    def onApplySettings(self, settings):
        super(ivmSound, self).onApplySettings(settings)
        pass

config = ivmSound()
fireEnabled = config.data['fireEnabled']
fireEvent = config.data['fireEvent']
stunEnabled = config.data['stunEnabled']
stunEvent = config.data['stunEvent']
emptyShellsEnabled = config.data['emptyShellsEnabled']
emptyShellsEvent = config.data['emptyShellsEvent']
almostOutEvent = config.data['almostOutEvent']

@overrideMethod(TimersPanel, '_TimersPanel__setFireInVehicle')
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

@overrideMethod(TimersPanel, '_TimersPanel__showStunTimer')
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
        