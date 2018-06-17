import cv2
import argparse
import io
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import itemfreq
from time import gmtime, strftime
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

print(img.shape)

average_colour = [img[:, :, i].mean() for i in range(img.shape[-1])]

print(average_colour)

# arr = np.float32(img)
# pixels = arr.reshape((-1, 3))

# n_colors = 5
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
# flags = cv2.KMEANS_RANDOM_CENTERS
# _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

# palette = np.uint8(centroids)
# quantized = palette[labels.flatten()]
# quantized = quantized.reshape(img.shape)