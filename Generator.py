import numpy as np
import cv2

WIDTH = 297
HEIGHT = 420

# NEW WHITE IMAGE
img = np.zeros((HEIGHT*2, WIDTH*2, 1), np.uint8)
img[:] = 255
cv2.namedWindow('image')

for x in [0,1]:
    for y in [0,1]:
        # DRAW X NUMBERS
        for i in range(0,13):
            cv2.putText(img, str(i), (29+20*i-(5 if i>9 else 0) + x*WIDTH, 12 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)

        # DRAW CALIBRATION STRIPS
        cv2.rectangle(img, (27 + x*WIDTH, 15 + y*HEIGHT), (27+20*13-2 + x*WIDTH, 15+15 + y*HEIGHT), 130, -1)
        cv2.rectangle(img, (27 + x*WIDTH, 395 + y*HEIGHT), (27+20*13-2 + x*WIDTH, 395+15 + y*HEIGHT), 130, -1)

        # DRAW SQUARES
        for i in range(27, 27+20*13, 20):
            for j in range(35, 35+20*18, 20):
                cv2.rectangle(img, (i + x*WIDTH, j + y*HEIGHT), (i+15 + x*WIDTH, j+15 + y*HEIGHT), 0, 1)

        # DRAW Y NUMBERS
        cv2.putText(img, "T", (10 + x*WIDTH, 48 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)
        cv2.putText(img, "M", (10 + x*WIDTH, 68 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)
        for i in range(1, 17):
            cv2.putText(img, str(i), ((10 if i<10 else 4) + x*WIDTH, 68+i*20 + y*HEIGHT), cv2.FONT_HERSHEY_PLAIN, 1, 0)

cv2.imwrite("scantron.png", img)
cv2.imshow('image', img)
cv2.waitKey(0)