import BigWorld
# Disable destroyed messages imports
from constants import ARENA_GUI_TYPE
from Vehicle import Vehicle
from gui.Scaleform.daapi.view.battle.shared.battle_timers import PreBattleTimer
from constants import VEHICLE_SETTING
from gui.Scaleform.daapi.view.lobby.techtree.techtree_dp import _TechTreeDataProvider
from gui.Scaleform.daapi.view.meta.ModuleInfoMeta import ModuleInfoMeta
from helpers import dependency
from skeletons.gui.shared import IItemsCache
import traceback
from xml.etree import ElementTree as ET

from .Core import overrideMethod, registerEvent, _getRanges, CORE
from PYmodsCore import PYmodsConfigInterface

class ivmBattle(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmBattle'
        self.version = CORE.Version
        self.modsGroups = 'IVM'
        self.modSettingsID = 'BattleUI'
        self.currentFPS = CORE.MaxFPS
        self.data = {'enabled': True, 
        'enableAutoSpeed': False
        }#, 'setMaxFPS': self.currentFPS}
        super(ivmBattle, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                # 'UI_setting_hideHelpScreen_text': '',
                # 'UI_setting_hideHelpScreen_tooltip': ''
                'name': 'Battle Options',
                'UI_setting_enableAutoSpeed_text': 'Start Battle In Speed Mode For Wheeled \"Tanks\".',
                'UI_setting_enableAutoSpeed_tooltip': 'Always start in the speed mode for wheeled tanks with this.',
                #'UI_setting_setMaxFPS_text': 'Max Framerate',
                #'UI_setting_setMaxFPS_tooltip': 'This will allow you to set your max framerate. This is something alot of people want. The default is 1000, or unlimited.'
            }
    
    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('enableAutoSpeed')]#, self.tb.createControl('setMaxFPS', self.tb.types.TextInput, 80)]
        }
    
    def onApplySettings(self, settings):
        super(ivmBattle, self).onApplySettings(settings)
        pass

c1 = ivmBattle()

isWheeledTech = False
@registerEvent(Vehicle, 'onEnterWorld')
def Vehicle_onEnterWorld(self, prereqs):
    if not c1.data['enableAutoSpeed']:
        return
    global isWheeledTech
    if self.isPlayerVehicle:
        isWheeledTech = self.isWheeledTech and self.typeDescriptor.hasSiegeMode
        if isWheeledTech:
            arenaPeriod = BigWorld.player().guiSessionProvider.shared.arenaPeriod
            startBattle = arenaPeriod.getPeriod() if arenaPeriod is not None else 0
            if startBattle >= 3:
                BigWorld.player().enableOwnVehicleAutorotation(True)

@registerEvent(PreBattleTimer, 'hideCountdown')
def hideCountdown(self, state, speed):
    if not c1.data['enableAutoSpeed']:
        return
    if state == 3 and isWheeledTech:
        BigWorld.player().base.vehicle_changeSetting(VEHICLE_SETTING.SIEGE_MODE_ENABLED, True)

# add shooting range in gun info window for SPG/machine guns
@overrideMethod(ModuleInfoMeta, 'as_setModuleInfoS')
def ModuleInfoWindow_as_setModuleInfoS(base, self, moduleInfo):
    try:
        if moduleInfo['type'] == 'vehicleGun':
            veh_id = self._ModuleInfoWindow__vehicleDescr.type.compactDescr
            itemsCache = dependency.instance(IItemsCache)
            vehicle = itemsCache.items.getItemByCD(veh_id)
            gun = itemsCache.items.getItemByCD(self.moduleCompactDescr).descriptor
            turret = self._ModuleInfoWindow__vehicleDescr.turret    # not accurate, but not relevant here
            (viewRange, shellRadius, artiRadius) = _getRanges(turret, gun, vehicle.nationName, vehicle.type)
            if vehicle.type == 'SPG':   # arti
                moduleInfo['parameters']['params'].append({'type': '<h>' + 'shootingRadius' + ' <p>' +'(m)' + '</p></h>', 'value': '<h>' + str(artiRadius) + '</h>'})
            elif shellRadius < 707:     # not arti, short range weapons
                moduleInfo['parameters']['params'].append({'type': '<h>' + 'shootingRadius' + ' <p>' + '(m)' + '</p></h>', 'value': '<h>' + str(shellRadius) + '</h>'})
    except Exception, ex:
        print(traceback.format_exc())
    return base(self, moduleInfo)

# def ivmMaxFPS():
    #tree = ET.parse(CORE.engineXML)
    #root = tree.getroot()
#
#    if CORE.debug:
#        print '%s setting maxFPS to %s' % (CORE.ModIDShort, setMaxFPS)
#
#    tree.find('renderer/maxFrameRate').text = setMaxFPS
#    tree.write(CORE.engineXML)

#ivmMaxFPS()