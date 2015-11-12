from relative_popularity import combine_counts
from constants import my_name
from word_cleanup import cleanup_word

def facebook_get_all_word_counts(messages_html):
    conversations = messages_html.split('<div class="thread">')[1:]
    all_word_counts = {}
    for conversation in conversations:
        names, word_counts = parse_conversation(conversation)
        if names in all_word_counts:
            for person, words in word_counts.iteritems():
                if person in all_word_counts[names]:
                    all_word_counts[names][person] = combine_counts(
                        [all_word_counts[names][person], words]
                    )
                else:
                    all_word_counts[names][person] = words
        else:
            all_word_counts[names] = word_counts

    return all_word_counts

def parse_conversation(conversation):
    word_counts = {}
    messages = conversation.split('<div class="message">')[1:]
    for message in messages:
        name, words = parse_message(message)
        if name not in word_counts:
            word_counts[name] = {}
        for word in words:
            word = cleanup_word(word)
            if word not in word_counts[name]:
                word_counts[name][word] = 0
            word_counts[name][word] += 1

    other_users_list = word_counts.keys()
    if my_name in other_users_list:
        other_users_list.remove(my_name)
    else:
        # I didn't speak
        pass

    other_users_list.sort()
    if not other_users_list:
        # I'm the only person who spoke
        other_users_list.append("Never Responded")
    conversation_name = ', '.join(other_users_list)

    return conversation_name, word_counts


def parse_message(message):
    user = message.split('<span class="user">')[1].split('</span>')[0]
    text = message.split('<p>')[1].split('</p>')[0]
    words = text.split()
    return user, words
