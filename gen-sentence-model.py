#!/usr/bin/env python3
from collections import defaultdict
from itertools import accumulate, groupby
import gzip
import json
import re
import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

words = [re.sub(r"[^\w.]", "", w) for l in lines for w in l.split()]
words = [w for w in words if len(w) > 0]

start_lens = defaultdict(int)
model = defaultdict(lambda: defaultdict(int))

# print(words)

sentence_id = 1


def break_sentence(word):
    global sentence_id
    if word[-1] == ".":
        old = sentence_id
        sentence_id += 1
        return old
    else:
        return sentence_id


def key(a, b):
    return f"{a},{b}"


for _, sentence_iter in groupby(words, break_sentence):
    sentence = list(sentence_iter)
    if len(sentence) <= 1:
        continue
    len1, len2 = tuple(len(w) for w in sentence[0:2])
    start_lens[key(len1, len2)] += 1
    for word in sentence[2:]:
        len3 = len(word)
        if word[-1] == ".":
            len3 -= 1
        model[key(len1, len2)][len3] += 1
        len1, len2 = len2, len3
    model[key(len1, len2)]["."] += 1


for context in model.keys():
    model[context] = dict(
        accumulate(model[context].items(), lambda a, b: (b[0], a[1] + b[1]))
    )

start_lens = dict(accumulate(start_lens.items(), lambda a, b: (b[0], a[1] + b[1])))

with gzip.open(sys.argv[2], "wt") as f:
    json.dump(dict(start_lens=start_lens, states=model), f)
