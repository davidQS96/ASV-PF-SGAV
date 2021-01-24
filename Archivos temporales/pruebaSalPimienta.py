import cv2
import random
import numpy

perc = .03

size = (750, 500)
l = []

totPixels = 750 * 500
totNoise = totPixels * 100

print(totPixels, totNoise)

img = numpy.zeros([size[1], size[0], 3])

img[:, :, 0] = numpy.ones([size[1], size[0]])
img[:, :, 1] = numpy.ones([size[1], size[0]])
img[:, :, 2] = numpy.ones([size[1], size[0]])

for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        if random.random() <= perc:
            img[j, i] = numpy.array((0, 0, 0))


cv2.imshow("image", img)
cv2.waitKey()

cv2.destroyAllWindows()