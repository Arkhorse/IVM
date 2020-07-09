from .Core import overrideMethod, CORE
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta
from gui.Scaleform.daapi.view.lobby.messengerBar.NotificationListButton import NotificationListButton

from debug_utils import LOG_CURRENT_EXCEPTION

try:
    from PYmodsCore import PYmodsConfigInterface
except ImportError:
    print ModIDShort, 'Ingame UI not found, passing'
    pass

class ivmGarage(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmGarage'
        self.version = CORE.Version[1]
        self.modsGroups = 'IVM'
        self.data = {
            'enabled': True, 
            'carEnabled': True, 
            'carRows': 2, 
            'ivmUnanonymizer': False, 
            'removeBadges': False, 
            'showTenYearsBanner': True, 
            'notificationBlinking': True, 
            'showCustomizationCounter': True,
            'notificationCounter': True
            } 
        super(ivmGarage, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                # 'UI_setting__text': '',
                # 'UI_setting__tooltip': ''
                'name': 'Garage Options',
                'UI_setting_carEnabled_text': 'Enable the carousel rows option',
                'UI_settings_carEnabled_tooltip': '',
                'UI_setting_carRows_text': 'Choose how many carousel rows you want',
                'UI_setting_carRows_tooltip': 'To apply this, you MUST reload the game.',
                'UI_setting_ivmUnanonymizer_text': 'Enable Unanonymizer',
                'UI_setting_ivmUnanonymizer_tooltip': 'This will remove a players fake name, and show thier real IGN on the battle results.',
                'UI_setting_removeBadges_text': 'Remove Badges',
                'UI_setting_removeBadges_tooltip': 'This requires Unanonymizer.',
                'UI_setting_notificationBlinking_text': 'Notification Status',
                'UI_setting_notificationBlinking_tooltip': 'Uncheck this if you dont want blinking notifications'
                }

    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('carEnabled'), self.tb.createControl('ivmUnanonymizer'), self.tb.createControl('notificationBlinking')],
            'column2': [self.tb.createSlider('carRows', vMin=0, vMax=12, value=2, formatStr='{{value}}', width=200, step=1, empty=False), self.tb.createControl('removeBadges')]
        }

config = ivmGarage()
carEnabled = config.data['carEnabled']
carRows = config.data['carRows']
ivmUnanonymizer = config.data['ivmUnanonymizer']
removeBadges = config.data['removeBadges']
notificationBlinking = config.data['notificationBlinking']

@overrideMethod(NotificationListButton, 'as_setStateS')
def ivmNotificationButtonState(base, self, isBlinking, counterValue):
    # https://gitlab.com/xvm/xvm/-/blob/master/src/xpm/xvm_hangar/svcmsg.py
    if not notificationBlinking:
        isBlinking = False
        counterValue = ''
    else:
        base(self, isBlinking, counterValue)

@overrideMethod(TankCarouselMeta, 'as_rowCountS')
def ivmCarouselS(base, self, value):
    if not carEnabled:
        print '[IVM] Carousels Not Enabled'
        return base(self, value)
    print '[IVM] Carousels Enabled with %s Rows' % (carRows)
    return self.flashObject.as_rowCount(carRows) if self._isDAAPIInited() else None
#TankCarouselMeta.as_rowCountS = ivmCarouselS
#override(TankCarouselMeta, 'as_rowCountS', ivmCarouselS)

from gui.battle_results.service import BattleResultsService
# Pre release testing
approved = False
finished = False

class Unanonymizer(object):
    def __init__(self):
        self.macros            = ['{{clan}}', '{{fakeName}}', '{{realName}}']
        self.macrosNb          = 3
        self.defaultConfig     = {"enable":True,"debug":False,"playerNameFormat":"<img src='img://gui/maps/icons/library/icon_eye.png'/>{{fakeName}}","fakePlayerDetailsHeaderFormat":"Fake player name","fakePlayerDetailsValuesFormat":"{{fakeName}}","realPlayerDetailsHeaderFormat":"Real player name","realPlayerDetailsValuesFormat":"{{realName}}","removeBadges": True}

ua = Unanonymizer

@overrideMethod(BattleResultsService, 'getResultsVO')
def ivmUAVO(base, self, arenaUniqueID):
    if not ivmUnanonymizer or not approved or not finished:
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
