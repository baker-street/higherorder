# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__copyright__ = "higherorder  Copyright (C) 2015  Steven Cutting"
__created_on__ = '9/17/2015'
from higherorder.__about__ import *

import logging
LOG = logging.getLogger(__name__)

import sys
from copy import deepcopy
from collections import Iterable
import traceback
from json import loads as jloads

from toolz.dicttoolz import dissoc

if sys.version_info[0] < 3:
    _STRINGTYPES = (basestring,)
else:
    # temp fix, so that 2.7 support wont break
    unicode = str  # adjusting to python3
    _STRINGTYPES = (str, bytes)


def xargs_cndm(*ok, **xargs):
    return {key: value for key, value in xargs.items() if key in ok}


def xargs_cndm_loads(ok, **xargs):
    return xargs_cndm(*jloads(ok), **xargs)


def pass_through(obj, *_, **__):
    return obj


def always_true(*_, **__):
    return True


def always_false(*_, **__):
    return False


def res_and_uuid(res, func, reskey=u'feature_array', funckey=u'feature_set_id'):
    """
    return {u'feature_array': res, u'functor_id': func.uuid}
    """
    return {reskey: res, funckey: func.uuid}


def run_and_return_res_n_uuid(func, *args, **xargs):
    """
    res = func(*args, **xargs)
    return res_and_uuid(res=res, func=func)
    """
    res = func(*args, **xargs)
    return res_and_uuid(res=res, func=func)


def rm_key(rpackiter, *keys):
    for pack in rpackiter:
        try:
            yield dissoc(pack, *keys)
        except KeyError:
            yield pack


# -----------------------------------------------------------------------------
# mess with func attrs


def get_attr(func, attr='__name__'):
    return func.__getattribute__(attr)


def _try_assign_name(func, *_, **kwargs):
    try:
        return kwargs['__name__']
    except KeyError:
        try:
            return func.__name__
        except AttributeError:
            return 'NoName'


def _try_assign_doc(func, *_, **kwargs):
    try:
        return kwargs['__doc__']
    except KeyError:
        try:
            return func.__doc__
        except AttributeError:
            return 'NoDoc'


def _try_assign_type(func, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A type attribute.
    __type__
    """
    try:
        return kwargs['__type__']
    except KeyError:
        try:
            return func.__type__
        except AttributeError:
            return 'NoType'


def _try_assign_arg_checker(func, *_, **kwargs):
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
            return func.__checker__
        except AttributeError:
            return pass_through


def _try_assign_uuid(func, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A uuid attribute.
    __uuid__
    """
    try:
        return kwargs['__uuid__']
    except KeyError:
        try:
            return func.__uuid__
        except AttributeError:
            return 'NoUUID'


def _try_assign_desc(func, *_, **kwargs):
    """
    Add custom dunder attribute to a function.
    A description attribute.
    __desc__
    """
    try:
        return kwargs['__desc__']
    except KeyError:
        try:
            return func.__desc__
        except AttributeError:
            return 'NoDesc'


# -----------------
def _try_kwarg(key, default=False, **kwargs):
    try:
        return kwargs[key]
    except KeyError:
        return default

try_kwarg = _try_kwarg


def _join_prts_fctr(**kwargs):
    append = _try_kwarg('append', **kwargs)
    prepend = _try_kwarg('prepend', **kwargs)
    nonstr = _try_kwarg('nonstr', **kwargs)
    if append:
        def join_prts(old, new):
            return ''.join([old, new])
    elif prepend:
        def join_prts(old, new):
            return ''.join([new, old])
    elif nonstr:
        def join_prts(old, new):
            return new
    else:
        def join_prts(old, new):
            return new
    return join_prts


def _var_to_func_attrs(func, *_, **kwargs):
    """
    Do not use directly.
    Handles manipulation of function attributes.
    """
    newfunc = deepcopy(func)
    nonstr = _try_kwarg('nonstr', **kwargs)
    join_prts = _join_prts_fctr(**kwargs)
    for k, v in kwargs.items():
        if k not in {'append', 'prepend', 'nonstr'}:
            try:
                oldattr = func.__getattribute__(k)
            except AttributeError:
                oldattr = ''
            newattr = join_prts(old=oldattr,
                                new=v)
            if nonstr:
                newfunc.__setattr__(k, newattr)
            else:
                newfunc.__setattr__(k, str(newattr))
    return newfunc


def assign_var_func_attrs(func, *_, **kwargs):
    """
    Adds custom attributes to a function and can be used to replace
    standard attributes.
    - can replace or add any attribute. Use with care.
    """
    return _var_to_func_attrs(func, append=False, prepend=False, **kwargs)


def assign_func_attrs(**kwargs):
    """
    Is a decorator
    Adds custom attributes to a function and can be used to replace
    standard attributes.
    - can replace or add any attribute. Use with care.
    """
    def _inner(func, *_, **__):
        return _var_to_func_attrs(func=func, append=False, prepend=False, **kwargs)
    return _inner


def assign_nonstr_func_attrs(**kwargs):
    """
    Is a decorator
    Adds custom attributes to a function and can be used to replace
    standard attributes.
    - can replace or add any attribute. Use with care.
    """
    def _inner(func, *_, **__):
        return _var_to_func_attrs(func=func, nonstr=True, append=False, prepend=False, **kwargs)
    return _inner


def prepend_var_to_func_attrs(func, *_, **kwargs):
    return _var_to_func_attrs(func, append=False, prepend=True, **kwargs)


def prepend_to_func_attrs(**kwargs):
    """
    Is a decorator
    Prepends stuff to existing function attributes (only works with strings)
    """
    def _inner(func, *_, **__):
        return _var_to_func_attrs(func=func, append=False, prepend=True, **kwargs)
    return _inner


def append_var_to_func_attrs(func, *_, **kwargs):
    return _var_to_func_attrs(func, append=True, prepend=False, **kwargs)


def append_to_func_attrs(**kwargs):
    """
    Is a decorator
    Appends stuff to existing function attributes (only works with strings)
    """
    def _inner(func, *_, **__):
        return _var_to_func_attrs(func=func, append=True, prepend=False, **kwargs)
    return _inner


# -----------------------------------------------------------------------------
# Error Handling


def log_error(dontstop=False, default=None, **kwargs):
    """
    A decorator.
    """
    def _inner(func, *_, **__):
        def mod(func, *_, **__):
            def new_func(*args, **xargs):
                try:
                    return func(*args, **xargs)
                except:
                    LOG.critical('\t'.join(['Function Failed:\t',
                                            func.__name__,
                                            '\tTraceback:',
                                            str(traceback.format_exc()),
                                            ]))
                    if dontstop:
                        return None
                    else:
                        raise
            mod.__name__ = func.__name__
            mod.__doc__ = func.__name__
            return new_func
        return mod(func)
    return _inner


# -----------------------------------------------------------------------------
# flatten data structures


# Try to make the flatten funcs suck a little less; too many loops and what not.
def flatten_dict_tree(dicttree, __keypath=u''):
    """
    Flattens only the dicts in a dict tree.
    """
    newdict = {}
    for key, value in dicttree.items():
        fullkeypath = __keypath + '-' + key
        if isinstance(value, dict):
            newdict.update(flatten_dict_tree(value, fullkeypath))
        else:
            newdict[key] = value
    return newdict


def flatten_array_like_strct_gen(arraything, dictvalues=False):
    for i in arraything:
        if isinstance(i, _STRINGTYPES):
            yield i
        elif isinstance(i, dict):
            if dictvalues:
                g = flatten_array_like_strct_gen(flatten_dict_tree(i).values(),
                                                 dictvalues=dictvalues)
                for j in g:
                    yield j
            else:
                yield i
        elif isinstance(i, Iterable):
            for j in flatten_array_like_strct_gen(i,
                                                  dictvalues=dictvalues):
                yield j
        else:
            yield i


def flatten_handle_all(datastrct, dictvalues=False, *_, **__):
    if isinstance(datastrct, dict):
        if not dictvalues:
            yield datastrct
        else:
            for i in flatten_array_like_strct_gen(datastrct.values(),
                                                  dictvalues=dictvalues):
                yield i
    else:
        for i in flatten_array_like_strct_gen(datastrct,
                                              dictvalues=dictvalues):
            yield i


def flatten_all(*datastrcts, **xargs):
    return flatten_handle_all(datastrct=datastrcts, **xargs)


def flatten_all_if_true(*datastrcts, **xargs):
    try:
        flatten = xargs['flatten']
    except KeyError:
        flatten = True
    if flatten:
        return flatten_all(*datastrcts, **xargs)
    else:
        return datastrcts
