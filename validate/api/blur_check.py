import cv2
import numpy as np

def check_image_blurness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return check_if_blur(gray) or check_if_pixaleted(gray)

def check_if_blur(gray):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    value = cv2.Laplacian(gray, cv2.CV_64F).var()
    return value < 100


def check_if_pixaleted(gray):

    #edge detection using canny
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    minLineLength = 200
    maxLineGap = 10

    #number of lines detection using hough

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)

    if(lines is None):
        lines =[]
    return len(lines) > 5

