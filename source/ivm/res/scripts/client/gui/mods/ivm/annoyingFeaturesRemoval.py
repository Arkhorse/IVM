from .Core import overrideMethod, registerEvent, _getRanges, CORE
from PYmodsCore import PYmodsConfigInterface

class annoyingFeatureRemoval(PYmodsConfigInterface):

    def init(self):
        self.ID = 'annoyingFeatureRemoval'
        self.version = CORE.Version[1]
        self.data = {
            'enabled': True,
            'hideAll': False,
            'hideQuestHint': False,
            'notShowBattleMessage': False, 
            'hideTrajectoryView': False,
            'hideSiegeIndicator': False,
            'hideHelpScreen': False,
            'hideReferalButton': False,
            'hideGeneralChat': False,
            'hidePromoVehicle': False,
            'hideCombatIntel': False,
            'hideCombatIntelCount': False,
            'hidePiggyBankWindow': False,
            'hideRankedResults': False,
            'hideSessionStatsButton': False,
            'hideBattleCount': False,
            'hideDailyQuestWidget': False,
            'hideTenYearsBanner': False,
            'hideBattleCommunication': False,
            'hideProgressiveDecalsWindow': False,
            'Translator': 'The Illusion'
        }
        super(annoyingFeatureRemoval, self).init()

    # 'UI_setting__text': '',
    # 'UI_setting__tooltip': ''

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                'name': 'Annoying Features Removal',
                'UI_setting_translator_text': 'The Illusion',
                'UI_setting_battleOptions_text': 'Battle Options',
                'UI_setting_battleOptions_tooltip': '',
                'UI_setting_hangerOptions_text': 'Hanger Options',
                'UI_setting_hangerOptions_tooltip': 'Or Garage for some of you.',
                'UI_setting_hideAll_text': 'Hide All Annoying Features',
                'UI_setting_hideAll_tooltip': 'Checking this will turn off all the annoying features, you will not need to check the others.',
                'UI_setting_hideQuestHint_text': 'Hide Mission Popup.',
                'UI_setting_hideQuestHint_tooltip': 'This will disable the mission popup at the start of battle.',
                'UI_setting_notShowBattleMessage_text': 'Hide Destroyed Tanks Message.',
                'UI_setting_notShowBattleMessage_tooltip': 'This will disable the messages for destroyed tanks above the minimap.',
                'UI_setting_hideTrajectoryView_text': 'Hide Arty Trajectory View',
                'UI_setting_hideTrajectoryView_tooltip': '',
                'UI_setting_hideSiegeIndicator_text': 'Hide Siegemode Indicator',
                'UI_setting_hideSiegeIndicator_tooltip': '',
                'UI_setting_hideHelpScreen_text': 'Hide Help Screen',
                'UI_setting_hideHelpScreen_tooltip': '',
                'UI_setting_hideReferalButton_text': 'Hide Referal Button',
                'UI_setting_hideReferalButton_tooltip': '',
                'UI_setting_hideGeneralChat_text': 'Hide General Chat Button',
                'UI_setting_hideGeneralChat_tooltip': 'Finally! No more idiots!',
                'UI_setting_hideRankedResults_text': 'Hide Ranked Results',
                'UI_setting_hideRankedResults_tooltop': '',
                'UI_setting_sessionStats_text': 'Session Stats Options',
                'UI_setting_sessionStats_tooltip': '',
                'UI_setting_hideSessionStatsButton_text': 'Hide Button',
                'UI_setting_hideSessionStatsButton_tooltip': '',
                'UI_setting_hideBattleCount_text': 'Hide Battle Count',
                'UI_setting_hideBattleCount_tooltip': '',
                'UI_setting_hideDailyQuestWidget_text': 'Hide Daily Quest',
                'UI_setting_hideDailyQuestWidget_tooltip': '',
                'UI_setting_hideTenYearsBanner_text': 'Hide 10 Years Banner',
                'UI_setting_hideTenYearsBanner_tooltip': '',
                'UI_setting_hidePromoVehicle_text': 'Hide Promo Vehicle',
                'UI_setting_hidePromoVehicle_tooltip': '',
                'UI_setting_hideCombatIntel_text': 'Hide Adverts',
                'UI_setting_hideCombatIntel_tooltip': '',
                'UI_setting_hideCombatIntelCount_text': 'Hide Advert Count',
                'UI_setting_hideCombatIntelCount_tooltip': '',
                'UI_setting_hidePiggyBankWindow_text': 'Hide Piggy Bank',
                'UI_setting_hidePiggyBankWindow_tooltip': 'Why would you want to do this? Free money...',
                'UI_setting_tempOptions_text': 'Temporary Options',
                'UI_setting_hideBattleCommunication_text': 'Hide The Hint About The New Battle Communication',
                'UI_setting_hideBattleCommunication_tooltip': '',
                'UI_setting_hideProgressiveDecalsWindow_text': 'Hide Info Windows When Receiving Progressive Decals',
                'UI_setting_hideProgressiveDecalsWindow_tooltip': ''
            }
        if self.lang == 'ru':
            self.i18n = {
                'name': 'Удаление надоедливых опций',
                'UI_setting_translator_text': 'DrWeb7_1',
                'UI_setting_battleOptions_text': 'Battle Options',
                'UI_setting_battleOptions_tooltip': '',
                'UI_setting_hangerOptions_text': 'Hanger Options',
                'UI_setting_hangerOptions_tooltip': 'Or Garage for some of you.',
                'UI_setting_hideQuestHint_text': 'Не показывать активную миссию',
                'UI_setting_hideQuestHint_tooltip': 'Это отключит показ выбранной ЛБЗ в начале боя.',
                'UI_setting_notShowBattleMessage_text': 'Не показывать уведомления об уничтожении техники',
                'UI_setting_notShowBattleMessage_tooltip': 'Это отключит показ сообщений об уничтожении танка над миникартой.',
                'UI_setting_hideTrajectoryView_text': 'Не показывать указку САУ',
                'UI_setting_hideTrajectoryView_tooltip': '',
                'UI_setting_hideSiegeIndicator_text': 'Не показывать индикатор осадного-походного режима',
                'UI_setting_hideSiegeIndicator_tooltip': '',
                'UI_setting_hideHelpScreen_text': 'Не показывать экран помощи',
                'UI_setting_hideHelpScreen_tooltip': '',
                'UI_setting_hideReferalButton_text': 'Hide Referal Button',
                'UI_setting_hideReferalButton_tooltip': '',
                'UI_setting_hideGeneralChat_text': 'Hide General Chat Button',
                'UI_setting_hideGeneralChat_tooltip': 'Finally! No more idiots!',
                'UI_setting_hideBattleCommunication_text': 'Hide The Hint About The New Battle Communication.',
                'UI_setting_hideBattleCommunication_tooltip': '',
                'UI_setting_hideProgressiveDecalsWindow_text': 'Hide Info Windows When Receiving Progressive Decals',
                'UI_setting_hideProgressiveDecalsWindow_tooltip': ''
            }
        if self.lang == 'es':
            self.i18n = {
                'name': 'Eliminación de características molestas',
                'UI_setting_translator_text': 'LordFelix',
                'UI_setting_battleOptions_text': 'Battle Options',
                'UI_setting_battleOptions_tooltip': '',
                'UI_setting_hangerOptions_text': 'Hanger Options',
                'UI_setting_hangerOptions_tooltip': 'Or Garage for some of you.',
                'UI_setting_hideQuestHint_text': 'Ocultar pop-up de misiones',
                'UI_setting_hideQuestHint_tooltip': 'Deshabilita el pop-up de misiones al inicio de la batalla',
                'UI_setting_notShowBattleMessage_text': 'Ocultar mensajes de destrucción',
                'UI_setting_notShowBattleMessage_tooltip': 'Deshabilita los mensajes sobre el minimapa cuando un tanque es destruido',
                'UI_setting_hideTrajectoryView_text': 'Ocultar vista de trayectoria de artillería',
                'UI_setting_hideTrajectoryView_tooltip': '',
                'UI_setting_hideSiegeIndicator_text': 'Ocultar indicador de modo asedio',
                'UI_setting_hideSiegeIndicator_tooltip': '',
                'UI_setting_hideHelpScreen_text': 'Ocultar pantalla de ayuda',
                'UI_setting_hideHelpScreen_tooltip': '',
                'UI_setting_hideReferalButton_text': 'Hide Referal Button',
                'UI_setting_hideReferalButton_tooltip': '',
                'UI_setting_hideGeneralChat_text': 'Hide General Chat Button',
                'UI_setting_hideGeneralChat_tooltip': 'Finally! No more idiots!',
                'UI_setting_hideBattleCommunication_text': 'Hide The Hint About The New Battle Communication.',
                'UI_setting_hideBattleCommunication_tooltip': '',
                'UI_setting_hideProgressiveDecalsWindow_text': 'Hide Info Windows When Receiving Progressive Decals',
                'UI_setting_hideProgressiveDecalsWindow_tooltip': ''
            }

    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [
                #self.tb.createLabel('UI_setting_translator_text'),
                self.tb.createControl('hideAll'),
                self.tb.createLabel('battleOptions'),
                self.tb.createControl('hideTrajectoryView'), 
                self.tb.createControl('hideQuestHint'), 
                self.tb.createControl('hideHelpScreen'),
                self.tb.createControl('hideSiegeIndicator'), 
                self.tb.createControl('notShowBattleMessage'),
                self.tb.createControl('hideBattleCommunication'),
                self.tb.createLabel('sessionStats'),
                self.tb.createControl('hideSessionStatsButton'),
                self.tb.createControl('hideBattleCount'),
                self.tb.createLabel('tempOptions'),
                self.tb.createControl('hideTenYearsBanner')
                ],
            'column2': [
                self.tb.createLabel('hangerOptions'),
                self.tb.createControl('hideReferalButton'),
                self.tb.createControl('hideGeneralChat'),
                self.tb.createControl('hidePromoVehicle'),
                self.tb.createControl('hideCombatIntel'),
                self.tb.createControl('hideCombatIntelCount'),
                self.tb.createControl('hidePiggyBankWindow'),
                self.tb.createControl('hideRankedResults'),
                self.tb.createControl('hideDailyQuestWidget'),
                self.tb.createControl('hideProgressiveDecalsWindow')
                ]
        }

    def onApplySettings(self, settings):
        super(annoyingFeatureRemoval, self).onApplySettings(settings)
        pass

c2 = annoyingFeatureRemoval()

#######################################################################
# Annoying Features Remover

# Imports
from helpers import dependency
from HeroTank import HeroTank

from gui.game_control.AwardController import PiggyBankOpenHandler
from gui.game_control.PromoController import PromoController

from messenger.gui.Scaleform.lobby_entry import LobbyEntry
from gui.Scaleform.genConsts.HANGAR_ALIASES import HANGAR_ALIASES
from gui.Scaleform.daapi.view.meta.MessengerBarMeta import MessengerBarMeta
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.Scaleform.daapi.view.lobby.hangar.daily_quest_widget import DailyQuestWidget
from gui.Scaleform.daapi.view.lobby.messengerBar.messenger_bar import MessengerBar
from gui.Scaleform.daapi.view.lobby.messengerBar.session_stats_button import SessionStatsButton
from gui.Scaleform.daapi.view.lobby.rankedBattles.ranked_battles_results import RankedBattlesResults

from gui.Scaleform.daapi.view.battle.shared.hint_panel.plugins import TrajectoryViewHintPlugin, SiegeIndicatorHintPlugin, PreBattleHintPlugin
from gui.Scaleform.daapi.view.battle.shared.messages.fading_messages import FadingMessages

from gui.promo.hangar_teaser_widget import TeaserViewer
from gui.game_control.AwardController import ProgressiveItemsRewardHandler

from skeletons.account_helpers.settings_core import ISettingsCore
from vehicle_systems.tankStructure import ModelStates

# Handlers

# Hanger

@overrideMethod(LobbyEntry, '_LobbyEntry__handleLazyChannelCtlInited')
def handleLazyChannelCtlInited(base, self, event):
    if c2.data['hideGeneralChat'] or c2.data['hideAll']:
        ctx = event.ctx
        controller = ctx.get('controller')
        if controller is None:
            print('Controller is not defined', ctx)
            return
        else:
            ctx.clear()
            return
    return base(self, event)

@overrideMethod(HeroTank, 'recreateVehicle')
def recreateVehicle(base, self, typeDescriptor=None, state=ModelStates.UNDAMAGED, callback=None):
    if c2.data['hidePromoVehicle'] or c2.data['hideAll']:
        return
    base(self, typeDescriptor, state, callback)

@overrideMethod(TeaserViewer, 'show')
def show(base, self, teaserData, promoCount):
    if c2.data['hideCombatIntel'] or c2.data['hideAll']:
        return
    base(self, teaserData, promoCount)
@overrideMethod(PromoController, 'getPromoCount')
def getPromoCount(base, self):
    if c2.data['hideCombatIntelCount'] or c2.data['hideAll']:
        return
    base(self)

@overrideMethod(PiggyBankOpenHandler, '_showAward')
def _showAward(base, self, ctx):
    if c2.data['hidePiggyBankWindow'] or c2.data['hideAll']:
        return
    base(self, ctx)

@overrideMethod(RankedBattlesResults, '_populate')
def _populate(base, self):
    if c2.data['hideRankedResults'] or c2.data['hideAll']:
        return
    base(self)

@overrideMethod(MessengerBar, '_MessengerBar__updateSessionStatsBtn')
def updateSessionStatsBtn(base, self):
    if c2.data['hideSessionStatsButton'] or c2.data['hideAll']:
        self.as_setSessionStatsButtonVisibleS(False)
        self._MessengerBar__onSessionStatsBtnOnlyOnceHintHidden(True) # hide display session statistics help hints
        return
    base(self)


@overrideMethod(SessionStatsButton, '_SessionStatsButton__updateBatteleCount')
def updateBatteleCount(base, self):
    if c2.data['hideBattleCount'] or c2.data['hideAll']:
        return
    base(self)


@overrideMethod(DailyQuestWidget, '_DailyQuestWidget__shouldHide')
def shouldHide(base, self):
    if c2.data['hideDailyQuestWidget'] or c2.data['hideAll']:
        return True
    base(self)

@overrideMethod(Hangar, '_Hangar__updateTenYearsCountdownEntryPointVisibility')
def updateTenYearsCountdownEntryPointVisibility(base, self):
    if c2.data['hideTenYearsBanner'] or c2.data['hideAll']:
        self.as_updateEventEntryPointS(HANGAR_ALIASES.TEN_YEARS_COUNTDOWN_ENTRY_POINT_INJECT, False)
        return
    base(self)

# hide display pop-up window when receiving progressive decals
@overrideMethod(ProgressiveItemsRewardHandler, '_showAward')
def _showAward(base, self, ctx):
    if c2.data['hideProgressiveDecalsWindow'] or c2.data['hideAll']:
        return
    base(self, ctx)

# Battle

# https://gitlab.com/xvm/xvm/-/blob/master/src/xpm/xvm_battle/battle.py
@overrideMethod(TrajectoryViewHintPlugin, '_TrajectoryViewHintPlugin__addHint')
def addHint(base, self):
    if c2.data['hideTrajectoryView'] or c2.data['hideAll']:
        return
    base(self)

@overrideMethod(SiegeIndicatorHintPlugin, '_SiegeIndicatorHintPlugin__updateHint')
def updateHint(base, self):
    if c2.data['hideSiegeIndicator'] or c2.data['hideAll']:
        return
    base(self)

@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayQuestHint')
def canDisplayQuestHint(base, self):
    if c2.data['hideQuestHint'] or c2.data['hideAll']:
        return False
    base(self)

@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayHelpHint')
def canDisplayHelpHint(base, self, typeDescriptor):
    if c2.data['hideHelpScreen'] or c2.data['hideAll']:
        return False
    base(self, typeDescriptor)

@overrideMethod(FadingMessages, 'showMessage')
def FadingMessages_showMessage(base, self, key, args=None, extra=None, postfix=''):
    if not c2.data['notShowBattleMessage'] or not c2.data['hideAll'] or CORE.FrontlineBattleType:
        return base(self, key, args=None, extra=None, postfix='')
    pass

@overrideMethod(MessengerBarMeta, 'as_setInitDataS')
def MessengerBarMeta_as_setInitDataS(base, self, data):
    if c2.data['hideReferalButton'] or c2.data['hideAll'] and 'isReferralEnabled' in data:
        data['isReferralEnabled'] = False
    return base(self, data)

@overrideMethod(PreBattleHintPlugin, '_PreBattleHintPlugin__canDisplayBattleCommunicationHint')
def canDisplayBattleCommunicationHint(base, self):
    if c2.data['hideBattleCommunication'] or c2.data['hideAll']:
        return False
    base(self)

#######################################################################
