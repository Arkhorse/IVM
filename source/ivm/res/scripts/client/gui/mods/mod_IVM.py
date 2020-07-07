import os


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