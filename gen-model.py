#!/usr/bin/env python3
from collections import defaultdict
from itertools import accumulate
import base64
import gzip
import json
import re
import sys

with open(sys.argv[1]) as f:
    words = f.read().splitlines()

words = [w for w in words if re.match(r"^\w+$", w) and w.islower()]

one_char_words = [w for w in words if len(w) == 1]
two_char_words = [w for w in words if len(w) == 2]
start_chars = []
model = defaultdict(lambda: defaultdict(int))

for word in [w for w in words if len(w) > 2]:
    prev = word[0:2]
    start_chars.append(prev)
    for c in word[2:]:
        model[prev][c] += 1
        prev = prev[1] + c

for prev in model.keys():
    model[prev] = dict(
        accumulate(model[prev].items(), lambda a, b: (b[0], a[1] + b[1]))
    )

json = json.dumps(
    dict(
        one_char_words=one_char_words,
        two_char_words=two_char_words,
        start_chars=start_chars,
        states=model,
    )
)
model_encoded = base64.b64encode(gzip.compress(json.encode()))

print(model_encoded.decode())
