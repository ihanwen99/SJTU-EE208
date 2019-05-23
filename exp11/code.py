import cv2
import numpy as np
import copy

# 1
img = cv2.imread("img1.png", 0)
# cv2.imshow("David Stark's Image", img)


# 2
Guass_img = cv2.GaussianBlur(img, (3, 3), 0)
cv2.imshow("David Stark's Guass_img", Guass_img)

# 3
x = cv2.Sobel(Guass_img, cv2.CV_16S, 1, 0)
y = cv2.Sobel(Guass_img, cv2.CV_16S, 0, 1)

absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)

dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

# cv2.imshow("absX", absX)
# cv2.imshow("absY", absY)
# cv2.imshow("dst", dst)

# 4
absX = absX + 1e-8
angle = np.floor_divide(absX, absY).astype(int)

height = len(dst)
width = len(dst[0])

for i in range(1, height - 2):
    for j in range(1, width - 2):
        k = angle[i][j]
        if k >= 1:
            dTmp1 = (1 - 1 / k) * dst[i - 1][j] + (1 / k) * dst[i - 1][j + 1]
            dTmp2 = (1 - 1 / k) * dst[i + 1][j] + (1 / k) * dst[i + 1][j - 1]
        elif 0 <= k < 1:
            dTmp1 = k * dst[i - 1][j + 1] + (1 - k) * dst[i][j + 1]
            dTmp2 = k * dst[i + 1][j - 1] + (1 - k) * dst[i][j - 1]
        elif -1 <= k < 0:
            dTmp1 = -k * dst[i - 1][j - 1] + (1 + k) * dst[i][j - 1]
            dTmp2 = -k * dst[i + 1][j + 1] + (1 + k) * dst[i][j + 1]
        elif k < -1:
            dTmp1 = (1 + 1 / k) * dst[i - 1][j] - (1 / k) * dst[i - 1][j - 1]
            dTmp2 = (1 + 1 / k) * dst[i + 1][j] - (1 / k) * dst[i + 1][j + 1]

        value = dst[i][j]
        if value < dTmp1 or value < dTmp2:
            dst[i][j] = 0

# cv2.imshow("David Stark's New dst_img", dst)

# 5
th1 = 32
th2 = 70

for i in range(0, height):
    for j in range(0, width):
        if dst[i][j] >= th2:
            dst[i][j] = 2
        elif th1 < dst[i][j] < th2:
            dst[i][j] = 1
        else:
            dst[i][j] = 0

for i in range(1, height - 1):
    for j in range(1, width - 1):
        if dst[i][j] == 1:
            if dst[i + 1][j + 1] == 2 or dst[i + 1][j - 1] == 2 or dst[i - 1][j + 1] == 2 \
                    or dst[i - 1][j - 1] == 2 or dst[i + 1][j] == 2 or dst[i - 1][j] == 2 \
                    or dst[i][j + 1] == 2 or dst[i][j - 1] == 2:
                dst[i][j] = 2

for i in range(1, height - 1):
    for j in range(1, width - 1):
        if dst[i][j] == 2:
            dst[i][j] = 255

cv2.imshow("David Stark's Data", dst)

edges = cv2.Canny(Guass_img, 50, 150, apertureSize=3)
cv2.imshow("David Stark's Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
