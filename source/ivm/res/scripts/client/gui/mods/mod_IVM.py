import os

from account import PlayerAccount
from gui.mods.ivm.Core import CORE
from gui.mods.ivm.fixes import *

# CORE.printLoadMessage('IVM', '       ', buildDate='July 12th, 2020')

if CORE.debug:
    import platform
    print '%s Debug info:\nCurrent OS Version is %s.\nCurrent mod build version is %s\nCurrent game version is %s.' % (CORE.ModIDShort, platform.version, CORE.Version[1], CORE.gameVersion)

garage = True
sound = True
battle = True
annoyingFeatures = True

try:
    from gui.mods.ivm.ivmGarage import *
    print CORE.ModIDShort, 'Garage Module Found'
except ImportError:
    garage = False
    print CORE.ModIDShort, 'Garage Module Not Found'
    pass

try:
    from gui.mods.ivm.battle import *
    print CORE.ModIDShort, 'Battle Module Found'
except ImportError:
    battle = False
    print CORE.ModIDShort, 'Battle Module Not Found'
    pass

# try:
from gui.mods.ivm.soundModule import ivmSound, ivm_setFireInVehicle, ivm_stunSound, ivm_getShells
#     print CORE.ModIDShort, 'Sound Module Found'
# except ImportError:
#     sound = False
#     print CORE.ModIDShort, 'Sound Module Not Found'
#     pass

try:
    from gui.mods.ivm.annoyingFeaturesRemoval import *
    print CORE.ModIDShort, 'Annoying Features Module Found'
except ImportError:
    annoyingFeatures = False
    print CORE.ModIDShort, 'Annoying Features Module Not Found'
    pass

#try:
#    from .ivm.credits import *
#    print CORE.ModIDShort, 'Credits Found'
#except ImportError:
#    print CORE.ModIDShort, 'Credits Not Found!'
#    pass

from time import sleep

if not garage or not sound or not battle or not annoyingFeatures:
    #CORE.addSystemMessage_Error('IVM Failed to load')
    print CORE.ModIDShort, 'Modules Not Found, Redownload Mod'
else:
    #CORE.addSystemMessage_GameGreeting('[IVM] Loaded. Have fun. Don\'t get artied')
    print CORE.ModIDShort, 'Loaded', 'Version', CORE.Version[1]

#if CORE.debug:
    #CORE.addSystemMessage_GameGreeting('Debug Info:\nGarage = %s\nSound= %s\nBattle = %s' % (garage, sound, battle))
    