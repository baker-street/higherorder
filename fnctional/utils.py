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
