# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_quad', [dirname(__file__)])
        except ImportError:
            import _quad
            return _quad
        if fp is not None:
            try:
                _mod = imp.load_module('_quad', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _quad = swig_import_helper()
    del swig_import_helper
else:
    import _quad
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0


try:
    import weakref
    weakref_proxy = weakref.proxy
except Exception:
    weakref_proxy = lambda x: x


import collections
class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _quad.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self):
        return _quad.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _quad.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _quad.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _quad.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _quad.SwigPyIterator_equal(self, x)

    def copy(self):
        return _quad.SwigPyIterator_copy(self)

    def next(self):
        return _quad.SwigPyIterator_next(self)

    def __next__(self):
        return _quad.SwigPyIterator___next__(self)

    def previous(self):
        return _quad.SwigPyIterator_previous(self)

    def advance(self, n):
        return _quad.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _quad.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _quad.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _quad.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _quad.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _quad.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _quad.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _quad.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)


def new_doublep():
    return _quad.new_doublep()
new_doublep = _quad.new_doublep

def copy_doublep(value):
    return _quad.copy_doublep(value)
copy_doublep = _quad.copy_doublep

def delete_doublep(obj):
    return _quad.delete_doublep(obj)
delete_doublep = _quad.delete_doublep

def doublep_assign(obj, value):
    return _quad.doublep_assign(obj, value)
doublep_assign = _quad.doublep_assign

def doublep_value(obj):
    return _quad.doublep_value(obj)
doublep_value = _quad.doublep_value

_quad.QD_MAX_swigconstant(_quad)
QD_MAX = _quad.QD_MAX
class Quad(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Quad, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Quad, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _quad.new_Quad(*args)
        try:
            self.this.append(this)
        except Exception:
            self.this = this
    __swig_destroy__ = _quad.delete_Quad
    __del__ = lambda self: None

    def init(self):
        return _quad.Quad_init(self)

    def SetAlpha(self, alpha):
        return _quad.Quad_SetAlpha(self, alpha)

    def SetBeta(self, betta):
        return _quad.Quad_SetBeta(self, betta)

    def SetDomain(self, *args):
        return _quad.Quad_SetDomain(self, *args)

    def GetDomain(self, *args):
        return _quad.Quad_GetDomain(self, *args)

    def SetRule(self, *args):
        return _quad.Quad_SetRule(self, *args)

    def GetRule(self, *args):
        return _quad.Quad_GetRule(self, *args)

    def SetQdpts(self, q):
        return _quad.Quad_SetQdpts(self, q)

    def SetWghts(self, w):
        return _quad.Quad_SetWghts(self, w)

    def GetQdpts(self, q):
        return _quad.Quad_GetQdpts(self, q)

    def GetWghts(self, w):
        return _quad.Quad_GetWghts(self, w)

    def SetLevel(self, param):
        return _quad.Quad_SetLevel(self, param)

    def nextLevel(self):
        return _quad.Quad_nextLevel(self)

    def GetNQ(self):
        return _quad.Quad_GetNQ(self)

    def SetVerbosity(self, verbosity):
        return _quad.Quad_SetVerbosity(self, verbosity)
Quad_swigregister = _quad.Quad_swigregister
Quad_swigregister(Quad)

# This file is compatible with both classic and new-style classes.


