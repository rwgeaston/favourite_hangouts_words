# -*- coding: utf-8 -*-
from constants import minimum_tally_to_care, words_to_display


def find_relative_most_popular(word_counts, reference_counts):
    common_words = [
        (word, count) for word, count in word_counts.iteritems()
        if count > minimum_tally_to_care
    ]
    ratios = [(get_ratio(word, count, reference_counts), word) for word, count in common_words]
    ratios.sort(reverse=True)
    max_to_keep = ratios[:words_to_display]
    # Don't bother with things that have a ratio that rounds to 0
    return [word for word in max_to_keep if word[0] >= 0.05]


def get_ratio(word, count, reference_counts_combined):
    if not isinstance(reference_counts_combined, dict):
        print type(reference_counts_combined)
        print len(reference_counts_combined)
    if word not in reference_counts_combined:
        return '(inf)'
    return round(float(count) / reference_counts_combined[word], 1)


def format_common_words(tallies):
    return u', '.join([u'"{}" {}'.format(word, tally) for tally, word in tallies])


def combine_counts(list_of_counts):
    combined = {}
    for word_count in list_of_counts:
        for word, count in word_count.iteritems():
            if word not in combined:
                combined[word] = 0
            combined[word] += count
    return combined
