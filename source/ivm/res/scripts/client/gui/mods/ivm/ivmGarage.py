from .Core import overrideMethod, CORE
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta
from gui.Scaleform.daapi.view.lobby.messengerBar.NotificationListButton import NotificationListButton

from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from gui.Scaleform.daapi.view.lobby.hangar.ammunition_panel import AmmunitionPanel
from gui.Scaleform.daapi.view.lobby.customization.customization_bottom_panel import CustomizationBottomPanel

from gui.Scaleform.genConsts.HANGAR_ALIASES import HANGAR_ALIASES
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar

from messenger.proto.xmpp.xmpp_constants import CONTACT_LIMIT

try:
    from PYmodsCore import PYmodsConfigInterface
except ImportError:
    print ModIDShort, 'Ingame UI not found, passing'
    pass

class ivmGarage(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmGarage'
        self.version = CORE.Version[1]
        self.carouselRows = 2
        self.data = {
            'enabled': True, 
            'carEnabled': False, 
            'carRows': 2, 
            'ivmUnanonymizer': False, 
            'removeBadges': False, 
            'showTenYearsBanner': True, 
            'notificationBlinking': True, 
            'showCustomizationCounter': True,
            'notificationCounter': True,
            'extendedRoster': False,
            'rosterCount': 5000,
            'blackListCount': 10000,
            'extendedTooltips': False,
            'extendedTooltips_MAXLIST_Module': 1000,
            'extendedTooltips_MAXLIST_Booster': 1000
            } 
        super(ivmGarage, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                # 'UI_setting__text': '',
                # 'UI_setting__tooltip': ''
                'name': 'Garage Options',
                'UI_setting_garageLabel1_text': 'Note: All settings require a full game reload to apply',
                'UI_setting_garageLabel1_tooltip': 'This is due to coding limitations at this time.',
                'UI_setting_carEnabled_text': 'Enable the carousel rows option',
                'UI_setting_carEnabled_tooltip': '',
                'UI_setting_carRows_text': 'Choose how many carousel rows you want',
                'UI_setting_carRows_tooltip': 'To apply this, you MUST reload the game.',
                'UI_setting_anonHeader_text': 'Anonymizer Options',
                'UI_setting_anonHeader_tooltip': '',
                'UI_setting_ivmUnanonymizer_text': 'Enable Unanonymizer',
                'UI_setting_ivmUnanonymizer_tooltip': 'This will remove a players fake name, and show thier real IGN on the battle results.',
                'UI_setting_removeBadges_text': 'Remove Badges',
                'UI_setting_removeBadges_tooltip': 'This requires Unanonymizer.',
                'UI_setting_notificationBlinking_text': 'Notification Status',
                'UI_setting_notificationBlinking_tooltip': 'Turn this to off if you dont want blinking notifications',
                'UI_setting_showTenYearsBanner_text': 'Show 10 Years Banner',
                'UI_setting_showTenYearsBanner_tooltip': 'Annoyed by the 10 years banner? Turn it off!',
                'UI_setting_notificationCounter_text': 'Enable Notification Counter Options',
                'UI_setting_notificationCounter_tooltip': '',
                'UI_setting_showCustomizationCounter_text': 'Show Notification Counters',
                'UI_setting_showCustomizationCounter_tooltip': 'Show notifications counters in some areas and on the button \"Exterior\".',
                'UI_setting_updateCodeName_text': '%s Update' % (CORE.updateCodeName),
                'UI_setting_updateCodeName_tooltip': '',
                'UI_setting_rosterHeader_text': 'Extended Roster Options',
                'UI_setting_rosterHeader_tooltip': 'Max Friends and Max Blacklisted',
                'UI_setting_extendedRoster_text': 'Enable',
                'UI_setting_extendedRoster_tooltip': '',
                'UI_setting_rosterCount_text': 'Friend Count',
                'UI_setting_rosterCount_tooltip': '',
                'UI_setting_blackListCount_text': 'Blacklist Count',
                'UI_setting_blackListCount_tooltip': '',
                'UI_setting_extendedTooltipsLabel_text': 'Extended Tooltips',
                'UI_setting_extendedTooltipsLabel_tooltip': '',
                'UI_setting_extendedTooltips_text': 'Enable',
                'UI_setting_extendedTooltips_tooltip': '',
                'UI_setting_extendedTooltips_MAXLIST_Module_text': 'Maximum Modules',
                'UI_setting_extendedTooltips_MAXLIST_Module_tooltip': 'This is for the modules. What most people use this mod for. Higher = More modules shown in the tooltip.',
                'UI_setting_extendedTooltips_MAXLIST_Booster_text': 'Maximum Boosters',
                'UI_setting_extendedTooltips_MAXLIST_Booster_tooltip': 'This will increase the shown boosters.'
                }

    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [
                self.tb.createLabel('updateCodeName'),
                self.tb.createLabel('garageLabel1'),
                self.tb.createControl('carEnabled'),
                self.tb.createSlider('carRows', vMin=0, vMax=12, value=2, formatStr='{{value}}', width=200, step=1, empty=False),
                self.tb.createControl('notificationCounter'),
                self.tb.createControl('showCustomizationCounter'),
                self.tb.createControl('notificationBlinking')
                ],
            'column2': [
                self.tb.createLabel('anonHeader'),
                self.tb.createControl('ivmUnanonymizer'),
                self.tb.createControl('removeBadges'),
                self.tb.createLabel('rosterHeader'),
                self.tb.createControl('extendedRoster'),
                self.tb.createControl('rosterCount', self.tb.types.TextInput, 80),
                self.tb.createControl('blackListCount', self.tb.types.TextInput, 80),
                self.tb.createLabel('extendedTooltipsLabel'),
                self.tb.createControl('extendedTooltips'),
                self.tb.createControl('extendedTooltips_MAXLIST_Module', self.tb.types.TextInput, 80),
                self.tb.createControl('extendedTooltips_MAXLIST_Booster', self.tb.types.TextInput, 80)
                ]
        }

    def onApplySettings(self, settings):
        super(ivmGarage, self).onApplySettings(settings)

config = ivmGarage()
carEnabled = config.data['carEnabled']
carRows = config.data['carRows']
ivmUnanonymizer = config.data['ivmUnanonymizer']
removeBadges = config.data['removeBadges']
notificationBlinking = config.data['notificationBlinking']
showTenYearsBanner = config.data['showTenYearsBanner']
showCustomizationCounter = config.data['showCustomizationCounter']
notificationCounter = config.data['notificationCounter']
extendedRoster = config.data['extendedRoster']

if extendedRoster:
    CONTACT_LIMIT.ROSTER_MAX_COUNT = config.data['rosterCount']
    CONTACT_LIMIT.BLOCK_MAX_COUNT = config.data['blackListCount']

# https://gitlab.com/xvm/xvm/-/blob/master/src/xpm/xvm_hangar/svcmsg.py
@overrideMethod(NotificationListButton, 'as_setStateS')
def _NotificationListButton_as_setStateS(base, self, isBlinking, counterValue):
    if not notificationBlinking:
        isBlinking = False
        counterValue = ''
    elif notificationBlinking:
        counterValue = ''
    base(self, isBlinking, counterValue)

# https://gitlab.com/xvm/xvm/-/blob/9322831b9fdd9c74a09587b4206229aee9841ca1/src/xpm/xvm_hangar/counters.py
@overrideMethod(LobbyHeader, '_LobbyHeader__setCounter')
def _LobbyHeader__setCounter(base, self, alias, counter=None):
    if notificationCounter:
        base(self, alias, counter)

# https://gitlab.com/xvm/xvm/-/blob/9322831b9fdd9c74a09587b4206229aee9841ca1/src/xpm/xvm_hangar/counters.py
@overrideMethod(AmmunitionPanel, '_AmmunitionPanel__applyCustomizationNewCounter')
def __applyCustomizationNewCounter(base, self, vehicle):
    if not showCustomizationCounter:
        return self.as_setCustomizationBtnCounterS(0)
    base(self, vehicle)

# https://gitlab.com/xvm/xvm/-/blob/9322831b9fdd9c74a09587b4206229aee9841ca1/src/xpm/xvm_hangar/counters.py
@overrideMethod(CustomizationBottomPanel, '_CustomizationBottomPanel__setNotificationCounters')
def __setNotificationCounters(base, self):
    if not showCustomizationCounter:
        tabsCounters = []
        return self.as_setNotificationCountersS({'tabsCounters': tabsCounters, 'switchersCounter': 0})
    base(self)


@overrideMethod(TankCarouselMeta, 'as_rowCountS')
def ivmCarouselS(base, self, value):
    if not carEnabled or not config.data['enabled']:
        if CORE.debug:
            print '[IVM] Carousels Not Enabled'
        return base(self, value)
    if CORE.debug:
        print '[IVM] Carousels Enabled with %s Rows' % (carRows)
    return self.flashObject.as_rowCount(carRows) if self._isDAAPIInited() else None
#TankCarouselMeta.as_rowCountS = ivmCarouselS
#override(TankCarouselMeta, 'as_rowCountS', ivmCarouselS)

from gui.shared.tooltips.module import ModuleTooltipBlockConstructor
from gui.shared.tooltips import battle_booster
from gui.Scaleform.daapi.view.lobby.storage import storage_helpers

@overrideMethod(storage_helpers, 'createStorageDefVO')
def createStorageDefVO(base, itemID, title, description, count, price, image, imageAlt, itemType='', nationFlagIcon='', enabled=True, contextMenuId=''):
    if not config.data['extendedTooltips'] or not config.data['enabled']:
        base(itemID, title, description, count, price, image, imageAlt, itemType='', nationFlagIcon='', enabled=True, contextMenuId='')
    b = []
    for priced in price['price']:
        b.append((priced[0], priced[1] * count))
    price['price'] = tuple(b)
    return {'id': itemID,
     'title': title,
     'description': description,
     'count': count,
     'price': price,
     'image': image,
     'imageAlt': imageAlt,
     'type': itemType,
     'nationFlagIcon': nationFlagIcon,
     'enabled': enabled,
     'contextMenuId': contextMenuId}

if config.data['extendedTooltips']:
    ModuleTooltipBlockConstructor.MAX_INSTALLED_LIST_LEN = config.data['extendedTooltips_MAXLIST_Module']
    battle_booster._MAX_INSTALLED_LIST_LEN = config.data['extendedTooltips_MAXLIST_Booster']

# ivmUAVO is based on RaJCel code. Really great guy. Go use his mods: https://wgmods.net/search/?owner=219030
from gui.battle_results.service import BattleResultsService
# Pre release testing

class Unanonymizer(object):
    def __init__(self):
        self.macros            = ['{{clan}}', '{{fakeName}}', '{{realName}}']
        self.macrosNb          = 3
        self.defaultConfig     = {"enable":True,"debug":False,"playerNameFormat":"<img src='img://gui/maps/icons/library/icon_eye.png'/>{{fakeName}}","fakePlayerDetailsHeaderFormat":"Fake player name","fakePlayerDetailsValuesFormat":"{{fakeName}}","realPlayerDetailsHeaderFormat":"Real player name","realPlayerDetailsValuesFormat":"{{realName}}","removeBadges": True}

ua = Unanonymizer

@overrideMethod(BattleResultsService, 'getResultsVO')
def ivmUAVO(base, self, arenaUniqueID):
    if not ivmUnanonymizer:
        return base(self, arenaUniqueID)
    vo = BattleResultsService.getResultsVO
    try:
        for player in (vo['team1'] + vo['team2']):
            if not removeBadges: player['badgeVO']['icon'] = ''
            if player['userVO']['fakeName'] != player['userVO']['userName']:
                values = ['[%s]' % player['userVO']['clanAbbrev'] if player['userVO']['clanAbbrev'] <> '' else '', player['userVO']['fakeName'], player['userVO']['userName']]
                player['userVO']['fakeName'] = CORE.applyMacros(ua.defaultConfig('playerNameFormat',{}), ua.macrosNb, ua.macros, values)
                statBlock = {'infoTooltip':'','label':CORE.applyMacros(ua.defaultConfig('realPlayerDetailsHeaderFormat',{}), ua.macrosNb, ua.macros, values),'value':CORE.applyMacros(ua.defaultConfig('realPlayerDetailsValuesFormat',{}), ua.macrosNb, ua.macros, values)}
                player['statValues'][0].insert(0,statBlock)
                player['statValues'][1].insert(0,statBlock)
                statBlock = {'infoTooltip':'','label':CORE.applyMacros(ua.defaultConfig('fakePlayerDetailsHeaderFormat',{}), ua.macrosNb, ua.macros, values),'value':CORE.applyMacros(ua.defaultConfig('fakePlayerDetailsValuesFormat',{}), ua.macrosNb, ua.macros, values)}
                player['statValues'][0].insert(0,statBlock)
                player['statValues'][1].insert(0,statBlock)
    except:
        CORE.addSystemMessage_Error('IVM Failed on ivmUAVO\nThis is the Unanonymizer')
        print CORE.ModIDShort, ' ivmUAVO Issue', LOG_CURRENT_EXCEPTION
    return vo

