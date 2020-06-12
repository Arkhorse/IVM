# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/mods/vehicle_exp/settings.py
# Compiled at: 2019-04-28 17:25:20
import inspect
import sys
from functools import partial, update_wrapper
from gui.modsSettingsApi import g_modsSettingsApi
__all__ = ('SettingsKeyGetter', 'SettingsKeyChecker', 'AbstractSettings', 'overrideMethod')

class SettingsKeyGetter(object):

    def __init__(self, key, attribute='settings', wrapper=lambda value: value):
        super(SettingsKeyGetter, self).__init__()
        self.key = key
        self.attribute = attribute
        self.wrapper = wrapper
        assert callable(wrapper), 'Wrapper is not callable!'
        assert isinstance(key, str), 'Key is not string!'
        assert isinstance(attribute, str), 'Attribute is not string!'

    def __get__(self, instance, objtype=None):
        value = getattr(instance, self.attribute)[self.key]
        if self.wrapper:
            value = self.wrapper(value)
        return value


class SettingsKeyChecker(SettingsKeyGetter):

    def __init__(self, key, attribute='settings'):
        super(SettingsKeyChecker, self).__init__(key, attribute=attribute, wrapper=g_modsSettingsApi.checkKeySet)


class AbstractSettings(object):

    def __init__(self, name):
        self.__name = name
        self.__registerModSettings()

    def __registerModSettings(self):
        settingsTemplate = self.getSettingsTemplate()
        savedSettings = g_modsSettingsApi.getModSettings(self.__name, settingsTemplate)
        if savedSettings:
            settings = savedSettings
            g_modsSettingsApi.registerCallback(self.__name, self.__onModSettingsChanged)
        else:
            settings = g_modsSettingsApi.setModTemplate(self.__name, settingsTemplate, self.__onModSettingsChanged)
        self.__onModSettingsChanged(self.__name, settings, True)

    def __onModSettingsChanged(self, linkage, settings, isFirst=False):
        if linkage == self.__name:
            self.onSettingsUpdated(settings, isFirst)

    def onSettingsUpdated(self, settings, isFirst):
        pass

    def getSettingsTemplate(self):
        raise NotImplementedError

#@overrideMethod
def overrideMethod(obj, prop, getter=None, setter=None, deleter=None):
    """
    :param obj: object, which attribute needs overriding
    :param prop: attribute name (can be not mangled), attribute must be callable
    :param getter: fget function or None
    :param setter: fset function or None
    :param deleter: fdel function or None
    :return function: unmodified getter or, if getter is None and src is not property, decorator"""

    if inspect.isclass(obj) and prop.startswith('__') and prop not in dir(obj) + dir(type(obj)):
        prop = obj.__name__ + prop
        if not prop.startswith('_'):
            prop = '_' + prop
    src = getattr(obj, prop)
    if type(src) is property and (getter or setter or deleter):
        props = []
        for func, fType in ((getter, 'fget'), (setter, 'fset'), (deleter, 'fdel')):
            assert func is None or callable(func), fType + ' is not callable!'
            props.append(partial(func, getattr(src, fType)) if func else getattr(src, fType))
        setattr(obj, prop, property(*props))
        return getter
    elif getter:
        getter_orig = getter
        assert callable(src), 'Source property is not callable!'
        assert callable(getter_orig), 'Handler is not callable!'
        while isinstance(getter, partial):
            getter = getter.func

        def getter_new(*a, **k):  # noinspection PyUnusedLocal
            info = None
            try:
                return getter_orig(src, *a, **k)
            except Exception:  # Code to remove this wrapper from traceback
                info = sys.exc_info()
                new_tb = info[2].tb_next  # https://stackoverflow.com/q/44813333
                if new_tb is None:  # exception occurs inside this wrapper, not inside of getter_orig
                    new_tb = _generate_new_tb(getter.func_code)
                raise info[0], info[1], new_tb
            finally:
                del info

        try:
            update_wrapper(getter_new, getter)
        except AttributeError:
            pass
        if inspect.isclass(obj):
            if inspect.isfunction(src):
                getter_new = staticmethod(getter_new)
            elif getattr(src, '__self__', None) is not None:
                getter_new = classmethod(getter_new)
        setattr(obj, prop, getter_new)
        return getter_orig
    else:
        return partial(overrideMethod, obj, prop)