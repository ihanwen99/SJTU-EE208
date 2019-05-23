#!/usr/bin/env python
import cv2
import numpy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

img = cv2.imread("img1.png", cv2.IMREAD_GRAYSCALE)

list = numpy.array(img).flatten()
print(list)
number = 255

plt.hist(list, number, density=1)

plt.legend()

plt.xlabel("Gray")
plt.title("GrayScale")

plt.show()
# cv2.namedWindow("image")
# cv2.imshow("image",img)
# cv2.waitKey(0)
