import cv2
import numpy as np

def signo(contorno):
    valido = 0
    comando2 = 0

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
    comando = 0
    alto,bajo,_ = img.shape
    tarea = alto*bajo
    slimite = tarea*0.15
    ilimite = tarea*0.02
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_ora = np.array([70, 100, 160])
    upper_ora = np.array([110,255,255])
    maskora = cv2.inRange(hsv,lower_ora,upper_ora)
    
    lower_blu = np.array([30, 150, 120])
    upper_blu = np.array([50,255,255])
    maskblu = cv2.inRange(hsv,lower_blu,upper_blu)  
    
    contora, _ = cv2.findContours(maskora, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contblu, _ = cv2.findContours(maskblu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contora:
        
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        
        if area < slimite and area > ilimite:
            if len(approx) == 3:
                valido,com2 = signo(contora)
                comando = 2
                if valido == 1:
                    comando = com2
    
                    
            if len(approx) == 4:
                
                valido,com2 = signo(contora)
                comando = 1
                if valido == 1:
                    comando = com2
                
    for cnt in contblu:

        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        
        if area < slimite and area > ilimite:
            
            if len(approx) == 3:
                valido,com2 = signo(contblu)
                comando = 4
                if valido == 1:
                    comando = com2
                    
            if len(approx) == 4:
                valido,com2 = signo(contblu)
                comando = 3
                if valido == 1:
                    comando = com2
    
    
    return comando

# commandsByNum = {0: "N/A",
#                 1: "Gira a la derecha y acelera",
#                 2: "Gira a la izquierda y acelera",
#                 3: "Gira a la derecha y desacelera",
#                 4: "Gira a la izquierda y desacelera",
#                 5: "Detención",
#                 6: "Puesta en marcha"}
#
#
#
# scale_percent = 35 # percent of original size

# for i in range(1, 16 + 1):
#     numFile = "0" + str(i) if i < 10 else str(i)
#     print(numFile)
#
#     img = cv2.imread("Fichas/t" + numFile + ".jpg")
#
#     width = int(img.shape[1] * scale_percent / 100)
#     height = int(img.shape[0] * scale_percent / 100)
#     dim = (width, height)
#
#     # resize image
#     resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#
#     res = recono(img)
#
#     print(res, commandsByNum[res[0]])
#     cv2.imshow('image', resized)
#
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


def camera(status):
    # https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
    # define a video capture object
    vid = cv2.VideoCapture(0)

    condition = True

    while(condition and status.running):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        status.currImage = frame
        # Display the resulting frame
        # cv2.imshow('frame', frame)

        if ret == True:
            command = recono(frame)

            status.changeNextCmd(command)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            condition = False
            break


    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

