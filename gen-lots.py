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


# Generate some random words

word_length = defaultdict(list)

for _ in range(0, 10000):
    word = gen_word()
    word_length[len(word)].append(word)

word_length[1] = one_chars

#for (wlen, wlist) in sorted(word_length.items()):
#    print(f'{wlen}: {len(wlist)}')

def key(a, b):
    return f'{a},{b}'

def unkey(key):
    return tuple(int(x) for x in key.split(","))

sentence = []

start = random.choices(
    list(sentence_start_lens.keys()),
    cum_weights=list(sentence_start_lens.values())
)
start = start[0]

#print(f'start={start}')

len1, len2 = unkey(start)
sentence.append(random.choice(word_length[len1]))
sentence.append(random.choice(word_length[len2]))
#print(sentence)

while True:
    len3 = random.choices(
        list(sentence_states[key(len1, len2)].keys()),
        list(sentence_states[key(len1, len2)].values())
    )
    len3 = len3[0]
    if len3 == ".":
        break
    len3 = int(len3)
    word = random.choice(word_length[len3])
    sentence.append(word)
    len1, len2 = len2, len3

#for _ in range(0, num_words):
#    while True:
#        try:
#            num_c = random.randint(0,4) + random.randint(0,4) + 2
#            sentence.append(random.choice(word_length[num_c]))
#            break
#        except IndexError:
#            pass
    

sentence[0] = sentence[0].capitalize()

sentence[-1] = sentence[-1] + "."

print(" ".join(sentence))
