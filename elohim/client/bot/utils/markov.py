#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import sys
import math


def value_iteration(sizes, epsilon, action_probs, verbose=False):

    def loop_dimensions(sizes):
        dimensions = list(reversed(sizes))
        def iterate(dimensions, parents=None):
            parents = list() if parents is None else parents
            for a in range(dimensions[0](*parents)):
                if len(dimensions) > 1:
                    for indexes in iterate(dimensions[1:],
                            parents + [a]):
                        yield [a] + indexes
                else:
                    yield [a]

        for indexes in iterate(dimensions):
            yield indexes

    def get_value(container, indexes):
        result = container
        for index in indexes:
            result = result[index]
        return result

    def set_value(container, indexes, value):
        result = container
        for index in indexes[:-1]:
            result = result[index]
        result[indexes[-1]] = value
        return result

    def compute_diffs(sizes, old, new):
        result = 0
        for indexes in loop_dimensions(sizes):
            try:
                result += math.fabs(get_value(old, indexes) -
                        get_value(new, indexes))
            except (ValueError, TypeError):
                result += math.fabs(int(get_value(old, indexes) ==
                    get_value(new, indexes)))
        return result

    def init_arrays(size, dimensions):
        if dimensions:
            p = list()
            interest = list()
            for a in range(size):
                subp, subinterest = init_arrays(size, dimensions - 1)
                p.append(subp)
                interest.append(subinterest)
        else:
            p = [0.0] * size
            interest = [None] * size
        return p, interest


    p, interest = init_arrays(sizes[0](), len(sizes) - 1)

    if verbose:
        iterations = 0
        diffs = None
    max_change = 1.0
    old_interest = None

    while max_change > epsilon:
        if verbose:
            if old_interest:
                diffs = compute_diffs(sizes, interest, old_interest)
            old_interest = copy.deepcopy(interest)
            iterations += 1
            sys.stderr.write(str((iterations, max_change, diffs)) + '\n')
            sys.stderr.flush()
        max_change = 0.0

        for indexes in loop_dimensions(sizes):
            old_prob = get_value(p, indexes)
            probs = action_probs(indexes, p)
            best_action, best_prob = max(probs, key=lambda x: x[1])
            set_value(p, indexes, best_prob)
            set_value(interest, indexes, best_action)
            max_change = max(max_change, math.fabs(best_prob - old_prob))
    return interest


