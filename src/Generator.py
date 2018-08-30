import numpy as np
import cv2

WIDTH = 594
HEIGHT = 840

# NEW WHITE IMAGE
img = np.zeros((HEIGHT*2, WIDTH*2, 1), np.uint8)
img[:] = 255
cv2.namedWindow('image')

for x in [0,1]:
    for y in [0,1]:
        # DRAW X NUMBERS
        for i in range(0,13):
            cv2.putText(img, str(i), (64+40*i-(10 if i>9 else 0) + x*WIDTH, 24 + y*HEIGHT), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 0)

        # DRAW DS LOCATIONS
        for i, l in enumerate(["R1", "R2", "R3", "B1", "B2", "B3"]):
            cv2.putText(img, l, (60+40*i + x*WIDTH, 90 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)
        cv2.putText(img, "R", (304 + x*WIDTH, 90 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)
        cv2.putText(img, "C", (464 + x*WIDTH, 130 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)

        # DRAW CALIBRATION STRIPS
        cv2.rectangle(img, (54 + x*WIDTH, 30 + y*HEIGHT), (54+40*13-4 + x*WIDTH, 30+30 + y*HEIGHT), 130, -1)
        cv2.rectangle(img, (54 + x*WIDTH, 790 + y*HEIGHT), (54+40*13-4 + x*WIDTH, 790+30 + y*HEIGHT), 130, -1)

        # DRAW SQUARES
        for j in range(70, 70+40*18, 40):
            for i in range(54, 54+40*(7 if j==70 else 11 if j==110 else 10 if j==150 else 13), 40):
                cv2.rectangle(img, (i + x*WIDTH, j + y*HEIGHT), (i+30 + x*WIDTH, j+30 + y*HEIGHT), 0, 1)

        # DRAW Y NUMBERS
        cv2.putText(img, "_0", (13 + x*WIDTH, 132 + y*HEIGHT), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 0)
        cv2.putText(img, "0_", (13 + x * WIDTH, 172 + y * HEIGHT), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 0)
        for i in range(1, 16):
            cv2.putText(img, str(i), ((32 if i<10 else 18) + x*WIDTH, 172+i*40 + y*HEIGHT), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 0)

cv2.imwrite("../scantron.png", img)
cv2.imshow('image', img)
cv2.waitKey(0)