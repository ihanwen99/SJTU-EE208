# -*- coding: UTF-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import cv2
import pickle as pk
import time


def reset(k):
    if 0 <= k < 0.3:
        k = 0
    elif 0.3 <= k < 0.6:
        k = 1
    elif 0.6 <= k:
        k = 2
    return k


def getPartInfo(img, start1, end1, start2, end2):
    r = 0
    g = 0
    b = 0
    for i in range(start1, end1):
        for j in range(start2, end2):
            r += img[i][j][0]
            g += img[i][j][1]
            b += img[i][j][2]

    count = r + g + b
    r = round(r / count, 2)
    g = round(g / count, 2)
    b = round(b / count, 2)
    l = []
    l.append(r)
    l.append(g)
    l.append(b)
    return l


# Basic Process
def basicProcess(img):
    H = len(img)
    W = len(img[1])

    MH = int(H / 2)
    MW = int(W / 2)

    l1 = getPartInfo(img, 0, MH, 0, MW)
    l2 = getPartInfo(img, 0, MH, MW, W)
    l3 = getPartInfo(img, MH, H, 0, MW)
    l4 = getPartInfo(img, MH, H, MW, W)

    l = []
    for i in l1:
        l.append(reset(i))
    for i in l2:
        l.append(reset(i))
    for i in l3:
        l.append(reset(i))
    for i in l4:
        l.append(reset(i))

    # LSH PreProcess
    res = []
    for i in l:
        if i == 0:
            res.extend([0, 0])
        elif i == 1:
            res.extend([1, 0])
        elif i == 2:
            res.extend([1, 1])
    return res


# LSH Search
def LSHserarch(vec):
    count = 0
    for i in vec:
        count += vec[i]
    count %= 6
    return count


# PreProcess
def PreProcess():
    print("Processing...")
    dataset = []
    for i in range(6):
        dataset.append([])
    for i in range(1, 41):
        imgname = "Dataset/{}.jpg".format(i)
        print("Processing Pic {} ...".format(i))
        img = cv2.imread(imgname)
        vec = basicProcess(img)
        hash = LSHserarch(vec)
        dataset[hash].append(tuple([imgname, vec]))
    file = open("Data.pkl", "wb")
    pk.dump(dataset, file)
    file.close()
    print("Data PreProcess Done !")


# PreProcess()  # yong yu yu chu li

def PreProcessMax():
    print("Processing...")
    dataset = []
    for i in range(1, 41):
        imgname = "Dataset/{}.jpg".format(i)
        print("Processing Pic {} ...".format(i))
        img = cv2.imread(imgname)
        vec = basicProcess(img)

        dataset.append(tuple([imgname, vec]))
    file = open("DataMax.pkl", "wb")
    pk.dump(dataset, file)
    file.close()
    print("DataMax PreProcess Done !")


PreProcessMax()


def LSHCompare():
    a = time.clock()
    img = cv2.imread("target.jpg")
    cv2.imshow("Raw Target", img)
    vec = basicProcess(img)
    hash = LSHserarch(vec)
    with open("Data.pkl", "rb") as f:
        dataset = pk.load(f)

    aimSet = dataset[hash]
    print("\nVector of Target : ")
    print(vec)
    # print(aimSet[0][0])  # name
    # print(aimSet[0][1])  # vector

    NN_search(vec, aimSet)
    b = time.clock()
    print("Using {} seconds.".format(b - a))
    cv2.waitKey(0)

    cv2.destroyAllWindows()


def Compare():
    a = time.clock()
    img = cv2.imread("target.jpg")
    cv2.imshow("Raw Target", img)
    vec = basicProcess(img)

    with open("DataMax.pkl", "rb") as f:
        dataset = pk.load(f)

    aimSet = dataset
    print("\nVector of Target : ")
    print(vec)
    # print(aimSet[0][0])  # name
    # print(aimSet[0][1])  # vector

    NN_search(vec, aimSet)
    b = time.clock()
    print("Using {} seconds.".format(b - a))
    cv2.waitKey(0)

    cv2.destroyAllWindows()


def NN_search(vec, aimSet):
    result = []
    len1 = len(aimSet)
    len2 = len(vec)
    for i in range(len1):
        for j in range(len2):
            if vec[j] != aimSet[i][1][j]:
                break

            if j == len2 - 1:
                result.append(aimSet[i][0])

    num = len(result)
    for i in range(num):
        img = cv2.imread(result[i])
        cv2.imshow("Matched Target", img)

    if (num == 1):
        print("The Matched Photo is {}.".format(result[0]))
    else:
        for i in range(num):
            print("The Sim Photos are {}.".format(result[i]))


# LSHCompare()
Compare()
