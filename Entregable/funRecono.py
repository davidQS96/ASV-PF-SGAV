import cv2
import numpy as np


# Función de detección de signo
def signo(contorno,sslimite,ilimite,img):
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
            if area < sslimite and area > ilimite:
                valido = 1
                comando2 = 6
                cv2.drawContours(img, [approx], 0, (255, 0, 0), 5)

        # Detección de signo de suma
        if len(approx) == 12:
            if area < sslimite and area > ilimite:
                valido = 1
                comando2 = 5
                cv2.drawContours(img, [approx], 0, (255, 0, 0), 5)

    return  valido,comando2,img


def subborde(lineas,img):
    maskc = np.zeros(img.shape, dtype=np.uint8)
    cv2.drawContours(maskc, lineas, 0, (255, 255, 255), cv2.FILLED)
    maskc = cv2.cvtColor(maskc, cv2.COLOR_RGB2GRAY)
    corte = cv2.bitwise_or(img, img, mask=maskc)
    corte = cv2.cvtColor(corte, cv2.COLOR_RGB2GRAY)
    return corte
    return  valido, comando2

# Reconocimiento de instrucciones
def recono(img):
    # Variable del sistema
    comando = 0
    comando2 = 0
    img2 = img.copy()
    alto,bajo,_ = img.shape
    tarea = alto*bajo
    slimite = tarea*0.15
    sslimite = tarea*0.05
    ilimite = tarea*0.02
    silimite = tarea*0.005
    
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
                
                corte = subborde([approx],img2)
                contorno, _ = cv2.findContours(corte, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                valido,com2,img = signo(contorno,sslimite,silimite,img)
                
                comando = 2
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  
                    
            if len(approx) == 4:
                
                corte = subborde([approx],img2)
                contorno, _ = cv2.findContours(corte, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                valido,com2,img = signo(contorno,sslimite,silimite,img)
                
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
                
                corte = subborde([approx],img2)
                contorno, _ = cv2.findContours(corte, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                valido,com2,img = signo(contorno,sslimite,silimite,img)
                
                comando = 4
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  
                    
            if len(approx) == 4:
                
                corte = subborde([approx],img2)
                contorno, _ = cv2.findContours(corte, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                valido,com2,img = signo(contorno,sslimite,silimite,img)
                
                comando = 1#3
                if valido == 1:
                    comando = com2
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  

    #print(comando)
    return comando, img


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
            lastCommand = status.nextCommandNum
            #print("comando desde recono", command)

            if status.sameCommandCount <= status.sameCommandMaxCount:
                command = recono(frame)[0]

                if command != 0 and command == lastCommand:
                    if status.carIsRunning:
                        status.sameCommandCount += 1
=======
>>>>>>> Stashed changes


        if ret == True:
            lastCommand = status.nextCommandNum

            command  = recono(frame)[0]

            status.changeNextCmd(command)

            frame = np.flip(frame, 1) #Refleja imagen respecto al eje y, para facilitar el posicionamiento de las figuras

            status.currImage = frame

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

