import os
from gui import SystemMessages

__all__ = ('Author', 'Version', 'ModIDShort')
Author = 'The Illusion'
Credits = 'RaJCel'
Version = ['Rel 0 ', 'Patch 0.02']
Status = 'Dev'
debug = True
ModIDInternal = 'mod_ivm'
ModIDShort = 'IVM'
ModIDLong = 'Improved Visuals and Sounds'
DIR = os.path.join('mods', 'configs', 'ivm')
FILE = DIR, 'ivm.json'
downloadURL = ''

print ModIDShort, 'Loading', Version[0]

def getOSVersion():
    # Needed for Support. If the OSReadable is less than Windows 7, No support will be given.
    import platform
    OSPlatform = platform.system()
    OSReadable = platform.release()
    OSVersion = platform.version()
    print OSPlatform, OSReadable, OSVersion 

getOSVersion()

garage = True
sound = True
battle = True

try:
    from .ivm.ivmGarage import *
    print ModIDShort, 'Garage Module Found'
except ImportError:
    garage = False
    print ModIDShort, 'Garage Module Not Found'
    pass

try:
    from .ivm.sound import *
    print ModIDShort, 'Sound Module Found'
except ImportError:
    sound = False
    print ModIDShort, 'Sound Module Not Found'
    pass

try:
    from .ivm.battle import *
    print ModIDShort, 'Battle Module Found'
except ImportError:
    battle = False
    print ModIDShort, 'Battle Module Not Found'
    pass

if not garage or not sound or not battle:
    SystemMessages.pushMessage(text='[IVM] Modules not found. Redownload Mod', type=SystemMessages.SM_TYPE.Error)
    print ModIDShort, 'Modules Not Found, Redownload Mod @ %s' % (downloadURL)
else:
    SystemMessages.pushMessage(text='[IVM] Loaded. Have fun. Don\'t get artied', type=SystemMessages.SM_TYPE.Information)
    print ModIDShort, 'Loaded', 'Version', Version[1]