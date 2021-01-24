import cv2
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt


def signo(img,maskc,cont):
    count = 0
    maskc = np.zeros(img.shape, dtype=np.uint8)
    cv2.drawContours(maskc, cont, 0, (255, 255, 255), cv2.FILLED)
    maskc = cv2.cvtColor(maskc, cv2.COLOR_RGB2GRAY)
    corte = cv2.bitwise_or(img, img, mask=maskc)
    gray = cv2.cvtColor(corte, cv2.COLOR_RGB2GRAY)
    contorno, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contorno:
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if len(approx) == 4:
            if area < 20000 and area > 100:
                valido = 1
                comando2 = 6


        if len(approx) == 12:
            if area < 20000 and area > 100:
                valido = 1
                comando2 = 5


    return  valido,comando2


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
            valido,com2 = signo(img,maskora,[approx])
            if valido == 1:
                comando = 2
                comando2 = com2
                
        if len(approx) == 4:
            valido,com2 = signo(img,maskora,[approx])
            if valido == 1:
                comando = 1
                comando2 = com2
                
    for cnt in contblu:
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            valido,com2 = signo(img,maskora,[approx])
            if valido == 1:
                comando = 4
                comando2 = com2
                
        if len(approx) == 4:
            valido,com2 = signo(img,maskora,[approx])
            if valido == 1:
                comando = 3
                comando2 = com2
    
    
    return comando,comando2