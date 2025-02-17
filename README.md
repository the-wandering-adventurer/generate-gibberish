# Generate Gibberish

_Parreggle aseming pareous unfrolandachus!_

This repo contains a couple of small demonstration Python scripts that can be
used to generate gibberish words that "sort-of" look like real words, possibly
from another language, but aren't. It is loosely based off the article
[Generating Text With Markov
Chains](https://healeycodes.com/generating-text-with-markov-chains) by Alex
Healy.

## WARNING

**While unlikely, nothing stops these scripts from generating obscenities or
other undesirable words. Use them with care.**

## Usage

First generate the model:

```sh
$ ./gen-model.py /usr/share/dict/words words.gz
```

Then use the model to generate a gibberish phrase

```sh
$ ./gen-gibberish.py words.gz
```

## How Does It Work?

Most examples of Markov chains uses words as their atoms in order to generate
phrases or sentence. In my case, I wanted to generate the words themselves.
`gen-model.py` goes through each word in the dictionary, character by character,
in order to generate the Markov chain for generating words. It saves that model
as compressed JSON to a file.

`gen-gibberish.py` reads in the Markov chain and uses it to generate a simple
random phrase.

## I Want to Generate Gibberish in Another Language

If you have [aspell](http://aspell.net/) installed, you can ask it to dump its
dictionaries to a file, and use that file as input to the generate the Markov
chain:

```sh
# Dump the Latin dictionary to a text file
$ aspell -l la dump master | aspell -l la expand | sed 's/ /\n/g' > la.txt

# Generate the model
$ ./gen-model.py la.txt la.gz

# Generate some gibberish that looks vaguely like Latin
$ ./gen-gibberish la.gz
defant pretilique alibinue didentaviviti
```

Do you want to generate gibberish based off words from Danish, French and
Swedish? Go for it!

```sh
$ aspell -l da dump master | aspell -l da expand > dafrsv.txt
$ aspell -l fr dump master | aspell -l fr expand >> dafrsv.txt
$ aspell -l sv dump master | aspell -l sv expand >> dafrsv.txt
$ ./gen-gibberish.py dafrsv.gz 
$ ./gen-gibberish.py dafrsv.gz 
apprépropruriversions enterolfinradik färdener barde bedspréchisemekref tningerirent
```

## What's This For?

Are you GM'ing a fantasy role playing game, and your players come across an
ancient inscription that you want to show them, but you can't be bothered
developing a whole new language? Do you want to spout some nonsense while your
mage PC casts a spell? Is your ten-page college essay due in an hour, and you
need to turn in something---_anything_?! The applications are limitless!

(No, please don't use this to write your college essay. Really, don't do it.)

## TODO

`./gen-gibberish.py` tends to generate words that are way too long. This could
potentially be mitigated by artificially boosting the probability of the
end-of-word marker (the period `.`) in the Markov chain.

As mentioned at the top, there is no filter for bad words.
