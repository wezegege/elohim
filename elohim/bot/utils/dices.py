#!/usr/bin/env python
# -*- coding: utf-8 -*-


def dice_probability(size, dice_number, forbidden=None):
    def iteration(previous, values):
        result = dict()
        for value, count in previous:
            for index in values:
                total = value + index
                if total in result:
                    result[total] += count
                else:
                    result[total] = count
        return result

    forbidden = list() if forbidden is None else forbidden
    values = [number for number in range(1, size + 1) if not number in forbidden]
    probabilities = dict()
    indexes = [(0, 1)]
    for number in range(1, dice_number + 1):
        iteration_probs = iteration(indexes, values)
        total = size ** number
        probabilities[number] = [(value, count / total) for value, count in iteration_probs.items()]
        indexes = iteration_probs.items()
    return probabilities


