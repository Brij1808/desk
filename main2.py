import cv2
from object_detector import *
import numpy as np

detector = HomogeneousBgDetector()

# Load Image
img = cv2.imread("phone_aruco_marker.jpg")

contours = detector.detect_objects(img)

# Draw objects boundaries
for cnt in contours:

    cv2.polylines(img, [cnt], True, (255, 0, 0), 2)



cv2.imshow("Image", img)
cv2.waitKey(0)