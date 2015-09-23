# -*- coding: utf-8 -*-
__title__ = 'fnctional'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.c.projects@gmail.com'
__created_on__ = '9/17/2015'


from fnctional import utils


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


utils._try_custom_name
def test__try_custom_name():
    def some_func(*_, **kwargs):
        pass
    the_func = some_func
    assert(the_func.__name__ == 'some_func')
    the_func.__name__ = utils._try_custom_name(the_func, **{'fncname': 'name_two'})
    assert(the_func.__name__ == 'name_two')
