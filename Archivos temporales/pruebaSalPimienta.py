import cv2
import random
import numpy

perc = .05

size = (567, 378)
l = []

totPixels = 567 * 378
totNoise = totPixels * 100

print(totPixels, totNoise)

img = numpy.zeros([size[1], size[0], 3])

img[:, :, 0] = numpy.zeros([size[1], size[0]])
img[:, :, 1] = numpy.zeros([size[1], size[0]])
img[:, :, 2] = numpy.zeros([size[1], size[0]])

for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        if random.random() <= perc:
            img[j, i] = numpy.array((255, 255, 255))

cv2.imwrite("sal3.jpg", img)
cv2.imshow("image", img)
cv2.waitKey()

cv2.destroyAllWindows()
