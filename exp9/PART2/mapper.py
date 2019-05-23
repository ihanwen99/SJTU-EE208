#!/usr/bin/env python

import sys
#file1 = open("test2.txt")
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into parts
    eles = line.split()
   
    current_link = eles[0]
    current_pr = float(eles[1])
    
    print '%s\t%s\t%f' % (current_link, 0, 0.0375)
	
    try:
        outlinks = eles[2:]
	
    	outnum = float(len(outlinks))
	
    	# increase counters
    	for link in outlinks:
	        # write the results to STDOUT (standard output);
        	# what we output here will be the input for the
        	# Reduce step, i.e. the input for reducer.py
        	#
	        # tab-delimited; the trivial word count is 1
		
        	print '%s\t%s\t%f' % (link, current_link, 0.85*current_pr/outnum)
    except:
	pass
	
