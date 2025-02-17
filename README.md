# Generate Gibberish

_Parreggle aseming pareous unfrolandachus!_

This repo contains a couple of small demonstration Python scripts that can be
used to generate gibberish words that "sort-of" look like real words, possibly
from another language, but aren't. It is loosely based off the article
[Generating Text With Markov
Chains](https://healeycodes.com/generating-text-with-markov-chains) by Alex
Healy.

## WARNING

**While unlikely, these scripts may unintentionally generate obsceneties or
other undesirable words. Use them with care.**

## Usage

First generate the model:

```sh
./gen-model.py /usr/share/dict/words words.gz
```

Then use the model to generate a gibberish phrase

```sh
./gen-gibberish.py words.gz
```
