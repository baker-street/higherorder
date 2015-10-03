# -*- coding: utf-8 -*-
__author__ = 'Steven Cutting'
__author_email__ = 'steven.c.projects@gmail.com'
__copyright__ = "higherorder  Copyright (C) 2015  Steven Cutting"
__created_on__ = '9/17/2015'

from higherorder.__about__ import *

from higherorder import utils


def test__pass_through():
    assert(utils.pass_through('monkey') == 'monkey')


def test__pass_through__two():
    somelist = ['monkey', 'foo', 'bar']
    assert(utils.pass_through(somelist) == somelist)


def test__always_true():
    assert(utils.always_true('monkey') is True)


def test__always_true__two():
    somelist = ['monkey', 'foo', 'bar']
    assert(utils.always_true(somelist) is True)


def test__always_false():
    assert(utils.always_false('monkey') is False)


def test__always_false__two():
    somelist = ['monkey', 'foo', 'bar']
    assert(utils.always_false(somelist) is False)


def test__try_assign_name():
    def some_func(*_, **kwargs):
        pass
    the_func = some_func
    assert(the_func.__name__ == 'some_func')
    the_func.__name__ = utils._try_assign_name(the_func, **{'__name__': 'name_two'})
    assert(the_func.__name__ == 'name_two')


def test__assign_new_var_func_attrs():
    def m():
        pass
    m = utils.assign_var_func_attrs(m, __name__='m_and_m')
    assert(m.__name__ == 'm_and_m')


def test__assign_new_var_func_attrs__two():
    def m():
        pass
    m = utils.assign_var_func_attrs(m, __type__='monkey')
    assert(m.__type__ == 'monkey')


def test__append_var_to_func_attrs():
    def m():
        pass
    m = utils.append_var_to_func_attrs(m, __name__='_and_m')
    assert(m.__name__ == 'm_and_m')


def test__prepend_var_to_func_attrs():
    def m():
        pass
    m = utils.prepend_var_to_func_attrs(m, __name__='m_and_')
    assert(m.__name__ == 'm_and_m')
