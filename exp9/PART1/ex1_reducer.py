#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
current_len = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, len = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        len = int(len)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_len += len
        current_count += 1
    else:
        if current_word:
            # write result to STDOUT
            print '%s\t%s' % (current_word, round(current_len/current_count,2))
        current_len = len
        current_count=1
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s' % (current_word, round(current_len/current_count,2))
