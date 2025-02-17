#!/usr/bin/env python3
import gzip
import json
import random
import sys

with gzip.open(sys.argv[1], "rt") as f:
    model = json.load(f)

states = model["states"]
start_chars = model["start_chars"]


def gen_word():
    word = random.choices(
        list(start_chars.keys()), cum_weights=list(start_chars.values())
    )
    word = word[0]
    while True:
        key = word[-2:]
        if key in states:
            next_char = random.choices(
                list(states[key].keys()), cum_weights=list(states[key].values())
            )
            next_char = next_char[0]
        else:
            break
        if next_char == ".":
            break
        word += next_char
    return word

num_words = random.randint(1, 4) + random.randint(1, 4) + 1
sentence = [gen_word() for _ in range(0, num_words)]
print(" ".join(sentence))
