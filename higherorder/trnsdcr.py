# -*- coding: utf-8 -*-
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__copyright__ = "higherorder  Copyright (C) 2015  Steven Cutting"
__created_on__ = '8/27/2015'

from higherorder.__about__ import *

from functools import partial
from collections import defaultdict, namedtuple
from copy import copy

from higherorder import utils
from higherorder.utils import(pass_through,
                              always_true,
                              _try_assign_name,
                              _try_assign_doc,
                              get_attr,
                              flatten_all_if_true)

__all__ = ['trnsdcr', 'one_layer_tree', 'one_layer_tree_w_meta', 'preiter_iter_postiter']


# ------------------------------------------------------------------------------
# simple transducer
def _run_if_not_none(proc, **bldargs):
    def rinn(arg, nxt_proc=pass_through, **runargs):
        # does not allow for runargs to override bldargs.
        runargs.update(bldargs)
        return nxt_proc(proc(arg, **runargs), **runargs)
    return rinn


def trnsdcr(procs, mdl_func=_run_if_not_none, **xargs):
    """
    a simple transducer.

    procs - a list of functions to be composed.
    """
    # TODO (steven_c) checkout functools.wraps
    # TODO (steven_c) add auto doc gen.
    if len(procs) == 1:
        return mdl_func(proc=procs[0], **xargs)
    else:
        new_proc = mdl_func(proc=procs[0], **xargs)
        return partial(new_proc,
                       nxt_proc=trnsdcr(procs[1:],
                                        **xargs))


# ------------------------------------------------------------------------------
# other transducers


def fork(*functors, **bldargs):
    """
    Accepts a bunch of functions and creates a new function that will
    pass it's arguments on to each of the original functions.

    If you want to customize the resulting functions attributes check out:
        higherorder.utils.prepend_to_func_attrs
    """
    def fork_run(operand, *_, **runargs):
        bldargs.update(runargs)  # bldargs can be overwritten at runtime
        # fnctrs = copy(functors)

        def inner(func):
            for op in flatten_all_if_true(operand, **bldargs):
                yield func(op, **bldargs)

        output = tuple(map(inner, functors))
        return output
    fork_run.functors = functors
    return fork_run


def one_layer_tree(head_op, *branch_ops, **bldargs):
    """
    - Uses names of functions as key names
        - if the key names should come from some other attribute of the functions
          then pass the name of the attribute using the attr key word.
    - flatten - True - if True the data structure produced by the head_op will be flattened.
    ex:
        head_op - parses sentences.
        branch_ops - a list of 'tokenizers' that will tokenize the sentences in different ways.
    It will return something like this:
        setsdict = {'setone': ['t1', 't2', ..., 'tn'],
                    'settwo': ['t1', 't2', ..., 'tn'],
                    }
    """
    branch_func = fork(*branch_ops, **bldargs)

    def tree_func(operand, *_, **runargs):
        bldargs.update(runargs)
        firstlayerres = list(flatten_all_if_true(head_op(operand, *_, **bldargs),
                                                 **bldargs))
        output = branch_func(firstlayerres)
        return {get_attr(func, **bldargs): out
                for func, out in zip(branch_ops, output)}
    tree_func.__name__ = _try_assign_name(func=tree_func, **bldargs)
    tree_func.functors = (head_op, tuple(branch_ops))
    return tree_func


@utils.append_to_func_attrs(__doc__=''.join(['\n', '-' * 10, '\n',
                                             one_layer_tree.__doc__]))
def one_layer_tree_w_meta(head_op, *branch_ops, **bldargs):
    """
    TODO
    """
    funcmeata = {get_attr(head_op, **bldargs): tuple([get_attr(b_op, **bldargs)
                                                     for b_op in branch_ops])}
    tree_func = one_layer_tree(head_op, *branch_ops, **bldargs)
    tree_func.funcmeta = funcmeata
    return tree_func


def preiter_iter_postiter(iter_func, pre_iter=pass_through, post_iter=pass_through,
                          iter_bool=always_true, *_, **bldargs):
    """
    pre_iter - a function that modifies the incoming operand.
    iter_func - a function the splits the operand.
    post_iter - a function that modifies the iterated objs.
    iter_bool - decides if an objs should be used. a function that accepts an obj and returns
                True or False.
    """
    def iter_and_op(txt, **runargs):
        runargs.update(bldargs)
        for i, split in enumerate(iter_func(pre_iter(txt, **runargs), **runargs)):
            modedsplit = post_iter(split, **runargs)
            if iter_bool(modedsplit, **runargs):
                yield modedsplit
    iter_and_op.__name__ = _try_assign_name(func=iter_and_op, **bldargs)
    iter_and_op.__doc__ = _try_assign_doc(func=iter_and_op, **bldargs)
    return iter_and_op
