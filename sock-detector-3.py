import cv2
import argparse
import io
import numpy
import matplotlib.pyplot as plt
from scipy.stats import itemfreq
from time import gmtime, strftime
import picamera
from time import sleep

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", help = "path to the image")
#args = vars(ap.parse_args())
class SockDetector():
    def __init__(self):
        

#img = cv2.imread(args["image"])
camera = picamera.PiCamera()
camera.awb_mode = 'off'
camera.awb_gains = (2,2)
#camera.exposure_mode = 'off'
sleep(5)
while True:
    stream = io.BytesIO()
    camera.resolution = (320,240)
    camera.framerate =24
    #print(stream.__dict__)
    sleep(1)
    camera.capture(stream, format='jpeg')
    #sleep(5)
    test = stream.getvalue()
    #print(test)
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    img = cv2.imdecode(buff, 1)

    #print(img.shape)

    #average_colour = [img[150:151,115:116, i].mean() for i in range(img.shape[-1])]
    average_colour = img[150,115]

    print("Red: " + str(average_colour[2]) + ", Green: " + str(average_colour[1]) + ", Blue: " + str(average_colour[0]))

# arr = np.float32(img)
# pixels = arr.reshape((-1, 3))

# n_colors = 5
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
# flags = cv2.KMEANS_RANDOM_CENTERS
# _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

# palette = np.uint8(centroids)
# quantized = palette[labels.flatten()]
# quantized = quantized.reshape(img.shape)