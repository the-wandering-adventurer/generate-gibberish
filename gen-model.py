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

start_chars = defaultdict(int)
model = defaultdict(lambda: defaultdict(int))

for word in words:
    prev = word[0:2]
    start_chars[prev] += 1
    for c in word[2:]:
        model[prev][c] += 1
        prev = prev[1] + c
    model[prev]["."] += 1

for prev in model.keys():
    model[prev] = dict(
        accumulate(model[prev].items(), lambda a, b: (b[0], a[1] + b[1]))
    )

start_chars = dict(accumulate(start_chars.items(), lambda a, b: (b[0], a[1] + b[1])))

with gzip.open(sys.argv[2], "wt") as f:
    json.dump(
        dict(
            start_chars=start_chars,
            states=model,
        ),
        f,
    )
