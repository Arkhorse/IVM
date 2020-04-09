# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/armagomen_battle_observer/__init__.py
# Compiled at: 2020-03-18 02:19:52
from .main import mod_ivm

def init():
    if mod_battleObserver.isLoading:
        mod_battleObserver.start()


def fini():
    if mod_battleObserver.isLoading:
        mod_battleObserver.fini()
