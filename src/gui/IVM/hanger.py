from _config import config
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta

if config.data['carEnabled'] == True:
    old_as_rowsCountS = TankCarouselMeta.as_rowCountS
    tankrows = config.data['carRows']
    def new_as_rowCountS(self, value):
        old_as_rowsCountS(self, value)
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(tankrows)
    
    TankCarouselMeta.as_rowCountS = new_as_rowCountS
    from gui.Scaleform.daapi.view.common.vehicle_common import carousel_environment
    def updateVehicles(self, diff):
        self._carouselDP.updateVehicles()

    print '[IVM] Tank Carousels Loaded with ' + str(config.data['carRows']) + ' rows'
else:
    print '[IVM] Tank Carousels Not Enabled'
    pass