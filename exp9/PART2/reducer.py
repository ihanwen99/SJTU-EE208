#!/usr/bin/env python

from operator import itemgetter
import sys

current_page = None
current_pr = 0
dict1={}
dict2={}
for i in range(5):
    dict1[i] = []
    dict2[i] = 0;
#file1 = open("reduce.txt")
# input comes from STDIN
for line in sys.stdin:
    #print line
    line = line.strip()
    # parse the input we got from mapper.py
    try:
   	page, target, pr = line.split()
	
    except:
	break
    # convert count (currently a string) to int
    try:
        pr = float(pr)
	target = int(target)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    #if current_page == page:
    #    current_pr += pr
#	dict1[target].append(current_page)
#	dict2[int(current_page)]=current_pr
    #else:
        
        #if current_word:
            # write result to STDOUT
        #    print '%s\t%s' % (current_word, float(current_count)/current_len)
    #current_page = page       
#	current_pr = pr
    dict1[target].append(page)
    dict2[int(page)]+=pr
 

#print dict2
for key,value in dict2.items():
    if key != 0:
	print key,'\t',value,'\t','\t'.join(dict1[int(key)])
