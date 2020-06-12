# Module Imports
import BigWorld
import BattleReplay
import os
import glob
import traceback
import re
import inspect
import sys
import items
import math
import codecs
import json
from os import path
from math import fabs
from functools import partial, update_wrapper
from debug_utils import LOG_CURRENT_EXCEPTION
from SoundGroups import g_instance as SoundGroups_g_instance
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
from gui.mods.settings import AbstractSettings, SettingsKeyGetter, overrideMethod
from gui.mods.template import Template
# All other imports happen as they are needed


class Ident(object):

    def __init__(self):
        super(Ident, self).__init__()
        self.Author = "The Illusion"
        self.Version = "Rel 0 ", "Patch 0.02"
        self.Status = "Dev"
        self.debug = True
        self.ModIDInternal = 'mod_ivm'
        self.ModIDShort = "IVM"
        self.ModIDLong = "Improved Visuals and Sounds"
        self.DIR = './mods/configs/IVM'
        self.FILE = self.DIR, 'ivm.json'

ident = Ident()
MOD_NAME = ident.ModIDInternal

print ident.ModIDLong + ' Loading'

try:
    from gui.modsSettingsApi import g_modsSettingsApi
    print ident.ModIDShort + ' Settings API found'
except ImportError:
    print ident.ModIDShort + ' Settings API not found, skipping. ' + 'Settings can be found at ' + ident.FILE
    pass

template = Template()

def ConfigCreate(self):
    if not os.path.exists(ident.DIR):
        os.makedirs(ident.DIR)
    try:
        with open('./mods/configs/IVM/ivm.json', 'w') as json_file:
            jsonDump(template.config['settings'], json_file, separators=(',', ': '), indent=4, sort_keys=False)
            json_file.write('\n')
            print '[IVM] New Config Generated'
    except:
        LOG_CURRENT_EXCEPTION()
        print '[IVM] ConfigCreate Failed'

config = template.config['settings']

def ConfigCheck(self):
        _FILE_ = './mods/configs/IVM/ivm.json'
        if path.exists(_FILE_):
            with open(_FILE_, 'r+') as f:
                data = jsonLoad(f)
                enabled = config['enabled']
                carEnabled = config['carEnabled']
                carRows = config['carRows']
                counterEnabled = config['counterEnabled']
                questHintEnabled = config['questHintEnabled']
                stunEnabled = config['stunEnabled']
                stunEvent = config['stunEvent']
                fireEnabled = config['fireEnabled']
                fireEvent = config['fireEvent']
                fixEffects = config['fixEffects']
                emptyShellsEnabled = config['emptyShellsEnabled']
                emptyShellsEvent = config['emptyShellsEvent']
                almostOutEvent = config['almostOutEvent']
                fixVehicleTransparency = config['fixVehicleTransparency']
                repairEnabled = config['repairEnabled']
                removeStun = config['removeStun']
                extinguishFire = config['extinguishFire']
                repairPriority = config['repairPriority']
                healCrew = config['healCrew']
                repairDevices = config['repairDevices']
                restoreChassis = config['restoreChassis']
                useGoldKits = config['useGoldKits']
                repairPriority = config['repairPriority']
                print '[IVM] Config Found'
        else:
            LOG_CURRENT_EXCEPTION()
            print '[IVM] Config not found'
            ConfigCreate(self)
            pass

def ConfigUpdate(self, key):
    with open(ident.FILE, 'r+') as f:
        data = jsonLoad(f)
        tmp = data[key]
        data[key] = 'newSettings'
        f.seek(0)
        jsonDump(data, f)
        f.truncate()

enabled = config['enabled']
carEnabled = config['carEnabled']
carRows = config['carRows']
counterEnabled = config['counterEnabled']
questHintEnabled = config['questHintEnabled']
stunEnabled = config['stunEnabled']
stunEvent = config['stunEvent']
fireEnabled = config['fireEnabled']
fireEvent = config['fireEvent']
fixEffects = config['fixEffects']
emptyShellsEnabled = config['emptyShellsEnabled']
emptyShellsEvent = config['emptyShellsEvent']
almostOutEvent = config['almostOutEvent']
fixVehicleTransparency = config['fixVehicleTransparency']
repairEnabled = config['repairEnabled']
removeStun = config['removeStun']
extinguishFire = config['extinguishFire']
repairPriority = config['repairPriority']
healCrew = config['healCrew']
repairDevices = config['repairDevices']
restoreChassis = config['restoreChassis']
useGoldKits = config['useGoldKits']
repairPriority = config['repairPriority']

class IVM(AbstractSettings):

    def __init__(self):
        AbstractSettings.__init__(self, MOD_NAME)
                
    def getSettingsTemplate(self):
        if ident.debug:
            print "getSettingsTemplate"
        return template.config['templates']

    def onSettingsUpdated(self, settings, newSettings):
        if ident.debug:
            print 'onSettingsUpdated'
            print settings
            print newSettings            
        self.settings = template.config['settings']
        key = newSettings
        #ConfigUpdate(self, key)
        print ident.ModIDShort + ' Settings changed ', newSettings

IVM()

from gui.Scaleform.daapi.view.meta.tankcarouselmeta import TankCarouselMeta

if carEnabled:
    @overrideMethod(TankCarouselMeta, 'as_rowCountS')
    def ivm_rowCount(self, value):
        if ident.debug:
            print 'DEBUG: Carousel Options:', carEnabled, carRows
        if carEnabled:
            print '[IVM] Tank Carousels Loaded with ' + str(carRows) + ' rows'
            if self._isDAAPIInited():
                return self.flashObject.as_rowCount(carRows)
        else:
            print "[IVM] Tank Carousels Skipped"
            return

if questHintEnabled:
    from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin

    @overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
    def ivm_questHint(self):
        if not questHintEnabled:
            print '[IVM] Quest Hint Skipped'
            return
        else:
            print '[IVM][LOAD] Missions Hint Panel Disabled'
        return None

if fireEnabled or stunEnabled:
    from gui.battle_control.controllers.consumables import ammo_ctrl
    from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController, _GunSettings
    from gui.Scaleform.daapi.view.battle.shared import destroy_timers_panel
    from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel

    @overrideMethod(DestroyTimersPanel, '_DestroyTimersPanel__setFireInVehicle')
    def ivm_setFireInVehicle(self, isInFire):
        try:
            if not fireEnabled:
                print '[IVM] Fire Event Skipped'
                return
            if isInFire:
                # play sound at event 'battle_event_fire'
                SoundGroups_g_instance.playSound2D(fireEvent)
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
    def ivm_stunSound(self, value):
        try:
            if not stunEnabled:
                print '[IVM] Stun Event Skipped'
                return
            if value.duration > 0.0:
                # play sound at event 'battle_event_stun'
                SoundGroups_g_instance.playSound2D(stunEvent)
                print '[IVM] Player Stunned'
        except:
            # if that doesnt work, log the error
            print '[ERROR][IVM] Stun Sound Not Played'
            LOG_CURRENT_EXCEPTION()

if emptyShellsEnabled:
    from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController

    @overrideMethod(AmmoController, 'getShells')
    def ivm_getShells(self, intCD):
        if not emptyShellsEnabled:
            print '[IVM] Shells Events Skipped'
            return
        try:
            quantity, quantitInClip = self.__ammo[intCD]
            if quantity == 0 or quantitInClip == 0:
                SoundGroups_g_instance.playSound2D(emptyShellsEvent)
                print '[IVM] Player out of ammo'
            if quantity == 5 or quantitInClip == 5:
                SoundGroups_g_instance.playSound2D(almostOutEvent)
                print '[IVM] Player Almost out of ammo ', quantity + ' shells left'
        except KeyError:
            LOG_ERROR('Shell is not found.', intCD)
            quantity, quantityInClip = (SHELL_QUANTITY_UNKNOWN,) * 2


print ident.ModIDLong + ' Loaded'
