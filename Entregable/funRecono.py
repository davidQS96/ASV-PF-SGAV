import cv2
import numpy as np


# Función de detección de signo
def signo(contorno):
    # Variables
    valido = 0
    comando2 = 0
    # Reconocimento de figuras
    for cnt in contorno:
        # Detección de figuras
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        # Detección de signo de resta
        if len(approx) == 4:
            if area < 20000 and area > 10000:
                valido = 1
                comando2 = 6

        # Detección de signo de suma
        if len(approx) == 12:
            if area < 20000 and area > 10000:
                valido = 1
                comando2 = 5


    return  valido,comando2

# Reconocimiento de instrucciones
def recono(img):
    # Variable del sistema
    comando = 0
    alto,bajo,_ = img.shape
    tarea = alto*bajo
    slimite = tarea*0.15
    ilimite = tarea*0.02
    
    #Mascaras para color naranja y turqueza
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_ora = np.array([70, 100, 160])
    upper_ora = np.array([110,255,255])
    maskora = cv2.inRange(hsv,lower_ora,upper_ora)
    
    lower_blu = np.array([20, 100, 100])
    upper_blu = np.array([50,255,255])
    maskblu = cv2.inRange(hsv,lower_blu,upper_blu)  
    
    contora, _ = cv2.findContours(maskora, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contblu, _ = cv2.findContours(maskblu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    # Busqueda de figuras de color naranja
    for cnt in contora:
        
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        
        # Clasificación de figuras en triangulo o rectangulo
        if area < slimite and area > ilimite:
            if len(approx) == 3:
                valido,com2 = signo(contora)
                comando = 2
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  
                    
            if len(approx) == 4:
                
                valido,com2 = signo(contora)
                comando = 3#1
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  
                    
    # Busqueda de figuras de color turqueza      
    for cnt in contblu:

        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        
        # Clasificación de figuras en triangulo o rectangulo
        if area < slimite and area > ilimite:
            
            if len(approx) == 3:
                valido,com2 = signo(contblu)
                comando = 4
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  
                    
            if len(approx) == 4:
                valido,com2 = signo(contblu)
                comando = 1#3
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  

    #print(comando)
    return comando,img

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

        # Display the resulting frame
        # cv2.imshow('frame', frame)

        if ret == True:
            command = recono(frame)
            #print("comando desde recono", command)

            frame = np.flip(frame, 1) #Refleja imagen respecto al eje y, para facilitar el posicionamiento de las figuras
            status.currImage = frame

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

