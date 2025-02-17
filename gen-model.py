#!/usr/bin/env python3
from collections import defaultdict
from itertools import accumulate
import gzip
import json
import re
import sys

with open(sys.argv[1]) as f:
    words = f.read().splitlines()

# Filter out:
# (1) Words w/ non-alpha characters (like ')
# (2) Words that have capital letters (they are likely names)
# (3) One/Two character words (these tend to be junk in many dictionaries I've used)

words = [w for w in words if re.match(r"^\w+$", w) and w.islower() and len(w) > 2]

# We are going to keep track of
#
# - start_chars: The first two characters of every word.
#   These will be the "starter" characters when generating a word.
#
# - model: The Markov chain model.
#   The model is two-level dictionary.
#   The first key is the two char combo that forms the current state.
#   The second key is a possible next character.
#   For example:
#       model["ee"]["n"] = 5
#   means we have encountered the letter "n" after "ee" five times in our
#   dictionary of words.

start_chars = defaultdict(int)
model = defaultdict(lambda: defaultdict(int))

# Go through each word in the dictionary to develop the model
for word in words:
    # The first two chars of the word form our starting point
    context = word[0:2]

    # Save off the fact these two chars start a word
    start_chars[context] += 1

    # Step through the rest of the word, building the model
    for c in word[2:]:
        model[context][c] += 1
        context = context[1] + c

    # Save off that we've reached the end of a word
    # using "." as the end-of-word marker.
    model[context]["."] += 1

# This step isn't completely necessary. We want to provide a probability
# distribution for random.choices. Using cumulative weights saves work for
# that function.

for context in model.keys():
    model[context] = dict(
        accumulate(model[context].items(), lambda a, b: (b[0], a[1] + b[1]))
    )

start_chars = dict(accumulate(start_chars.items(), lambda a, b: (b[0], a[1] + b[1])))

# Save the model of gzip'd JSON

with gzip.open(sys.argv[2], "wt") as f:
    json.dump(
        dict(
            start_chars=start_chars,
            states=model,
        ),
        f,
    )
