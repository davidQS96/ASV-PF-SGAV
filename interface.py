# Importacion de bibliotecas ----------------------------------------------------------------------
import pygame as pg
import pygame.freetype as ft
import threading as th
import cv2
import numpy as np

# Importacion de modulos propios --------------------------------------------------------------------------
from graphicsClasses import *
from classes import *
from funRecono import *

# Constantes -----------------------------------------------------------------------------------------

maxDims = (1920, 1080)
multiplFactor = 0.8 / 1.25  # (.8 / 1.25, resolucion de 1229 x 691)
windowCaption = "Proyecto SV - Simulador de Pista"

# Constantes de pista
pathWidth = 55

# Constantes de movimiento
speed = 300

# Colores
black = (0, 0, 0)
lightBlue = (183, 255, 247)
darkGreen = (0, 180, 65)
lightGrey = (150, 150, 150)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

bgColor = darkGreen  # For the background color of your window
streetColor = black
sidewalkColor = lightGrey
carColor = red
textColor = black

# Puntos del circuito con coordenadas predefinidas
points = ((238, 69), (505, 69), (99, 143), (238, 143),
          (386, 143), (505, 143), (817, 143), (1129, 143),
          (99, 397), (238, 397), (505, 397), (817, 397),
          (1129, 397), (817, 509), (1129, 509), (386, 621), (1129, 621))


# Creacion del circuito -----------------------------------------------------------------------------
def main():
    circuit = Circuit()
    circuit.addNeighborToLast(3, points[3])
    circuit.addNeighborToLast(9, points[9])
    circuit.addNeighborToLast(8, points[8])
    circuit.addNeighborToLast(2, points[2])
    circuit.joinLastTo(3)
    circuit.addNeighborToLast(0, points[0])
    circuit.addNeighborToLast(1, points[1])
    circuit.addNeighborToLast(5, points[5])
    circuit.addNeighborToLast(4, points[4])
    circuit.addNeighborToLast(15, points[15])
    circuit.addNeighborToLast(16, points[16])
    circuit.addNeighborToLast(14, points[14])
    circuit.addNeighborToLast(13, points[13])
    circuit.addNeighborToLast(11, points[11])
    circuit.addNeighborToLast(12, points[12])
    circuit.addNeighborToLast(7, points[7])
    circuit.addNeighborToLast(6, points[6])
    circuit.joinLastTo(11)
    circuit.addNeighborToLast(10, points[10])
    circuit.joinLastTo(5)
    circuit.joinLastTo(6)

    # Creacion de ventana --------------------------------------------------------------------------------
    # https://riptutorial.com/pygame/example/22240/creating-the-pygame-window
    (width, height) = (round(maxDims[0] * multiplFactor), round(maxDims[1] * multiplFactor))  # Dimension of the window

    # Creacion de ventana
    pg.init()
    screen = pg.display.set_mode((width, height))  # Making of the screen
    gameFont = ft.SysFont("Tehoma", 20)  # Fuente de texto
    pg.display.set_caption(windowCaption)  # Name for the window

    #Creacion de reloj de pygame
    clock = pg.time.Clock()
    status.clock = clock
    prevTime = 0
    currTime = 0
    fps = 0
    fpsShown = 0
    refreshCont = 0

    # Instancia del carro
    car = Car(circuit, screen, status, carColor, (pathWidth - 24) / 2, speed)

    # Loop para ventana
    while status.running:
        # Condicion para terminar programa y ventana grafica
        for event in pg.event.get():
            if event.type == pg.QUIT:
                status.running = False
                break

        if not status.running:
            pg.quit()
            break


        prevTime = currTime
        currTime = pg.time.get_ticks()
        fps = 1000 / (currTime - prevTime)

        if refreshCont % (status.framerate / 2) == 0:
            fpsShown = fps

        refreshCont += 1

        screen.fill(bgColor)  # This syntax fills the background colour

        # Se dibujan las lineas del circuito
        for line in circuit.getLines():
            point1 = [line[0]['x'], line[0]['y']]
            point2 = [line[1]['x'], line[1]['y']]

            # Se cambia largo para que esquinas de caminos coincidan
            if point1[0] == point2[0]:  # Linea vertical
                if point1[1] > point2[1]:
                    point2[1] -= pathWidth / 2 - 1
                    point1[1] += pathWidth / 2

                else:
                    point1[1] -= pathWidth / 2 - 1
                    point2[1] += pathWidth / 2

            elif point1[1] == point2[1]:  # Linea horizontal
                if point1[0] > point2[0]:
                    point2[0] -= pathWidth / 2 - 1
                    point1[0] += pathWidth / 2

                else:
                    point1[0] -= pathWidth / 2 - 1
                    point2[0] += pathWidth / 2

            pg.draw.line(screen, streetColor, point1, point2, pathWidth)

        # Texto de siguiente movimiento
        # https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
        # You can use `render` and then blit the text surface ...
        text_surface, rect = gameFont.render("Sig: " + status.nextCommand, textColor)
        screen.blit(text_surface, (600, 40))

        # Texto de velocidad del carro
        text_surface2, rect2 = gameFont.render("Veloc: " + str(car.speed) + " pix/s", textColor)
        screen.blit(text_surface2, (600, 70))

        # Texto de cuadros por segundo
        text_surface3, rect2 = gameFont.render("FPS: " + str(round(fpsShown, 1)), textColor)
        screen.blit(text_surface3, (1000, 40))

        # Texto de temporizador
        text_surface4, rect2 = gameFont.render("Reloj: " + str(status.timeLeft) + " s", textColor)
        screen.blit(text_surface4, (1000, 70))

        # Se mueve carro
        car.move()

        #Ver el feed de la camara en el interfaz
        # https://www.geeksforgeeks.org/python-display-images-with-pygame/
        # copying the image surface object
        # to the display surface object
        dim = (279, 209)

        rect = pg.Rect((54 - 4, 450 - 4), (dim[0] + 8, dim[1] + 8))
        pg.draw.rect(screen, black, rect)

        if type(status.currImage) == np.ndarray:
            print(status.currImage.shape)
            resized = cv2.resize(status.currImage, dim, interpolation = cv2.INTER_AREA)

            # https://note.nkmk.me/en/python-opencv-bgr-rgb-cvtcolor/
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

            # https://stackoverflow.com/questions/30818367/how-to-present-numpy-array-into-pygame-surface
            resized = np.swapaxes(resized, 0, 1)
            newSurface = pg.pixelcopy.make_surface(resized)
            screen.blit(newSurface, (54, 450))

        # Actualiza ventana
        pg.display.flip()

        #Interfaz avanza a una frecuencia de framerate
        clock.tick(status.framerate)


# Algoritmo que se encarga de reconocer patrones en imagenes de la camara
def patternRecognition():

    #Camara, esta funcion llama al algoritmo de reconocimiento de comandos
    camera(status) #Esta dentro de un loop

if __name__ == "__main__":
    #Clase usada como memoria que todos los programas comparten
    status = ProgramStatus()

    #Thread de main para correr programas en paralelo
    # https://realpython.com/intro-to-python-threading/
    th.Thread(target=main).start()

    patternRecognition()


