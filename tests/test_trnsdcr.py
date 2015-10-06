# -*- coding: utf-8 -*-
__author__ = 'Steven Cutting'
__author_email__ = 'steven.c.projects@gmail.com'
__copyright__ = "higherorder  Copyright (C) 2015  Steven Cutting"
__created_on__ = '8/30/2015'

from higherorder.__about__ import *

from functools import partial

from higherorder.trnsdcr import(trnsdcr,
                                one_layer_tree,
                                preiter_iter_postiter,
                                one_layer_tree_w_meta,
                                fork)


# -------------------------------------
# tests for simple transducer
def smpl_1(strng, addtn='', **xargs):
    return strng + '_one' + addtn


def smpl_2(strng, addtn='', **xargs):
    return strng + '_two' + addtn


def smpl_3(strng, addtn='', **xargs):
    return strng + '_three' + addtn


def smpl_4(strng, addtn='', **xargs):
    return strng + '_four' + addtn, xargs


def test_gen():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4])
    assert(f('monkey') == ('monkey_one_two_three_four', {}))


def test_kwarg_at_build():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4], addtn='-')
    assert(f('monkey') == ('monkey_one-_two-_three-_four-', {}))


def test_kwarg_at_run():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4])
    assert(f('monkey', addtn='-') == ('monkey_one-_two-_three-_four-', {}))


def test_same_kwarg_at_build_and_run_same_value():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4], addtn='-')
    assert(f('monkey', addtn='-') == ('monkey_one-_two-_three-_four-', {}))


def test_same_kwarg_at_build_and_run_diff_value():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4], addtn='-')
    assert(f('monkey', addtn='&') == ('monkey_one-_two-_three-_four-', {}))


def test_unused_kwarg_at_build():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4], foo='bar')
    assert(f('monkey') == ('monkey_one_two_three_four', {'foo': 'bar'}))


def test_unused_kwarg_at_run():
    f = trnsdcr([smpl_1, smpl_2, smpl_3, smpl_4])
    assert(f('monkey',
             foo='bar') == ('monkey_one_two_three_four',
                            {'foo': 'bar'}))


# -----------------------------------------------------------------------------
# Tests for other transducers

SMPLTXT = """Little Bo peep has lost her sheep
And doesn't know where to find them.
Leave them alone and they'll come home,
Bringing their tails behind them.
Little Bo peep fell fast asleep
And dreamt she heard them bleating,
But when she awoke, she found it a joke,
For they were all still fleeting.
"""

SMPLTOKENS = ['Little', 'Bo', 'peep', 'has', 'lost', 'her', 'sheep',
              'And', "doesn't", 'know', 'where', 'to', 'find', 'them.',
              'Leave', 'them', 'alone', 'and', "they'll", 'come', 'home,',
              'Bringing', 'their', 'tails', 'behind', 'them.',
              'Little', 'Bo', 'peep', 'fell', 'fast', 'asleep',
              'And', 'dreamt', 'she', 'heard', 'them', 'bleating,',
              'But', 'when', 'she', 'awoke,', 'she', 'found', 'it', 'a', 'joke,',
              'For', 'they', 'were', 'all', 'still', 'fleeting.']


def spliter(txt, **xargs):
    return txt.split()


def split_on(txt, spliton='.', **xargs):
    return txt.split(spliton)


def rm_char(txt, char, rplcwith='', **xargs):
    return txt.replace(char, rplcwith)


def test__preiter_iter_postiter__one__basic_spliter_only():
    func = preiter_iter_postiter(iter_func=spliter)
    assert(list(func(txt=SMPLTXT)) == SMPLTOKENS)


def test__preiter_iter_postiter__two__remove_t_pre_basic_split():
    rm_t = partial(rm_char, char='t')
    func = preiter_iter_postiter(iter_func=spliter, pre_iter=rm_t)
    for tkn in func(SMPLTXT):
        assert('t' not in tkn)


def test__preiter_iter_postiter__three__remove_t_post_basic_split():
    rm_t = partial(rm_char, char='t')
    func = preiter_iter_postiter(iter_func=spliter, post_iter=rm_t)
    for tkn in func(SMPLTXT):
        assert('t' not in tkn)


def test__preiter_iter_postiter__four__remove_t_pre_basic_split_then_undo_in_post_split():
    rplc_t = partial(rm_char, char='t', rplcwith='_-_')
    undo_rplc_t = partial(rm_char, char='_-_', rplcwith='t')
    func = preiter_iter_postiter(iter_func=spliter, pre_iter=rplc_t, post_iter=undo_rplc_t)
    for tkn, ptkn in zip(spliter(SMPLTXT), func(SMPLTXT)):
        if 't' in tkn:
            assert('t' in ptkn)
        else:
            assert('t' not in ptkn)


def layer_tree_one__frst_split_period__then_rplc_t__other_rplc_r(txt):
    rm_t = partial(rm_char, char='t')
    rm_t_split = preiter_iter_postiter(iter_func=spliter, post_iter=rm_t)
    rm_t_split.__name__ = 'rm_t_split'
    rm_r = partial(rm_char, char='r')
    rm_r_split = preiter_iter_postiter(iter_func=spliter, post_iter=rm_r)
    rm_r_split.__name__ = 'rm_r_split'

    func = one_layer_tree(split_on, *[rm_t_split, rm_r_split])
    return func(txt)


RESONE = layer_tree_one__frst_split_period__then_rplc_t__other_rplc_r(SMPLTXT)


def test__one_layer_tree_one__frst_split_period__then_rplc_t__other_rplc_r():
    for tkn in RESONE['rm_t_split']:
        assert('t' not in tkn)
    for tkn in RESONE['rm_r_split']:
        assert('r' not in tkn)


def test__one_layer_tree_w_meta():
    smpl_1.uuid = 'one'
    smpl_2.uuid = 'two'
    smpl_3.uuid = 'three'
    assert(smpl_1.uuid == 'one')
    treefunc = one_layer_tree_w_meta(smpl_1, *[smpl_2, smpl_3])
    assert(treefunc.funcmeta == {'smpl_1': ('smpl_2', 'smpl_3')})


def test__one_layer_tree():
    def foo(stuff):
        return stuff
    tree_func = one_layer_tree(foo, smpl_1, smpl_2, smpl_3)
    res = tree_func('monkey')
    assert(tuple(res['smpl_1']) == ('monkey_one',))
    assert(tuple(res['smpl_2']) == ('monkey_two',))
    assert(tuple(res['smpl_3']) == ('monkey_three',))


def test__one_layer_tree__two():
    def foo(stuff):
        return stuff
    tree_func = one_layer_tree(foo, smpl_1, smpl_2, smpl_3)
    assert(tree_func.functors[0].__name__ == 'foo')
    assert(tree_func.functors[1][0].__name__ == 'smpl_1')
    assert(tree_func.functors[1][1].__name__ == 'smpl_2')
    assert(tree_func.functors[1][2].__name__ == 'smpl_3')


def test__one_layer_tree_w_meta__two():
    def foo(stuff):
        return stuff
    tree_func = one_layer_tree_w_meta(foo, smpl_1, smpl_2, smpl_3)
    res = tree_func('monkey')
    assert(tuple(res['smpl_1']) == ('monkey_one',))
    assert(tuple(res['smpl_2']) == ('monkey_two',))
    assert(tuple(res['smpl_3']) == ('monkey_three',))


def test__one_layer_tree_w_meta__three():
    def foo(stuff):
        return stuff
    tree_func = one_layer_tree_w_meta(foo, smpl_1, smpl_2, smpl_3)
    assert(tree_func.funcmeta == {'foo': ('smpl_1', 'smpl_2', 'smpl_3')})


def test__fork():
    forked = fork(smpl_1, smpl_2, smpl_3)
    output = forked('monkey')
    assert(tuple(output[0]) == ('monkey_one',))
    assert(tuple(output[1]) == ('monkey_two',))
    assert(tuple(output[2]) == ('monkey_three',))


if __name__ == '__main__':
    """
    test__presplit_split_postsplit__one__basic_spliter_only()
    test__presplit_split_postsplit__two__remove_t_pre_basic_split()
    test__presplit_split_postsplit__three__remove_t_post_basic_split()
    test__presplit_split_postsplit__four__remove_t_pre_basic_split_then_undo_in_post_split()
    test__one_layer_tree_one__frst_split_period__then_rplc_t__other_rplc_r()
    test__one_layer_tree_two()
    """
    test__one_layer_tree_one__frst_split_period__then_rplc_t__other_rplc_r()
    test__one_layer_tree_w_meta()
    test__one_layer_tree()
    test__one_layer_tree_w_meta__two()
    test__fork()
