from __future__ import division
from Bitarray import Bitarray
import random

bitarray_obj = Bitarray(32000)


def get_random_string():
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 6))


strlist = [get_random_string() for i in xrange(1600)]
testlist = [get_random_string() for i in xrange(2000000)]
notinit = []
truenotinit = []


def BKDRHash(seed, key):
    # seed = 131  # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
        hash = (hash * seed) + ord(key[i])
    return hash


seedlist = [31, 131, 1313, 13131, 131313, 1313131, 13131313, 131313131, 1313131313, 13131313131]

for i in strlist:
    for j in seedlist:
        num = BKDRHash(j, i) % 32000
        bitarray_obj.set(num)

for i in testlist:
    l = 1
    for j in seedlist:
        num = BKDRHash(j, i) % 32000
        l *= bitarray_obj.get(num)
    if l == 0:
        notinit.append(i)

for j in testlist:
    count = 1
    for i in strlist:
        if j == i:
            count = 0
    if count == 1:
        truenotinit.append(j)

#print(notinit)
#print(truenotinit)

print(len(notinit) / len(truenotinit))
