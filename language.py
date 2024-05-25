#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides functions to detect the language of a text as well as
checking the linguistic typicity of a text

Created on 2024-05-25 13:38:11

Author: Infinity Coding
"""
import os
from typing import Dict, List, Optional, Iterator
from collections import Counter
from json import load

def _get_available_languages() -> Iterator[str]:
    """
    Get a all available languages, that are found in the frequency_tables folder.

    :yield: The name of the language.
    """
    for file_name in os.listdir('frequency_tables'):
        if file_name.endswith('.json'):
            yield file_name[:-5]


def detect_language(text: str, languages: Optional[List[str]] = None) -> Dict[str, float]:
    """
    Detect the language of a text based on the frequency of the characters.

    :param text: The text to analyze.
    :param languages: A list of languages to compare the text with. Default is None, which will use all
    available languages. If given language is not available, it will be ignored.
    :return: A dictionary with the languages as keys and the similarity to the text as values (1 is best).
    """
    if languages is None:
        languages = list(_get_available_languages())

    # load the frequency tables for the languages
    frequency_tables = {}
    for language in languages:
        with open(f'frequency_tables/{language}.json', 'r') as fr:
            frequency_tables[language] = load(fr)

    text_frequency = Counter(text.lower())
    text_length = len(text)

    # calculate the similarity to each language
    similarities = {}
    for language, frequency_table in frequency_tables.items():
        similarity = 0
        for char, frequency in frequency_table.items():
            if char in text_frequency:
                similarity += abs(frequency - text_frequency[char]) / text_length
        similarities[language] = 1 - similarity

    return similarities


def is_typical(text: str, language: str, threshold: int = 0.4) -> bool:
    """
    Check if a text is typical for a language based on the frequency of the characters.

    :param text: The text to analyze.
    :param language: The language to compare the text with.
    :param threshold: The threshold for the similarity to the language. Default is `0.4`.
    :return: True if the text is typical for the language, False otherwise.
    """
    if language not in _get_available_languages():
        raise ValueError(f"Language '{language}' is not available")

    with open(f'frequency_tables/{language}.json', 'r') as fr:
        frequency_table = load(fr)

    text_frequency = Counter(text.lower())
    text_length = len(text)

    similarity = 0
    for char, frequency in frequency_table.items():
        if char in text_frequency:
            similarity += abs(frequency - text_frequency[char]) / text_length

    return (1 - similarity) > threshold

if __name__ == '__main__':
    text = 'This is a test text to check the language detection.'
    print(detect_language(text))
    print("Most likely language:", max(detect_language(text), key=detect_language(text).get).capitalize())