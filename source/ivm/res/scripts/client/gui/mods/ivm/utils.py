from .Core import CORE
import userprefs

import BigWorld
import Vehicle
from gui import game_control
from gui.battle_control import avatar_getter
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


def getAccountDBID():
    accountDBID = getCurrentAccountDBID() if not isReplay() else None
    if accountDBID is None:
        accountDBID = userprefs.get('tokens/lastAccountDBID')
    return accountDBID
