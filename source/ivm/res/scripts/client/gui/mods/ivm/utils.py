import inspect
import sys
from functools import partial, update_wrapper

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
