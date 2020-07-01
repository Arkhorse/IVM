import inspect
import sys
from functools import partial, update_wrapper

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

import functools
import BigWorld

def override(obj, prop, getter=None, setter=None, deleter=None):
    """ Overrides attribute in object.
    Attribute should be property or callable.
    Getter, setter and deleter should be callable or None.
    :param obj: Object
    :param prop: Name of any attribute in object (can be not mangled)
    :param getter: Getter function
    :param setter: Setter function
    :param deleter: Deleter function"""
    if inspect.isclass(obj) and prop.startswith('__') and prop not in dir(obj) + dir(type(obj)):
        prop = obj.__name__ + prop
        if not prop.startswith('_'):
            prop = '_' + prop
    src = getattr(obj, prop)
    assert type(src) is property and (getter or setter or deleter) and getter is None or callable(getter), 'Getter is not callable!'
    assert setter is None or callable(setter), 'Setter is not callable!'
    if not deleter is None:
        assert callable(deleter), 'Deleter is not callable!'
        getter = functools.partial(getter, src.fget) if getter else src.fget
        setter = functools.partial(setter, src.fset) if setter else src.fset
        deleter = functools.partial(deleter, src.fdel) if deleter else src.fdel
        setattr(obj, prop, property(getter, setter, deleter))
        return getter
    elif getter:
        assert callable(src), 'Source property is not callable!'
        assert callable(getter), 'Handler is not callable!'
        if inspect.isclass(obj) and inspect.ismethod(src) or isinstance(src, type(BigWorld.Entity.__getattribute__)):
            getter_new = lambda *args, **kwargs: getter(src, *args, **kwargs)
        else:
            getter_new = functools.partial(getter, src)
        setattr(obj, prop, getter_new)
        return getter
    else:
        return functools.partial(override, obj, prop)
        return