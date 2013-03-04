#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Markov algorithms for AI computing
"""

import copy
import sys
import math


def value_iteration(sizes, epsilon, action_probs, verbose=False):
    """Variant of the Markov process to compute probabilities
    """

    def loop_dimensions(sizes):
        """Iterate through the differents axis of the problem
        """
        dimensions = list(reversed(sizes))
        def iterate(dimensions, parents=None):
            """Iterative function to loop through the dimensions
            """
            parents = list() if parents is None else parents
            for i in range(dimensions[0](*parents)):
                if len(dimensions) > 1:
                    for indexes in iterate(dimensions[1:],
                            parents + [i]):
                        yield [i] + indexes
                else:
                    yield [i]

        for indexes in iterate(dimensions):
            yield indexes

    def get_value(container, indexes):
        """Get value for a field of the state matrix
        """
        result = container
        for index in indexes:
            result = result[index]
        return result

    def set_value(container, indexes, value):
        """Set value for a field of the state matrix
        """
        result = container
        for index in indexes[:-1]:
            result = result[index]
        result[indexes[-1]] = value
        return result

    def compute_diffs(sizes, old, new):
        """Measure the distance between the state matrix before and after
        an iteration
        """
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
        """Initialize the state matrix
        """
        if dimensions:
            probabilities = list()
            interest = list()
            for _ in range(size):
                subp, subinterest = init_arrays(size, dimensions - 1)
                probabilities.append(subp)
                interest.append(subinterest)
        else:
            probabilities = [0.0] * size
            interest = [None] * size
        return probabilities, interest


    probabilities, interest = init_arrays(sizes[0](), len(sizes) - 1)

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
            old_prob = get_value(probabilities, indexes)
            probs = action_probs(indexes, probabilities)
            best_action, best_prob = max(probs, key=lambda x: x[1])
            set_value(probabilities, indexes, best_prob)
            set_value(interest, indexes, best_action)
            max_change = max(max_change, math.fabs(best_prob - old_prob))
    return interest


