#imports
import BigWorld
from gui.Scaleform.daapi.view.meta.TankCarouselMeta import TankCarouselMeta
#import BattleReplay

#set old to base file
old_as_rowsCountS = TankCarouselMeta.as_rowCountS
tankrows = 5

def new_as_rowCountS(self, value):
    old_as_rowsCountS(self, value)
    if self._isDAAPIInited():
        return self.flashObject.as_rowCount(tankrows)
    elif not self._isDAAPIInited():
        return 'DAAPI Failed'

#replace base file with new count
TankCarouselMeta.as_rowCountS = new_as_rowCountS

#tell python.log mod loaded
def printModLoaded(text):
    print text

printModLoaded('[LOAD] Lego Loaded Sucessfully')