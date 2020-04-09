#Global Imports
from json import dump as jsonDump, dumps as jsonDumps, load as jsonLoad
import os
from os import path
from debug_utils import LOG_CURRENT_EXCEPTION

#Game Imports
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta
from gui.Scaleform.daapi.view.battle.shared.destroy_timers_panel import DestroyTimersPanel
from SoundGroups import g_instance as SoundGroups_g_instance

#Ingame Menu
from gui.mods.mod_mods_gui import g_gui, inject

COLORS = ['#FE0E00', '#FE7903', '#F8F400', '#60FF00', '#02C9B3', '#D042F3']
COLOR = ['#0000FF', '#A52A2B', '#D3691E', '#6595EE', '#FCF5C8', '#00FFFF', '#28F09C', '#FFD700', '#008000', '#ADFF2E', '#FF69B5', '#00FF00', '#FFA500', '#FFC0CB', '#800080', '#FF0000', '#8378FC', '#DB0400', '#80D639', '#FFE041', '#FFFF00', '#FA8072', '#FE0E00', '#FE7903', '#F8F400', '#60FF00', '#02C9B3', '#D042F3']
MENU = ['UI_color_blue', 'UI_color_brown', 'UI_color_chocolate', 'UI_color_cornflower_blue', 'UI_color_cream', 'UI_color_cyan', 'UI_color_emerald', 'UI_color_gold', 'UI_color_green', 'UI_color_green_yellow', 'UI_color_hot_pink', 'UI_color_lime',
        'UI_color_orange', 'UI_color_pink', 'UI_color_purple', 'UI_color_red', 'UI_color_wg_blur', 'UI_color_wg_enemy', 'UI_color_wg_friend', 'UI_color_wg_squad', 'UI_color_yellow', 'UI_color_nice_red', 'UI_color_very_bad', 'UI_color_bad', 'UI_color_normal', 'UI_color_good', 'UI_color_very_good', 'UI_color_unique']

__name__ = 'IVM '
__author__ = 'The Illusion '
__copyright__ = 'Copyright 2020, The Illusion'
__credits__ = ['The Illusion, RaJCel']
__maintainer__ = 'The Illusion'
__status__ = 'Dev'
__version__ = '0.1'
_DIR_ = './mods/configs/IVM'
_FILE_ = './mods/configs/IVM/IVM.json'

#print '[IVM] ' + str(__name__) + 'By ' + str(__maintainer__) + ' Version ' + str(__status__), str(__version__)
tankrows = 2

class Config(object):
    def __init__(self):
        self.ids = 'IVM'
        self.version = 'v0.2 (2020-04-08)'
        self.version_id = 0.2
        self.author = 'by The Illusion'
        self.data = {
            'version': self.version_id,
            'enabled': True,
            'fireSoundEnabled': False,
            'stunSoundEnabled': False,
            'carouselsEnabled': False,
            'tankrows': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        }
        self.i18n = {
            'version': self.version_id,
            'UI_ivm_name': 'IVM',
            'UI_description': 'Improved Visuals and Sounds Mod',
            'UI_setting_carouselsEnabled_label': 'Carousels',
            'UI_setting_carouselsEnabled_text': 'Enable Carousel Enhancement',
            'UI_setting_tankrows_text': 'Number of rows',
            'UI_setting_tankrows_label': 'See Label',
            'UI_setting_sounds_label': 'Sound Options',
            'UI_setting_fireSoundEnabled_text': 'Enable Fire Sound',
            'UI_setting_stunSoundEnabled_text': 'Enable Stun Sound',
            'UI_color_blue'                        : 'Blue',
            'UI_color_brown'                       : 'Brown',
            'UI_color_chocolate'                   : 'Chocolate',
            'UI_color_cornflower_blue'             : 'Cornflower Blue',
            'UI_color_cream'                       : 'Cream',
            'UI_color_cyan'                        : 'Cyan',
            'UI_color_emerald'                     : 'Emerald',
            'UI_color_gold'                        : 'Gold',
            'UI_color_green'                       : 'Green',
            'UI_color_green_yellow'                : 'Green Yellow',
            'UI_color_hot_pink'                    : 'Hot Pink',
            'UI_color_lime'                        : 'Lime',
            'UI_color_orange'                      : 'Orange',
            'UI_color_pink'                        : 'Pink',
            'UI_color_purple'                      : 'Purple',
            'UI_color_red'                         : 'Red',
            'UI_color_wg_blur'                     : 'WG Blur',
            'UI_color_wg_enemy'                    : 'WG Enemy',
            'UI_color_wg_friend'                   : 'WG Friend',
            'UI_color_wg_squad'                    : 'WG Squad',
            'UI_color_yellow'                      : 'Yellow',
            'UI_color_nice_red'                    : 'Nice Red',
            'UI_color_very_bad'                    : 'Very bad rating',
            'UI_color_bad'                         : 'Bad rating',
            'UI_color_normal'                      : 'Normal rating',
            'UI_color_good'                        : 'Good rating',
            'UI_color_very_good'                   : 'Very good rating',
            'UI_color_unique'                      : 'Unique rating'
        }
        #self.cdata = jsonDumps(self.data, indent=4, sort_keys=False)
        self.data, self.i18n = g_gui.register_data(self.ids, self.data, self.i18n, 'TheIllusion')
        g_gui.register(self.ids, self.template, self.data, self.apply)
        print '[LOAD_MOD]:  [%s %s, %s]' % (self.ids, self.version, self.author)

    def template(self):
        template_gen = {
            'modDisplayName': self.i18n['UI_description'],
            'settingsVersion': self.version_id,
            'enabled': self.data['enabled'],
            'column1': [{
                'type': 'Label',
                'text': self.i18n['UI_setting_carouselsEnabled_label'],
                'tooltip': ''
            }, {
                'type': 'CheckBox',
                'text': self.i18n['UI_setting_carouselsEnabled_text'],
                'value': self.data['carouselsEnabled'],
                'tooltip': '',
                'varName': ['carouselsEnabled']
            }, {
                'type': 'Dropdown',
                'text': self.i18n['UI_setting_tankrows_text'],
                'itemRenderer': 'DropDownListItemRendererSound',
                'options'     : self.generator_menu(),
                'width': 10,
                'value': self.data['tankrows'],
                'tooltip': '',
                'varName': 'tankrows'
                }],
            'column2': [{
                'type': 'Label',
                'text': self.i18n['UI_setting_sounds_label'],
                'tooltip': ''
            }, {
                'type': 'CheckBox',
                'text': self.i18n['UI_setting_fireSoundEnabled_text'],
                'value': self.data['fireSoundEnabled'],
                'tooltip': '',
                'varName': 'fireSoundEnabled'
            }, {
                'type': 'CheckBox',
                'text': self.i18n['UI_setting_stunSoundEnabled_text'],
                'value': self.data['stunSoundEnabled'],
                'tooltip': '',
                'varName': 'stunSoundEnabled'
            }]
        }
        return template_gen

    def apply(self, settings):
        self.data = g_gui.update_data(self.ids, settings, 'TheIllusion')
        g_gui.update(self.ids, self.template)
    
    def generator_menu(self):
        res = []
        for i in xrange(0, len(COLOR)):
            res.append({
                'label': '<font color="%s">%s</font>' % (COLOR[i], self.i18n[MENU[i]])
            })
        return res

config = Config()

config.carouselsEnabled = config.data['carouselsEnabled']
#config.carouselsSize = data['Carousels']['Large']
config.tankrows = config.data['tankrows']
config.stunEnabled = config.data['stunSoundEnabled']
config.fireEnabled = config.data['fireSoundEnabled']

"""
IVM Carousel Handler
"""

if config.carouselsEnabled == True: #and _config.carouselsSize == False:
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS

    def new_as_rowCountS(self, value):
        old_as_rowsCountS(self, value)
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(_config.tankrows)

    TankCarouselMeta.as_rowCountS = new_as_rowCountS
    print '[IVM] Tank Carousels Loaded with ' + str(_config.tankrows) + ' rows'
#elif _config.carouselsEnabled == True and _config.carouselsSize == True:
#    old_as_setSmallDoubleCarouselS = TankCarouselMeta.as_setSmallDoubleCarouselS
#
#    def new_as_setSmallDoubleCarouselS(self, value):
#        old_as_setSmallDoubleCarouselS(self, value)
#        if self._isDAAPIInited():
#            return self.flashObject.as_setSmallDoubleCarouselS(_config.tankrows)
#
#    TankCarouselMeta.as_setSmallDoubleCarouselS = new_as_setSmallDoubleCarouselS
#    print '[IVM] Tank Carousels Loaded as small with ' + str(_config.tankrows) + ' rows'
else:
    print '[IVM] Tank Carousels Not Enabled'
    pass

"""
IVM Stun Sound Handler
"""

if config.stunEnabled == True:
    #assign old event
    old_DestroyTimersPanel__showStunTimer = DestroyTimersPanel._DestroyTimersPanel__showStunTimer
    #define new event
    def illusion_stunSound_DestroyTimersPanel__showStunTimer(self, value):
        #call old event
        old_DestroyTimersPanel__showStunTimer(self, value)
        try:
            if value.duration > 0.0:
                #play sound at event 'battle_event_stun'
                SoundGroups_g_instance.playSound2D('battle_event_stun')
        except:
            #if that doesnt work, log the error
            print '[ERROR][IVM] Stun Sound Not Played'
            LOG_CURRENT_EXCEPTION()
    #replace old event with new one
    DestroyTimersPanel._DestroyTimersPanel__showStunTimer = illusion_stunSound_DestroyTimersPanel__showStunTimer

    print '[IVM][LOAD] IVM Stun Sound Loaded'
else:
    print '[IVM] Stun Sound Not Loaded'
    pass

"""
IVM fire sound handler
"""
if config.fireEnabled == True:
    #assign old event
    old_DestroyTimersPanel__setFireInVehicle = DestroyTimersPanel._DestroyTimersPanel__setFireInVehicle

    def IVM_new__setFireInVehicle(self, isInFire):
        old_DestroyTimersPanel__setFireInVehicle(self, isInFire)
        try:
            if isInFire:
                #play sound at event 'battle_event_fire'
                SoundGroups_g_instance.playSound2D('battle_event_fire')
            else:
                self._hideTimer(_TIMER_STATES.FIRE)
            return
        except:
            #if that doesnt work, log the exception
            print('Failed to play fire sound')
            LOG_CURRENT_EXCEPTION()
    #replace old event with new
    DestroyTimersPanel._DestroyTimersPanel__setFireInVehicle = IVM_new__setFireInVehicle

    print '[IVM][LOAD] IVM Fire Sound Loaded'
else:
    print '[IVM] Fire Sound Not Loaded'
    pass
