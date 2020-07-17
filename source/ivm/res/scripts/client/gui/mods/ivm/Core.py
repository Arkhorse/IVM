# Game Code
from BigWorld import player, callback, wg_getPreferencesFilePath
from gui import SystemMessages
import constants
from constants import ARENA_BONUS_TYPE
from account import PlayerAccount
from helpers.statistics import StatisticsCollector
# from helpers.statistics.StatisticsCollector import __onHangarSpaceLoaded
from helpers.statistics import HANGAR_LOADING_STATE
from SoundGroups import g_instance as SoundInstance
from gun_rotation_shared import calcPitchLimitsFromDesc
# Global Imports
import os
from math import sin, radians
from xml.etree import ElementTree
from time import sleep

class Core(object):
    def __init__(self):
        self.realmCT                = constants.CURRENT_REALM['CT']
        self.discordInvite          = 'https://discordapp.com/invite/58fdPvK'
        self.Author                 = 'The Illusion'
        self.Credits                = 'RaJCel'
        self.Version                = ['Rel 0 ', 'Patch 0.05']
        self.Status                 = 'Dev'
        self.debug                  = False
        self.Tester                 = False
        self.ModIDInternal          = 'mod_ivm'
        self.ModIDShort             = 'IVM'
        self.ModIDLong              = 'Improved Visuals and Sounds'
        self.defaultConfig          = os.path.join('mods', 'configs', 'theillusion')
        self.domain                 = 'https://bigmods.relhaxmodpack.com/WoT/'
        self.domainVersion          = '1.9.1'
        self.domainZip              = 'Dependency_IVM_Main_v0.03_1.9.1.1_2020-07-02.zip'
        self.downloadURL            = os.path.join(self.domain, self.domainVersion, self.domainZip)
        self.buildVersionClient     = '1.9.1.2'
        self.FrontlineBattleType    = ARENA_BONUS_TYPE.EPIC_BATTLE
        self.RandomBattleType       = ARENA_BONUS_TYPE.REGULAR
        self.gameVersion            = ElementTree.parse('./paths.xml').find('Paths').find('Path').text.split("/")[-1]
        self.appdataPath            = unicode(wg_getPreferencesFilePath()).replace('/preferences.xml', '')
        self.engineXML              = './res_mods/%s/engine_config.xml' % (self.gameVersion)
        self.MaxFPS                 = ElementTree.parse(self.engineXML).find('renderer').find('maxFrameRate')
        self._VEHICLE_TYPE_XML_PATH = 'scripts/item_defs/vehicles/'
        self.translationCodes       = ['en', 'es', 'ru']
        self.en                     = '.mods/configs/ivm/en.json'
        super(Core, self).__init__()

    #def onHangarSpaceLoaded(self):
        #return __hangarLoaded

    def openWebBrowser(self, url):
        BigWorld.wg_openWebBrowser(url)

    def getAccountPlayerName(self):
        return getattr(BigWorld.player(), 'name', None)

    def getCurrentHangerState(self, state):
        """
        LOGIN = 0
        CONNECTED = 1
        SHOW_GUI = 2
        QUESTS_SYNC = 3
        USER_SERVER_SETTINGS_SYNC = 4
        START_LOADING_SPACE = 5
        START_LOADING_VEHICLE = 6
        FINISH_LOADING_VEHICLE = 7
        FINISH_LOADING_SPACE = 8
        HANGAR_UI_READY = 9
        TRAINING_UI_READY = 10
        HANGAR_READY = 11
        START_LOADING_TUTORIAL = 12
        FINISH_LOADING_TUTORIAL = 13
        DISCONNECTED = 14
        COUNT = 15
        """
        # HANGAR_LOADING_STATE
        if state < 0 or state > HANGAR_LOADING_STATE.COUNT:
            print '%s Unknown Hanger State {0}'.format(state)
            stateCondition = 'Unknown'
        return state

    def joinPaths(self, a):
        path = a
        os.path.join(path)

    def compareBuildClient(self):
        modBuild = self.buildVersionClient
        if self.debug:
            print modBuild, self.gameVersion
        if modBuild != self.gameVersion:
            print self.ModIDShort, 'Warning!\nMod is not built for %s game version.\nYou may encounter issues!' % (self.gameVersion)

    def printLoadMessage(self, modCodeName, spacer, buildDate):
        print 'Loading mod: The Illusion.%s%s | %s | Support: %s' % (modCodeName, spacer, buildDate, self.discordInvite)

    def addSystemMessage_GameGreeting(self, message):
        #if StatisticsCollector.__onHangarSpaceLoaded.__hangarLoaded:
            SystemMessages.pushMessage(message, type = SystemMessages.SM_TYPE.GameGreeting)

    def addSystemMessage_Error(self, message):
        #if StatisticsCollector.__onHangarSpaceLoaded.__hangarLoaded:
            SystemMessages.pushMessage(message, type = SystemMessages.SM_TYPE.Error)

    def applyMacros(self, msg, macrosNb, macros, values):
        for i in range(macrosNb):
            msg = msg.replace(macros[i], values[i])
        return msg

    def getCurrentVehicle(self):
        player = player()
        vehicle = player.getVehicleAttached()
        return vehicle
    
    def send2DSoundEvent(self, event):
        if self.debug:
            print '%s playing %s 2D sound event' % (self.ModIDShort, event)
        return SoundInstance.playSound2D(event)

CORE = Core()
_VEHICLE_TYPE_XML_PATH = CORE._VEHICLE_TYPE_XML_PATH

# All below this has been taken from XVM. This was allowed at the time of usage.
#####################################################################
# EventHook

class EventHook(object):

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        if handler in self.__handlers:
            self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler

#####################################################################
# Register events

def _RegisterEvent(handler, cls, method, prepend=False):
    evt = '__event_%i_%s' % ((1 if prepend else 0), method)
    if hasattr(cls, evt):
        e = getattr(cls, evt)
    else:
        newm = '__orig_%i_%s' % ((1 if prepend else 0), method)
        setattr(cls, evt, EventHook())
        setattr(cls, newm, getattr(cls, method))
        e = getattr(cls, evt)
        m = getattr(cls, newm)
        l = lambda *a, **k: __event_handler(prepend, e, m, *a, **k)
        l.__name__ = method
        setattr(cls, method, l)
    e += handler

def __event_handler(prepend, e, m, *a, **k):
    try:
        if prepend:
            e.fire(*a, **k)
            r = m(*a, **k)
        else:
            r = m(*a, **k)
            e.fire(*a, **k)
        return r
    except:
        print '[IVM] Error: __event_handler'
def _override(cls, method, newm):
    orig = getattr(cls, method)
    if type(orig) is not property:
        setattr(cls, method, newm)
    else:
        setattr(cls, method, property(newm))

def _OverrideMethod(handler, cls, method):
    orig = getattr(cls, method)
    newm = lambda *a, **k: handler(orig, *a, **k)
    newm.__name__ = method
    _override(cls, method, newm)

def _OverrideStaticMethod(handler, cls, method):
    orig = getattr(cls, method)
    newm = staticmethod(lambda *a, **k: handler(orig, *a, **k))
    _override(cls, method, newm)

def _OverrideClassMethod(handler, cls, method):
    orig = getattr(cls, method)
    newm = classmethod(lambda *a, **k: handler(orig, *a, **k))
    _override(cls, method, newm)

#####################################################################
# Decorators

def _hook_decorator(func):
    def decorator1(*a, **k):
        def decorator2(handler):
            func(handler, *a, **k)
        return decorator2
    return decorator1

def _getRanges(turret, gun, nation, vclass):
    visionRadius = firingRadius = artyRadius = 0
    gunsInfoPath = _VEHICLE_TYPE_XML_PATH + nation + '/components/guns.xml/shared/'
    CONST_45_IN_RADIANS = radians(45)

    # Turret-dependent
    visionRadius = int(turret.circularVisionRadius)  # 240..420

    # Gun-dependent
    shots = gun.shots
    for shot in shots:
        radius = int(shot.maxDistance)
        if firingRadius < radius:
            firingRadius = radius  # 10000, 720, 395, 360, 350

        if vclass == 'SPG' and shot.shell.kind == 'HIGH_EXPLOSIVE':
            try:    # faster way
                pitchLimit_rad = min(CONST_45_IN_RADIANS, -calcPitchLimitsFromDesc(0, gun.pitchLimits)[0])
            except Exception: # old way
                minPitch = radians(-45)
                for _gun in turret.guns:
                    if _gun.name == gun.name:
                        minPitch = _gun.pitchLimits['minPitch'][0][1]
                        break
                pitchLimit_rad = min(CONST_45_IN_RADIANS, -minPitch)  # -35..-65
            radius = int(pow(shot.speed, 2) * sin(2 * pitchLimit_rad) / shot.gravity)
            if artyRadius < radius:
                artyRadius = radius  # 485..1469

    return (visionRadius, firingRadius, artyRadius)

# XVM
registerEvent = _hook_decorator(_RegisterEvent)
overrideMethod = _hook_decorator(_OverrideMethod)
overrideStaticMethod = _hook_decorator(_OverrideStaticMethod)
overrideClassMethod = _hook_decorator(_OverrideClassMethod)

