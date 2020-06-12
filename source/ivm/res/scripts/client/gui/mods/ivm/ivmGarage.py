import BigWorld
from ..mod_ivm import Version, ModIDShort, debug
from .utils import override
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta

try:
    from PYmodsCore import PYmodsConfigInterface
except ImportError:
    print ModIDShort, 'Ingame UI not found, passing'
    pass

class ivmGarage(PYmodsConfigInterface):

    def init(self):
        self.ID = 'ivmGarage'
        self.version = Version[1]
        self.modsGroups = 'IVM'
        self.data = {'enabled': True, 'carEnabled': True, 'carRows': 2}
        super(ivmGarage, self).init()

    def loadLang(self):
        if self.lang == 'en':
            self.i18n = {
                'name': 'Garage Options',
                'UI_setting_carEnabled_text': 'Enable the carousel rows option',
                'UI_setting_carRows_text': 'Choose how many rows you want',
                'UI_setting_carRows_tooltip': 'To apply this, you MUST reload the game'
                }

    def createTemplate(self):
        return {
            'modDisplayName': self.i18n['name'],
            'enabled': self.data['enabled'],
            'column1': [self.tb.createControl('carEnabled')],
            'column2': [self.tb.createSlider('carRows', vMin=0, vMax=12, value=2, formatStr='{{value}}', width=200, step=1, empty=False)]
        }

config = ivmGarage()
carEnabled = config.data['carEnabled']
carRows = config.data['carRows']

if carEnabled:
    print ModIDShort, 'Carousel Options Enabled'
    if debug:
        print ModIDShort, carEnabled, carRows
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS

    def new_as_rowCountS(self, value):
        old_as_rowsCountS(self, value)
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(carRows)
    TankCarouselMeta.as_rowCountS = new_as_rowCountS
else:
    print ModIDShort, 'Carousel Options Disabled'
