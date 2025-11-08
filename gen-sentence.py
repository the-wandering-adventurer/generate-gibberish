#!/usr/bin/env python3
from collections import defaultdict
import gzip
import json
import random
import sys

# Load the gzip'd JSON Markov chain
with gzip.open(sys.argv[1], "rt") as f:
    model = json.load(f)

with gzip.open(sys.argv[2], "rt") as f:
    sentence_model = json.load(f)

# Extract the states and starting characters into global variables
# (Just for easier reading down the road).
states = model["states"]
start_chars = model["start_chars"]
one_chars = model["one_chars"]

sentence_states = sentence_model["states"]
sentence_start_lens = sentence_model["start_lens"]


def gen_word():
    # Grab two random characters from the starter set
    word = random.choices(
        list(start_chars.keys()), cum_weights=list(start_chars.values())
    )
    # random.choices always returns a list, even if you only want one element
    word = word[0]

    # Now use the chain to generate a word
    while True:
        # Grab the last two characters of the word to use as our context
        key = word[-2:]

        # If the key is in our chain, then grab the next character at random
        if key in states:
            next_char = random.choices(
                list(states[key].keys()), cum_weights=list(states[key].values())
            )
            next_char = next_char[0]
        else:
            # The key isn't in the chain - we've reached the end
            break
        if next_char == ".":
            # The "." is a special marker for end-of-word
            break

        # We've gotten this far, add the character to the word and keep going
        word += next_char
    return word


# Generate some random words for our sentence
# Store the words by word length

word_length = defaultdict(list)

for _ in range(0, 10000):
    word = gen_word()
    word_length[len(word)].append(word)

word_length[1] = one_chars


# The key two our sentence model relies
# on the length of the last two words
def key(a, b):
    return f"{a}:{b}"


# Revert a key in our sentence model
# to the two word lengths, or the special
# punctuation markers of "," and "."
def unkey(key):
    return tuple(int(x) if x not in ",." else x for x in key.split(":"))


# Add a word to our sentence. If "length" is
# a string, that means it's punctuation, so just append it.
# Otherwise pick a word from our pre-generated list of words.
def add_word(length):
    if isinstance(length, str):
        sentence.append(length)
    else:
        sentence.append(random.choice(word_length[length]))

# Start our sentence, by getting starting word lengths
sentence = []

start = random.choices(
    list(sentence_start_lens.keys()), cum_weights=list(sentence_start_lens.values())
)
start = start[0]

# Generate the first two random words
len1, len2 = unkey(start)
add_word(len1)
add_word(len2)

# While we haven't encountered a period (ending our sentence),
#   keep adding new words
while len2 != ".":
    # Decide on the length of the next word
    len3 = random.choices(
        list(sentence_states[key(len1, len2)].keys()),
        list(sentence_states[key(len1, len2)].values()),
    )
    len3 = len3[0]
    len3 = int(len3) if len3 not in ",." else len3
    add_word(len3)
    len1, len2 = len2, len3

# for _ in range(0, num_words):
#    while True:
#        try:
#            num_c = random.randint(0,4) + random.randint(0,4) + 2
#            sentence.append(random.choice(word_length[num_c]))
#            break
#        except IndexError:
#            pass


sentence[0] = sentence[0].capitalize()

print(" ".join(sentence).replace(" ,", ",").replace(" .", "."))
