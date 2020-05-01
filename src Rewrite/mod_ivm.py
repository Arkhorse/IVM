modLinkage = 'mod_ivm'

#Module Imports
import BigWorld
import BattleReplay
import os
import glob
import traceback
import re
import inspect
import sys
from os import path
from math import fabs
from functools import partial, update_wrapper
from debug_utils import LOG_CURRENT_EXCEPTION
from SoundGroups import g_instance as SoundGroups_g_instance
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
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
        self.DIR = os.path.join('mods', 'configs', 'IVM')
        self.FILE = os.path.join(self.DIR, 'IVM.json')

ident = Ident()
MOD_NAME = ident.ModIDInternal

print ident.ModIDLong + ' Loading'

try:
    from gui.modsSettingsApi import g_modsSettingsApi
    print ident.ModIDShort + ' Settings API found'
except ImportError:
    print ident.ModIDShort + ' Settings API not found, skipping. ' + 'Settings can be found at ' + ident.FILE
    pass

#@overrideMethod
def overrideMethod(obj, prop, getter=None, setter=None, deleter=None):
    """
    :param obj: object, which attribute needs overriding
    :param prop: attribute name (can be not mangled), attribute must be callable
    :param getter: fget function or None
    :param setter: fset function or None
    :param deleter: fdel function or None
    :return function: unmodified getter or, if getter is None and src is not property, decorator"""

    if inspect.isclass(obj) and prop.startswith('__') and prop not in dir(obj) + dir(type(obj)):
        prop = obj.__name__ + prop
        if not prop.startswith('_'):
            prop = '_' + prop
    src = getattr(obj, prop)
    if type(src) is property and (getter or setter or deleter):
        props = []
        for func, fType in ((getter, 'fget'), (setter, 'fset'), (deleter, 'fdel')):
            assert func is None or callable(func), fType + ' is not callable!'
            props.append(partial(func, getattr(src, fType)) if func else getattr(src, fType))
        setattr(obj, prop, property(*props))
        return getter
    elif getter:
        getter_orig = getter
        assert callable(src), 'Source property is not callable!'
        assert callable(getter_orig), 'Handler is not callable!'
        while isinstance(getter, partial):
            getter = getter.func

        def getter_new(*a, **k):  # noinspection PyUnusedLocal
            info = None
            try:
                return getter_orig(src, *a, **k)
            except Exception:  # Code to remove this wrapper from traceback
                info = sys.exc_info()
                new_tb = info[2].tb_next  # https://stackoverflow.com/q/44813333
                if new_tb is None:  # exception occurs inside this wrapper, not inside of getter_orig
                    new_tb = _generate_new_tb(getter.func_code)
                raise info[0], info[1], new_tb
            finally:
                del info

        try:
            update_wrapper(getter_new, getter)
        except AttributeError:
            pass
        if inspect.isclass(obj):
            if inspect.isfunction(src):
                getter_new = staticmethod(getter_new)
            elif getattr(src, '__self__', None) is not None:
                getter_new = classmethod(getter_new)
        setattr(obj, prop, getter_new)
        return getter_orig
    else:
        return partial(overrideMethod, obj, prop)

class AbstractSettings(object):
    
    def __init__(self, name):
        self.__name = name
        self.__registerModSettings()

    def __registerModSettings(self):
        settingsTemplate = self.getSettingsTemplate()
        savedSettings = g_modsSettingsApi.getModSettings(self.__name, settingsTemplate)
        if savedSettings:
            settings = savedSettings
            g_modsSettingsApi.registerCallback(self.__name, self.__onModSettingsChanged)
        else:
            settings = g_modsSettingsApi.setModTemplate(self.__name, settingsTemplate, self.__onModSettingsChanged)
        self.__onModSettingsChanged(self.__name, settings, True)

    def __onModSettingsChanged(self, linkage, settings, isFirst=False):
        if linkage == self.__name:
            self.onSettingsUpdated(settings, isFirst)

    def onSettingsUpdated(self, settings, isFirst):
        pass

    def getSettingsTemplate(self):
        raise NotImplementedError

import Keys

class Template(object):

    def __init__(self):
        self.defaultKeys = {
            'buttonRepair' : [Keys.KEY_SPACE],
            'buttonChassis': [[Keys.KEY_LALT, Keys.KEY_RALT]]
        }
        self.config = {'templates': {
                'modDisplayName': 'Improved Visuals and Sounds',
                'settingsVersion': 0.2,
                'enabled': True,
                'column1': [
                    {
                        'type': 'Label',
                        'text': 'In Battle Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Missions Hint UI',
                        'value': False,
                        'tooltip': '{BODY} Turn this off if you dont want the missions hint UI at the start of the battle {/ BODY}',
                        'varName': 'questHintEnabled'
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
                        'varName': 'stunEnabled'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Fire Sound',
                        'value': False,
                        'tooltip': '{HEADER} Turn this on if you want a Voice Over for when you are set on fire. {/ HEADER} {BODY} This is the DeadPool one. {/ BODY}',
                        'varName': 'fireEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'In Garage Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable Carousel Function',
                        'value': False,
                        'tooltip': '{BODY} Turn this on if you want to use the carousel stuff{/ BODY}',
                        'varName': 'carEnabled'
                    },
                    {
                        'type': 'Slider',
                        'text': 'The number of carousel rows you want',
                        'minimum': 1,
                        'maximum': 12,
                        'snapInterval': 1,
                        'value': 1,
                        'format': '{{value}}',
                        'varName': 'carRows'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable Garage Counters',
                        'value': True,
                        'varName': 'counterEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'Fixes, Ect'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Effects List Spam',
                        'tooltip': 'Removes the effects list spam from the python.log. This can cause this log to be very large. #WG',
                        'value': False,
                        'varName': 'fixEffects'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Vehicle Model Transparency',
                        'tooltip': 'Fixes a rare issue where the vehicle model isnt shown correctly',
                        'value': False,
                        'varName': 'fixVehicleTransparency'
                    },
                ],
                'column2': [
                    {
                        'type': 'Label',
                        'text': 'Repair Options'
                    },
                    {
                        'type': 'Label',
                        'text': 'Repair Options is legal. None of these options are automatic.'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable',
                        'value': False,
                        'varName': 'repairEnabled'
                    },
                    {
                        'type': 'HotKey',
                        'text': 'Repair Tracks and Wheels',
                        'value': [Keys.KEY_SPACE],
                        'varName': 'buttonChassis'
                    },
                    {
                        'type': 'HotKey',
                        'text': 'Smart Repair',
                        'value': [[Keys.KEY_LALT, Keys.KEY_RALT]],
                        'varName': 'buttonRepair'
                    },
                    {
                        'type': 'Label',
                        'text': 'Smart Repair Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Use Gold Kits',
                        'value': False,
                        'varName': 'useGoldKits'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Repair Tracks and Wheels',
                        'value': False,
                        'varName': 'restoreChassis'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Repair all Devices (Optics, Turret, Gun, Ect)',
                        'value': False,
                        'varName': 'repairDevices'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Heal Crew',
                        'value': False,
                        'varName': 'healCrew'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Extinguish Fires',
                        'value': False,
                        'varName': 'extinguishFire'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Remove Stun',
                        'value': False,
                        'varName': 'removeStun'
                    }]
                }, 'settings': {
                'enabled': True,
                'carEnabled': False,
                'carRows': 1,
                'questHintEnabled': True,
                'counterEnabled': True,
                'stunEnabled': False,
                'stunEvent': 'battle_event_stun',
                'fireEnabled': False,
                'fireEvent': 'battle_event_fire',
                'fixEffects': False,
                'fixVehicleTransparency': False,
                'emptyShellsEnabled': False,
                'emptyShellsEvent': 'IVM_emptyShellsEvent',
                'almostOutEvent': 'IVM_almostOutEvent',
                'TESTER': True,
                'repairEnabled': False,
                'buttonChassis' : self.defaultKeys['buttonChassis'],
                'buttonRepair'  : self.defaultKeys['buttonRepair'],
                'removeStun'    : True,
                'extinguishFire': True,
                'healCrew': True,
                'repairDevices': True,
                'restoreChassis': True,
                'useGoldKits'   : False,
                'repairPriority': {
                    'lightTank'            : {
                        'medkit'   : ['commander', 'driver', 'gunner', 'loader'],
                        'repairkit': ['ammoBay', 'engine', 'gun', 'turretRotator', 'fuelTank']
                    },
                    'mediumTank'           : {
                        'medkit'   : ['commander', 'loader', 'driver', 'gunner'],
                        'repairkit': ['ammoBay', 'turretRotator', 'engine', 'gun', 'fuelTank']
                    },
                    'heavyTank'            : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'turretRotator', 'engine', 'fuelTank']
                    },
                    'SPG'                  : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'engine', 'turretRotator', 'fuelTank']
                    },
                    'AT-SPG'               : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'engine', 'turretRotator', 'fuelTank']
                    },
                    'AllAvailableVariables': {
                        'medkit'   : ['commander', 'gunner', 'driver', 'radioman', 'loader'],
                        'repairkit': ['engine', 'ammoBay', 'gun', 'turretRotator', 'chassis', 'surveyingDevice', 'radio', 'fuelTank', 'wheel']
                    }
                }
            }}

template = Template()

class SettingsKeyGetter(object):
    
    def __init__(self, key, attribute='settings', wrapper=lambda value: value):
        super(SettingsKeyGetter, self).__init__()
        self.key = key
        self.attribute = attribute
        self.wrapper = wrapper
        assert callable(wrapper), 'Wrapper is not callable!'
        assert isinstance(key, str), 'Key is not string!'
        assert isinstance(attribute, str), 'Attribute is not string!'

    def __get__(self, instance, objtype=None):
        value = getattr(instance, self.attribute)[self.key]
        if self.wrapper:
            value = self.wrapper(value)
        return value

class SettingsKeyChecker(SettingsKeyGetter):
    
    def __init__(self, key, attribute='settings'):
        super(SettingsKeyChecker, self).__init__(key, attribute=attribute, wrapper=g_modsSettingsApi.checkKeySet)

class Ivm(AbstractSettings):
    enabled = SettingsKeyGetter('enabled')
    carEnabled = SettingsKeyGetter('carEnabled')
    carRows = SettingsKeyGetter('carRows')
    counterEnabled = SettingsKeyGetter('counterEnabled')
    questHintEnabled = SettingsKeyGetter('questHintEnabled')
    stunEnabled = SettingsKeyGetter('stunEnabled')
    stunEvent = SettingsKeyGetter('stunEvent')
    fireEnabled = SettingsKeyGetter('fireEnabled')
    fireEvent = SettingsKeyGetter('fireEvent')
    fixEffects = SettingsKeyGetter('fixEffects')
    emptyShellsEnabled = SettingsKeyGetter('emptyShellsEnabled')
    emptyShellsEvent = SettingsKeyGetter('emptyShellsEvent')
    almostOutEvent = SettingsKeyGetter('almostOutEvent')
    fixVehicleTransparency = SettingsKeyGetter('fixVehicleTransparency')
    repairEnabled = SettingsKeyGetter('repairEnabled')
    removeStun = SettingsKeyGetter('removeStun')
    extinguishFire = SettingsKeyGetter('extinguishFire')
    repairPriority = SettingsKeyGetter('repairPriority')
    healCrew = SettingsKeyGetter('healCrew')
    repairDevices = SettingsKeyGetter('repairDevices')
    restoreChassis = SettingsKeyGetter('restoreChassis')
    useGoldKits = SettingsKeyGetter('useGoldKits')
    repairPriority = SettingsKeyGetter('repairPriority')

    def __init__(self):
        AbstractSettings.__init__(self, MOD_NAME)
        self.settings = {}
        self.__name = ident.ModIDShort
        self.version = ident.Version
        self.config = template.config['settings']
        self.ivm_rowCount(value=None)
        self.ivm_questHint()
        self.ivm_setFireInVehicle(isInFire=None)
        self.ivm_stunSound(value=None)
        self.ivm_getShells(intCD=None)

    def getSettingsTemplate(self):
        if ident.debug:
            print "getSettingsTemplate"
        return template.config['templates']

    def onSettingsUpdated(self, settings, newSettings):
        if ident.debug:
            print modLinkage, 'onSettingsUpdated'
        self.settings = template.config['settings']
        settings = newSettings
        print ident.ModIDShort + ' Settings changed ', newSettings

    from gui.Scaleform.daapi.view.meta.tankcarouselmeta import TankCarouselMeta
    @overrideMethod(TankCarouselMeta, 'as_rowCountS')
    def ivm_rowCount(self, value):
        if ident.debug:
            print 'DEBUG: Carousel Options:', self.carEnabled, self.carRows
        if self.carEnabled:
            print '[IVM] Tank Carousels Loaded with ' + str(self.carRows) + ' rows'
            if self._isDAAPIInited():
                return self.flashObject.as_rowCount(self.carRows)
        else:
            print "[IVM] Tank Carousels Skipped"
            return

    from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import PreBattleHintPlugin
    @overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
    def ivm_questHint(self):
        if not self.questHintEnabled:
            print '[IVM] Quest Hint Skipped'
            return
        else:
            print '[IVM][LOAD] Missions Hint Panel Disabled'
        return None

    from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController
    from gui.battle_control.controllers.consumables.ammo_ctrl import _GunSettings
    from gui.Scaleform.daapi.view.battle.shared import destroy_timers_panel
    from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel

    @overrideMethod(DestroyTimersPanel, '_DestroyTimersPanel__setFireInVehicle')
    def ivm_setFireInVehicle(self, isInFire):
        try:
            if not self.fireEnabled:
                print '[IVM] Fire Event Skipped'
                return
            if isInFire:
                #play sound at event 'battle_event_fire'
                 SoundGroups_g_instance.playSound2D(self.fireEvent)
                 print '[IVM] Player On Fire'
            else:
                self._hideTimer(_TIMER_STATES.FIRE)
            return
        except:
            #if that doesnt work, log the exception
            print('Failed to play fire sound')
            LOG_CURRENT_EXCEPTION()
        print '[IVM][LOAD] IVM Fire Sound Loaded'

    @overrideMethod(DestroyTimersPanel, '_DestroyTimersPanel__showStunTimer')
    def ivm_stunSound(self, value):
        try:
            if not self.stunEnabled == True:
                print '[IVM] Stun Event Skipped'
                return
            if value.duration > 0.0:
                #play sound at event 'battle_event_stun'
                SoundGroups_g_instance.playSound2D(self.stunEvent)
                print '[IVM] Player Stunned'
        except:
            #if that doesnt work, log the error
            print '[ERROR][IVM] Stun Sound Not Played'
            LOG_CURRENT_EXCEPTION()

    from gui.battle_control.controllers.consumables.ammo_ctrl import AmmoController
    @overrideMethod(AmmoController, 'getShells')
    def ivm_getShells(self, intCD):
        if not self.emptyShellsEnabled == True:
            print '[IVM] Shells Events Skipped'
            return
        try:
            quantity, quantitInClip = self.__ammo[intCD]
            if quantity == 0 or quantitInClip == 0:
                SoundGroups_g_instance.playSound2D(self.emptyShellsEvent)
                print '[IVM] Player out of ammo'
            if quantity == 5 or quantitInClip == 5:
                SoundGroups_g_instance.playSound2D(self.almostOutEvent)
                print '[IVM] Player Almost out of ammo ', quantity + ' shells left'
        except KeyError :
            LOG_ERROR('Shell is not found.', intCD)
            quantity, quantityInClip = (SHELL_QUANTITY_UNKNOWN,) * 2

Ivm()

print ident.ModIDLong + ' Loaded'
