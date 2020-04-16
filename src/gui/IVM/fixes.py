from _config import config
import mod_constants

# Effects List Spam Fix
if config.data['fixEffects'] == True:
    from helpers import EffectsList
    EffectsList.LOG_WARNING = lambda *_, **__: None
    print 'Effects List Spam Fix by ' + str(__name__), str(__version__) + ' done.'
else:
    pass

# Vehicle Model Transparency Fix
if config.data['fixVehicleTransparency'] == True:
    from vehicle_systems.components.highlighter import Highlighter
    def IVM_doHighlight(self, status, args):
        if self._Highlighter__isPlayersVehicle:
            status &= ~self.HIGHLIGHT_SIMPLE & ~self.HIGHLIGHT_ON
        old_doHighlight(self, status, args)
    old_doHighlight = Highlighter._Highlighter__doHighlightOperation
    Highlighter._Highlighter__doHighlightOperation = IVM_doHighlight
    print 'Vehicle Model Transparency Fix by ' + str(__name__), str(__version__) + ' done.'
else:
    pass