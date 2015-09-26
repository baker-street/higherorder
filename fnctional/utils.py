# -*- coding: utf-8 -*-
__title__ = 'fnctional'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '9/17/2015'

from copy import deepcopy


def pass_through(obj, *_, **__):
    return obj


def always_true(*_, **__):
    return True


def always_false(*_, **__):
    return False


def _try_assign_name(fnc, *_, **kwargs):
    try:
        return kwargs['__name__']
    except KeyError:
        try:
            return fnc.__name__
        except AttributeError:
            return 'NoName'


def _try_assign_doc(fnc, *_, **kwargs):
    try:
        return kwargs['__doc__']
    except KeyError:
        try:
            return fnc.__doc__
        except AttributeError:
            return 'NoDoc'


def _try_assign_type(fnc, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A type attribute.
    __type__
    """
    try:
        return kwargs['__type__']
    except KeyError:
        try:
            return fnc.__type__
        except AttributeError:
            return 'NoType'


def _try_assign_arg_checker(fnc, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A checker attribute.
    __checker__

    - checker - a function that can be optionally used to check the input to
                the function it's assigned to.
    """
    try:
        return kwargs['__checker__']
    except KeyError:
        try:
            return fnc.__checker__
        except AttributeError:
            return pass_through


def _try_assign_uuid(fnc, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A uuid attribute.
    __uuid__
    """
    try:
        return kwargs['__uuid__']
    except KeyError:
        try:
            return fnc.__uuid__
        except AttributeError:
            return 'NoUUID'


def _try_assign_desc(fnc, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A description attribute.
    __desc__
    """
    try:
        return kwargs['__desc__']
    except KeyError:
        try:
            return fnc.__desc__
        except AttributeError:
            return 'NoDesc'


def assign_new_var_fnc_attrs(fnc, *_, **kwargs):
    newfnc = deepcopy(fnc)
    for k, v in kwargs.items():
        newfnc.__setattr__(k, v)
    return newfnc


def assign_new_fnc_attrs(**kwargs):
    """
    Is a decorator
    Adds custom attributes to a function and can be used to replace
    standard attributes.
    - can replace or add any attribute. Use with care.
    """
    def _inner(fnc, *_, **__):
        return assign_new_var_fnc_attrs(fnc=fnc, **kwargs)
    return _inner
