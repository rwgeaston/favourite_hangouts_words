# -*- coding: utf-8 -*-
from json import loads
import codecs

from hangouts_parser import get_word_counts
from facebook_parser import facebook_get_all_word_counts
from relative_popularity import find_relative_most_popular, format_common_words, combine_counts
from constants import my_name, word_count_to_be_an_interesting_person, hangouts_source, facebook_source

word_counts = {}

if hangouts_source:
    with codecs.open(hangouts_source, encoding='utf-8') as logs_file:
        logs_txt = logs_file.read()

    all_chats = loads(logs_txt)
    del logs_txt

    # This has two keys [u'continuation_end_timestamp', u'conversation_state']
    # all_chats['conversation_state'] is a list of conversations

    for chat in all_chats[u'conversation_state']:
        should_keep, participants, word_counts_this_chat = get_word_counts(chat['conversation_state'])
        if should_keep:
            word_counts[participants] = word_counts_this_chat

    del chat
    del all_chats

if facebook_source:
    with codecs.open(facebook_source, encoding='utf-8') as logs_file:
        facebook_logs_txt = logs_file.read()

    more_word_counts = facebook_get_all_word_counts(facebook_logs_txt)
    del facebook_logs_txt

    for chat, counts in more_word_counts.iteritems():
        if chat in word_counts:
            for name, count in counts.iteritems():
                if name in word_counts[chat]:
                    word_counts[chat][name] = combine_counts([word_counts[chat][name], count])
                else:
                    word_counts[chat][name] = count
        else:
            word_counts[chat] = counts

    del more_word_counts

me = []
others = []

for chat in word_counts.itervalues():
    for person, count in chat.iteritems():
        if person == my_name:
            me.append(count)
        else:
            others.append(count)

my_word_counts = combine_counts(me)
others_counts = combine_counts(others)

output_file = open('output.txt', 'w')


def write(string):
    output_file.write(string + '\n')
    print string


def display_most_popular(word_counts, reference_counts):
    write(format_common_words(
        find_relative_most_popular(word_counts, reference_counts)
    ))


def total_size(conversation):
    return sum([len(tally) for tally in conversation.itervalues()])

write("Words I say more often than my friends.")
display_most_popular(my_word_counts, others_counts)

write("\nWords they say more often.")
display_most_popular(others_counts, my_word_counts)

for name, conversation in word_counts.iteritems():
    if total_size(conversation) > word_count_to_be_an_interesting_person:

        others_this_chat = []
        for person, count in conversation.iteritems():
            if person != my_name:
                others_this_chat.append(count)
        combined_this_chat = combine_counts(others_this_chat)

        write("\nWords I say more often to {} than they say to me.".format(name))
        display_most_popular(conversation[my_name], combined_this_chat)
        write("\nWords {} says more often to me.".format(name))
        display_most_popular(combined_this_chat, conversation[my_name])
        write("\nWords I say more often to {} than I say in general.".format(name))
        display_most_popular(conversation[my_name], my_word_counts)

output_file.close()
