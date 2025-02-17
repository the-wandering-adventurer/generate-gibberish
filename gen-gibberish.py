#!/usr/bin/env python3
import gzip
import json
import random
import sys

# Load the gzip'd JSON Markov chain
with gzip.open(sys.argv[1], "rt") as f:
    model = json.load(f)

# Extract the states and starting characters into global variables
# (Just for easier reading down the road).
states = model["states"]
start_chars = model["start_chars"]


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
num_words = random.randint(1, 4) + random.randint(1, 4) + 1
sentence = [gen_word() for _ in range(0, num_words)]
print(" ".join(sentence))
