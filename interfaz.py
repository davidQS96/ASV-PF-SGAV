#Importacion de bibliotecas ----------------------------------------------------------------------
import pygame as pg

#Importacion de modulos propios --------------------------------------------------------------------------
from classes import *

#Constantes -----------------------------------------------------------------------------------------
maxDims = (1920, 1080)
multiplFactor = 0.8 / 1.25 #(.8 / 1.25, resolucion de 1229 x 691)
windowCaption = "Proyecto SV - Simulador de Pista"

#Constantes de pista
pathWidth = 50

#Colores
black = (0, 0, 0)
lightBlue = (183,255,247)
green = (0, 180, 65)
lightGrey = (150, 150, 150)

bgColor = green # For the background color of your window
streetColor = black
sidewalkColor = lightGrey

#Puntos del circuito con coordenadas predefinidas
points = ((238, 69),   (505, 69),  (99, 143),   (238, 143),
          (386, 143),  (505, 143), (817, 143),  (1129, 143),
          (99, 397),   (238, 397), (505, 397),  (817, 397),
          (1129, 397), (817, 509), (1129, 509), (386, 621), (1129, 621))

#Creacion del circuito -----------------------------------------------------------------------------
circuit = Circuit()
circuit.addNeighborToLast(3,  points[3])
circuit.addNeighborToLast(9,  points[9])
circuit.addNeighborToLast(8,  points[8])
circuit.addNeighborToLast(2,  points[2])
circuit.joinLastTo(3)
circuit.addNeighborToLast(0,  points[0])
circuit.addNeighborToLast(1,  points[1])
circuit.addNeighborToLast(5,  points[5])
circuit.addNeighborToLast(4,  points[4])
circuit.addNeighborToLast(15, points[15])
circuit.addNeighborToLast(16, points[16])
circuit.addNeighborToLast(14, points[14])
circuit.addNeighborToLast(13, points[13])
circuit.addNeighborToLast(11, points[11])
circuit.addNeighborToLast(12, points[12])
circuit.addNeighborToLast(7,  points[7])
circuit.addNeighborToLast(6,  points[6])
circuit.joinLastTo(11)
circuit.addNeighborToLast(10, points[10])
circuit.joinLastTo(5)
circuit.joinLastTo(6)

#Creacion de ventana --------------------------------------------------------------------------------
#https://riptutorial.com/pygame/example/22240/creating-the-pygame-window
(width, height) = (round(maxDims[0] * multiplFactor), round(maxDims[1] * multiplFactor)) # Dimension of the window

#Creacion de ventana
screen = pg.display.set_mode((width, height)) # Making of the screen
pg.display.set_caption(windowCaption) # Name for the window
screen.fill(bgColor) #This syntax fills the background colour


#Loop para ventana
running = True
while running:
    #Condicion para terminar programa y ventana grafica
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break

    if not running:
        pg.quit()
        break

    #Se dibujan las lineas del circuito
    for line in circuit.getLines():
        point1 = [line[0][0], line[0][1]]
        point2 = [line[1][0], line[1][1]]

        #Se cambia largo para que esquinas de caminos coincidan
        if point1[0] == point2[0]: #Linea vertical
            if point1[1] > point2[1]:
                point2[1] -= pathWidth / 2 - 1
                point1[1] += pathWidth / 2

            else:
                point1[1] -= pathWidth / 2 - 1
                point2[1] += pathWidth / 2

        elif point1[1] == point2[1]: #Linea horizontal
            if point1[0] > point2[0]:
                point2[0] -= pathWidth / 2 - 1
                point1[0] += pathWidth / 2

            else:
                point1[0] -= pathWidth / 2 - 1
                point2[0] += pathWidth / 2

        pg.draw.line(screen, streetColor, point1, point2, pathWidth)

    #Actualiza ventana
    pg.display.flip()










