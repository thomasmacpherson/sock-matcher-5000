import cv2
img = cv2.imread('green.jpg')

crop_img = img[400:500,670:770]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)
