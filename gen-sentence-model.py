#!/usr/bin/env python3
from collections import defaultdict
from itertools import accumulate, groupby
import gzip
import json
import re
import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

words = []
for l in lines:
    for w in filter(lambda x: x, re.split(r" +|([.,])", l)):
        words.append(re.sub(r"[^\w.,]", "", w))

start_lens = defaultdict(int)
model = defaultdict(lambda: defaultdict(int))


sentence_id = 1


def break_sentence(word):
    global sentence_id
    if word == ".":
        old = sentence_id
        sentence_id += 1
        return old
    else:
        return sentence_id


def key2(a, b):
    ka = a if a in ",." else len(a)
    kb = b if b in ",." else len(b)
    return f"{ka}:{kb}"


def key(a):
    ka = a if a in ",." else len(a)
    return f"{ka}"


for _, sentence_iter in groupby(words, break_sentence):
    sentence = list(sentence_iter)
    if len(sentence) <= 1:
        continue
    word1, word2 = sentence[0:2]
    if word1 in ",.":
        print(sentence)
        sys.exit(1)
    start_lens[key2(word1, word2)] += 1
    for word in sentence[2:]:
        model[key2(word1, word2)][key(word)] += 1
        word1, word2 = word2, word


for context in model.keys():
    model[context] = dict(
        accumulate(model[context].items(), lambda a, b: (b[0], a[1] + b[1]))
    )

start_lens = dict(accumulate(start_lens.items(), lambda a, b: (b[0], a[1] + b[1])))

with gzip.open(sys.argv[2], "wt") as f:
    json.dump(dict(start_lens=start_lens, states=model), f)
