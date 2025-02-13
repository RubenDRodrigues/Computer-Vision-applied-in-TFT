
import matplotlib.pyplot as plt

import cv2
import numpy as np

img_rgb = cv2.imread('nunu1.jpg')
template = cv2.imread('nunu.png')
w, h = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = .3
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):  # Switch collumns and rows
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite('result.png', img_rgb)
plt.imshow(img_rgb,),plt.show()
