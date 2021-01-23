import cv2
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt




def recono(img):
    
    alto,bajo,_ = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_ora = np.array([70, 220, 220])
    upper_ora = np.array([110,255,255])
    maskora = cv2.inRange(hsv,lower_ora,upper_ora)
    
    lower_blu = np.array([30, 220, 220])
    upper_blu = np.array([50,255,255])
    maskblu = cv2.inRange(hsv,lower_blu,upper_blu)  
    
    contora, _ = cv2.findContours(maskora, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contblu, _ = cv2.findContours(maskblu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contora:
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            comando = 2
        if len(approx) == 4:
            comando = 1

    for cnt in contblu:
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            comando = 4
        if len(approx) == 4:
            comando = 3
    
    
    return comando