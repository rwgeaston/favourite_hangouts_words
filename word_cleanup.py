import unicodedata


emoticons = [':)', '(;', ':(', ':P', ':D']
# I'm not interested in whether one person types apostrophes and another doesn't
special_cases = {
    "wouldnt": "wouldn't",
    "wasnt": "wasn't",
    "ive": "i've",
    "hte": "the",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "thats": "that's",
    "im": "i'm",
    "dont": "don't",
    "anythnig": "anything",
    "somethnig": "something",
    "shouldnt": "shouldn't",
    "modafanil": "modafinil",
    "arent": "aren't",
    "wont": "won't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "kirstens": "kirsten's",
    "isnt": "isn't",
    "whats": "what's",
    "cant": "can't",
    "couldnt": "couldn't"
}

html_replacement = {
    '&#039;': "'",
    '&lt;': '<',
    '&gt;': '>',
    '&quot;': '"',
}

def cleanup_word(word):
    if word in emoticons:
        # Don't start stripping off colons or parens if they're part of the word
        return word
    improved = word.lower()
    for character, mapping in html_replacement.iteritems():
        improved = improved.replace(character, mapping)
    improved = improved.strip(',.?":()')
    improved = unicodedata.normalize('NFKD', improved)
    improved = improved.encode('ascii', 'replace')
    return special_cases.get(improved, improved)
