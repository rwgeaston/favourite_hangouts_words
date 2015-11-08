from copy import copy
from constants import hardcoded_participants, name_mapping, my_name


def unsafe_get(dictionary, element):
    if element not in dictionary:
        raise KeyError(
            "Couldn't find the key {} in dictionary with keys {}."
            .format(element, dictionary.keys())
        )
    return dictionary[element]


def get_word_counts(chat_log):
    network_type = chat_log['conversation']['network_type']
    if 'PHONE' in network_type:
        # These are all too small to bother working out how to parse
        return False, None, None
    messages = chat_log['event']

    participants = get_participant_mapping(chat_log)
    active_participants = {}

    for message in messages:
        gaia_id = message['sender_id']['gaia_id']
        if message['event_type'] != 'REGULAR_CHAT_MESSAGE':
            continue
        try:
            elements = message['chat_message']['message_content']
        except KeyError:
            print "Couldn't find a key in {}".format(repr(message))
            raise
        if len(elements.keys()) == 1 and 'attachment' in elements:
            # I think this means it's a photo.
            continue
        text = unsafe_get(elements, 'segment')[0]['text']
        if gaia_id not in participants:
            raise KeyError(
                "Do not recognise this ID: {}\nI know these IDs: {}\nMessage: {}"
                .format(gaia_id, participants, message)
            )
        participant = participants[gaia_id]
        if participant not in active_participants:
            active_participants[participant] = {}
        update_word_counts(active_participants[participant], text)

    participant_names = active_participants.keys()
    participant_names.remove(my_name)
    conversation_name = ','.join(sorted(participant_names))

    return True, conversation_name, active_participants


def update_word_counts(current_word_counts, new_message):
    for word in new_message.split():
        insensitive = word.lower()
        insensitive = insensitive.strip(',.?:"')
        if insensitive not in current_word_counts:
            current_word_counts[insensitive] = 0
        current_word_counts[insensitive] += 1


def get_participant_mapping(chat_log):
    participants = copy(hardcoded_participants)
    for participant in unsafe_get(chat_log, 'conversation')['participant_data']:
        if 'fallback_name' in participant:
            name = participant['fallback_name']
            if name in name_mapping:
                friendly_name = name_mapping[name]
            else:
                friendly_name = name
            participants[participant['id']['gaia_id']] = friendly_name
    return participants
