# -*- coding: utf-8 -*-
__title__ = 'fnctional'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__copyright__ = "fnctional  Copyright (C) 2015  Steven Cutting"
__created_on__ = '8/27/2015'

from fnctional.__about__ import *

from functools import partial
from collections import defaultdict


from fnctional.utils import pass_through, always_true, _try_custom_name, _try_custom_doc


# ------------------------------------------------------------------------------
# simple transducer
def _run_if_not_none(proc, **bldargs):
    def rinn(arg, nxt_proc=pass_through, **runargs):
        # does not allow for runargs to override bldargs.
        runargs.update(bldargs)
        return nxt_proc(proc(arg, **runargs), **runargs)
    return rinn


def trnsdcr(procs, mdl_fnc=_run_if_not_none, **xargs):
    """
    a simple transducer.

    procs - a list of functions to be composed.
    """
    # TODO (steven_c) checkout functools.wraps
    # TODO (steven_c) add auto doc gen.
    if len(procs) == 1:
        return mdl_fnc(proc=procs[0], **xargs)
    else:
        new_proc = mdl_fnc(proc=procs[0], **xargs)
        return partial(new_proc,
                       nxt_proc=trnsdcr(procs[1:],
                                        **xargs))


# ------------------------------------------------------------------------------
# other transducers

def one_layer_tree_trnsdcr(head_op, *branch_ops, **bldargs):
    """
    ex:
        head_op - parses sentences.
        branch_ops - a list of 'tokenizers' that will tokenize the sentences in different ways.
        postdictmod - mods the result dict before returning it.
    It will return something like this:
        setsdict = {'setone': ['t1', 't2', ..., 'tn'],
                    'settwo': ['t1', 't2', ..., 'tn'],
                    }
    """
    def tree_func(operand, *_, **runargs):
        runargs.update(bldargs)
        posteriordict = defaultdict(list)
        for res in head_op(operand, *_, **runargs):
            for b_op in branch_ops:
                #  Assumes each branch function will have a differant name.
                #  Could end up being a big problem.
                posteriordict[b_op.__name__].extend(b_op(res))
        return dict(posteriordict)
    tree_func.__name__ = _try_custom_name(fnc=tree_func, **bldargs)
    return tree_func


def preiter_iter_postiter(iter_fnc, pre_iter=pass_through, post_iter=pass_through,
                          iter_bool=always_true, **bldargs):
    """
    pre_iter - a function that modifies the incoming operand.
    iter_fnc - a function the splits the operand.
    post_iter - a function that modifies the iterated objs.
    iter_bool - decides if an objs should be used. a function that accepts an obj and returns
                True or False.
    """
    def iter_and_op(txt, **runargs):
        runargs.update(bldargs)
        for i, split in enumerate(iter_fnc(pre_iter(txt, **runargs), **runargs)):
            modedsplit = post_iter(split, **runargs)
            if iter_bool(modedsplit, **runargs):
                yield modedsplit
    iter_and_op.__name__ = _try_custom_name(fnc=iter_and_op, **bldargs)
    iter_and_op.__doc__ = _try_custom_doc(fnc=iter_and_op, **bldargs)
    return iter_and_op
