# Importacion de bibliotecas ----------------------------------------------------------------------
import pygame as pg
import pygame.freetype as ft
import tkinter as tk
import threading as th

# Importacion de modulos propios --------------------------------------------------------------------------
from graphicsClasses import *
from classes import *

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
    running = True
    while running:
        # Condicion para terminar programa y ventana grafica
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

        if not running:
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
        text_surface2, rect2 = gameFont.render("FPS: " + str(round(fpsShown, 1)), textColor)
        screen.blit(text_surface2, (1000, 40))

        # Texto de temporizador
        text_surface2, rect2 = gameFont.render("Reloj: " + str(status.timeLeft) + " s", textColor)
        screen.blit(text_surface2, (1000, 70))

        # Se mueve carro
        car.move()

        # Actualiza ventana
        pg.display.flip()

        clock.tick(status.framerate)


# PRUEBAS -----------------------------------------------------------------------------------------
# Ventana con varias opciones para accion en siguiente interseccion
def interfaz():
    root = tk.Tk()
    root.geometry("250x250")
    f = tk.Frame(root)
    f.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Label(f, text="Ingrese opción:").pack()
    f2 = tk.Frame(f)
    f2.pack()

    status.intVarCmd = tk.IntVar()

    gdaR = tk.Radiobutton(f2, text="Gira a la derecha y acelera", variable=status.intVarCmd, value=1,
                          command=transmitMessage)
    giaR = tk.Radiobutton(f2, text="Gira a la izquierda y acelera", variable=status.intVarCmd, value=2,
                          command=transmitMessage)
    gddR = tk.Radiobutton(f2, text="Gira a la derecha y desacelera", variable=status.intVarCmd, value=3,
                          command=transmitMessage)
    gidR = tk.Radiobutton(f2, text="Gira a la izquierda y desacelera", variable=status.intVarCmd, value=4,
                          command=transmitMessage)
    detR = tk.Radiobutton(f2, text="Detención", variable=status.intVarCmd, value=5, command=transmitMessage)
    plyR = tk.Radiobutton(f2, text="Puesta en marcha", variable=status.intVarCmd, value=6, command=transmitMessage)

    status.intVarCmd.set(0)
    gdaR.deselect()
    giaR.deselect()
    gddR.deselect()
    gidR.deselect()
    detR.deselect()
    plyR.deselect()

    gdaR.grid(row=1, sticky="W")
    giaR.grid(row=2, sticky="W")
    gddR.grid(row=3, sticky="W")
    gidR.grid(row=4, sticky="W")
    detR.grid(row=5, sticky="W")
    plyR.grid(row=6, sticky="W")

    tk.mainloop()


def transmitMessage():
    status.changeNextCmd(status.intVarCmd.get())


# --------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    status = ProgramStatus()

    # https://realpython.com/intro-to-python-threading/
    th.Thread(target=main).start()

    interfaz()


