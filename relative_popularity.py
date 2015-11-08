# -*- coding: utf-8 -*-
from constants import minimum_tally_to_care


def find_relative_most_popular(word_counts, reference_counts):
    common_words = [
        (word, count) for word, count in word_counts.iteritems()
        if count > minimum_tally_to_care
    ]
    ratios = [(get_ratio(word, count, reference_counts), word) for word, count in common_words]
    ratios.sort(reverse=True)
    return ratios[:35]


def get_ratio(word, count, reference_counts_combined):
    if not isinstance(reference_counts_combined, dict):
        print type(reference_counts_combined)
        print len(reference_counts_combined)
    if word not in reference_counts_combined:
        return '(inf)'
    return round(float(count) / reference_counts_combined[word], 1)


def format_common_words(tallies):
    return u', '.join([u'"{}" {}'.format(word, tally) for tally, word in tallies])
