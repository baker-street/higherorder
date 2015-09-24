# -*- coding: utf-8 -*-
__title__ = 'fnctional'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '9/17/2015'


def pass_through(obj, *_, **__):
    return obj


def always_true(obj, *_, **__):
    return True


def always_false(obj, *_, **__):
    return False


def _try_custom_name(fnc, *_, **kwargs):
    try:
        return kwargs['fncname']
    except KeyError:
        try:
            return fnc.__name__
        except AttributeError:
            return 'NoName'


def _try_custom_doc(fnc, *_, **kwargs):
    try:
        return kwargs['fncdoc']
    except KeyError:
        try:
            return fnc.__doc__
        except AttributeError:
            return 'NoDoc'


def _try_assign_type(fnc, *_, **kwargs):
    try:
        return kwargs['fnctype']
    except KeyError:
        try:
            return fnc.__type__
        except AttributeError:
            return 'NoType'


def _try_assign_arg_checker(fnc, *_, **kwargs):
    try:
        return kwargs['fncchecker']
    except KeyError:
        try:
            return fnc.__checker__
        except AttributeError:
            return pass_through


def _try_assign_uuid(fnc, *_, **kwargs):
    try:
        return kwargs['fncuuid']
    except KeyError:
        try:
            return fnc.__uuid__
        except AttributeError:
            return 'NoUUID'


def assign_new_fnc_attrs(**kwargs):
    def _assign_new_fnc_attrs(fnc, *_, **xargs):
        fnc.__name__ = _try_custom_name(fnc, **kwargs)
        fnc.__doc__ = _try_custom_doc(fnc, **kwargs)
        fnc.__type__ = _try_assign_type(fnc, **kwargs)
        fnc.__checker__ = _try_assign_arg_checker(fnc, **kwargs)
        fnc.__uuid__ = _try_assign_uuid(fnc, **kwargs)
        return fnc
    return _assign_new_fnc_attrs


def assign_new_var_fnc_attrs(fnc, *_, **kwargs):
    fnc.__name__ = _try_custom_name(fnc, **kwargs)
    fnc.__doc__ = _try_custom_doc(fnc, **kwargs)
    fnc.__type__ = _try_assign_type(fnc, **kwargs)
    fnc.__checker__ = _try_assign_arg_checker(fnc, **kwargs)
    fnc.__uuid__ = _try_assign_uuid(fnc, **kwargs)
    return fnc
