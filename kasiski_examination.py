#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides functions to perform a Kasiski examination on a
text to find the most likely key lengths of a Vigenère cipher.

Created on 2024-05-20 11:37:36

Author: InfnityCoding
"""
from typing import List, Dict, Optional
from heapq import nlargest

def find_repeat_sequences(text: str, min_length: int = 3) -> Dict[str, List[int]]:
    """
    Find all repeated sequences in a text with a length between min_length and the half of the text length.

    :param text: The text to search for repeated sequences.
    :param min_length: The minimum length of the repeated sequence. Default is 3. Must be at least 2 and smaller
    than the half of the text length.
    :return: A dictionary with the repeated sequences as keys and a list of their positions in the text as values.
    """
    sequences = {}

    # check if min_length is at least 2 and smaller than the half of the text length
    if min_length < 2 or min_length >= len(text) // 2:
        raise ValueError("min_length must be at least 2 and smaller than the half of the text length")

    # create a dictionary with all sequences and their occurrences
    for length in range(min_length, len(text) // 2 + 1):
        for i in range(len(text) - length):
            sequence = text[i:i + length]
            if sequence in sequences:
                sequences[sequence].append(i)
            else:
                sequences[sequence] = [i]

    # return only sequences with more than one occurrence
    return {sequence: positions for sequence, positions in sequences.items() if len(positions) > 1}


def get_spaces(sequences: dict) -> List[int]:
    """
    Find the spaces between the repeated sequences.

    :param sequences: A dictionary with the repeated sequences as keys and a list of their positions in the text as values.
    :return: A list with the spaces between the repeated sequences.
    """
    spaces = []
    for positions in sequences.values():
        for i in range(len(positions) - 1):
            spaces.append(positions[i + 1] - positions[i])

    return spaces


def find_factors(number: int) -> set:
    """
    Find all factors of a number, excluding 1.

    :param number: The number to find the factors of. Must be greater than 1.
    :return: A set with all factors of the number.
    """
    if number <= 1:
        raise ValueError("number must be greater than 1")

    i, factors = 2, set()
    while i*i <= number:
        if number % i == 0:
            factors.add(i)
            factors.add(number // i)
        i += 1

    factors.add(number)

    return factors


def find_key_lengths(spaces: list, n: Optional[int] = None) -> List[tuple[int, int]]:
    """
    Find the most likely key lengths of a vignere cipher.

    :param sequences: A list containing the spaces between the repeated sequences.
    :param n: The number of key lengths to return. If None, all key lengths are returned.
    :return: A list of tuples with the key lengths and their occurrences, sorted from most likely to least likely.
    """
    # calculate all factors of the spaces
    factors = []
    for distance in spaces:
        factors.extend(find_factors(distance))

    # count the occurrences of the factors
    key_lengths = dict()
    for factor in factors:
        key_lengths[factor] = key_lengths.get(factor, 0) + 1

    # return the n most likely key lengths
    if n is None:
        return sorted(key_lengths.items(), key=lambda x: x[1], reverse=True)

    return nlargest(n, key_lengths.items(), key=lambda x: x[1])


if __name__ == "__main__":
    text = "PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAGVOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU"

    print("Most likely key lengths: ", find_key_lengths(get_spaces(find_repeat_sequences(text)), 3))