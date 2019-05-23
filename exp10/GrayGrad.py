#!/usr/bin/env python
import cv2
import numpy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

img = cv2.imread("img2.png", cv2.IMREAD_GRAYSCALE)

list = []

H = len(img)
W = len(img[0])

for j in range(1, H - 2):
    for k in range(1, W - 2):
        Ix = int(img[j][k - 1]) - int(img[j][k + 1])
        Iy = int(img[j - 1][k]) - int(img[j + 1][k])
        I = round((Ix ** 2 + Iy ** 2) ** 0.5)
        list.append(I)

print(list)
number = 360

plt.hist(list, number, density=1)

plt.legend()

plt.xlabel("Gray")
plt.title("GrayScale")

plt.show()
# cv2.namedWindow("image")
# cv2.imshow("image",img)
# cv2.waitKey(0)
