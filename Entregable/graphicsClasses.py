import pygame as pg

import classes


# Clase para guardar cada punto del circuito
class Point:

    # Metodo constructor
    # self.identif es un numero entero para identificar y llamar a un punto
    # self.coords son las coordenadas representadas con un diccionario, en pixeles, dentro de la ventana
    # self.neigbors es una lista con los puntos conectados al punto, y su angulo relativo
    # self.numConns es la cantidad entera de puntos conectados al punto
    # self.possibleDirections son los puntos cardinales posibles, ya que cada punto solo tiene vecinos en estas direcciones
    def __init__(self, identif, coords):
        if type(coords) != tuple or len(coords) != 2:
            print("Point.__init__: coords", coords, "no es valido.")
            return

        for elem in coords:
            if type(elem) != int or elem < 0:
                print("Point.__init__: coordenadas", coords, "no validas.")
                return

        self.identif = identif
        self.coords = {"x": coords[0], "y": coords[1]}
        self.neighbors = {}  # Direcc: punto vecino en esa direcc
        self.numConns = 0
        self.possibleDirections = ("N", "E", "S", "O")

    # Metodo para agregar un punto vecino conectado al punto
    # point es un objeto Point
    # direction es un string igual a "N", "E", "S" u "O"
    def addNeighbor(self, point, direction):
        # Verifica tipo de point
        if type(point) != Point:
            print("Point.addNeighbor: point no es de tipo Point.")
            return

        # Verifica si la direccion es de tipo y valor correctos
        if direction not in self.possibleDirections:
            print("Point.addNeighbor: direction no es valido.")
            return

        # Verifica si el punto a agregar no es el objeto mismo
        if point == self:
            print("Point.addNeighbor: punto no puede ser su propio vecino.")
            return

        # Verifica si punto a agregar ya esta en la lista
        for neighbor in self.neighbors:
            if point == neighbor:
                print("Point.addNeighbor: vecino %d repetido dentro de punto %d." % (point.identif, self.identif))
                return

        # Verifica si el punto ya tiene un vecino en la direccion ingresada
        if direction in self.neighbors:
            print("Point.addNeighbor: punto %d ya tiene un vecino en la direccion %s." % (self.identif, direction))
            return

        self.neighbors[direction] = point
        self.numConns += 1

        # Debido a que cada conexion es bidireccional, verifica que no se agregue
        # el mimso punto al punto agregado
        for neighborDir in point.neighbors:

            if point.neighbors[neighborDir] == self:
                return

        # Se agrega direccion contraria de vuelta a lastPoint (relativo a newPoint)
        newIx = -1
        numDirections = len(self.possibleDirections)
        for ix in range(numDirections):
            if self.possibleDirections[ix] == direction:
                newIx = ix
                break

        newIx = (newIx + 2) % numDirections  # newIx es el el indice del punto cardinal contrario al actual
        newDirection = self.possibleDirections[newIx]

        point.addNeighbor(self, newDirection)

    # Metodo para obtener puntos vecinos
    def getNeighbors(self):
        return self.neighbors

    # Metodo para obtener coordenadas del punto
    def getCoords(self):
        return self.coords

    # Metodo para obtener identificador del punto
    def getIdentif(self):
        return self.identif

    # Metodo para obtener numero de conexiones o vecinos del punto
    def getNumConns(self):
        return self.numConns

    # Metodo para debug, muestra vecinos por su identificador
    def getNeighborsAsIdentif(self):
        temp = {}
        for key in self.neighbors:
            temp[key] = self.neighbors[key].identif

        return temp


# Clase que representa al circuito donde circulara el carro
class Circuit:

    # Metodo constructor
    # self.points son los puntos que conforman el circuito
    # self.lastPoints se usa para construir el circuito, es el ultimo punto agregado
    # self.lines son todas las lineas entre 2 puntos, sin repetir, que conforman el circuito
    def __init__(self):
        self.points = []
        self.lastPoint = None
        self.lines = []

    # Metodo para agregar un punto vecino al ultimo punto agregado
    # identif es el identificador del punto
    # coords son las coordenadas del punto
    def addNeighborToLast(self, identif, coords):
        newPoint = Point(identif, coords)
        # Se verifica si se creo un newPoint correctamente
        if newPoint == None:
            print("Circuit.addNeighborToLast: newPoint no valido.")
            return

        self.points += [newPoint]

        # Si ya el circuito tiene por lo menos un punto, i.e. no es None
        if self.lastPoint != None:
            # Se calcula direccion de newPoint relativo a lastPoint
            direction = self.detDirectionRelToLast(newPoint)
            # Verificacion de direccion correcta
            if direction == None:
                print("Circuit.addNeighborToLast: no se encontro direccion valida.")
                return

            self.lastPoint.addNeighbor(newPoint, direction)

            # Se agrega linea al circuito
            lastCoords = self.lastPoint.getCoords()
            newCoords = newPoint.getCoords()
            self.lines += [(lastCoords, newCoords)]

        self.lastPoint = newPoint

    # Metodo para agregar una conexion del ultimo punto a un punto ya agregado
    # identif es el identificador del punto al que se quiere conectar el ultimo punto
    def joinLastTo(self, identif):
        # Busca el punto con identificador identif
        for point in self.points:
            if point.getIdentif() == identif:

                # Se calcula direccion de newPoint relativo a lastPoint
                direction = self.detDirectionRelToLast(point)
                # Verificacion de direccion correcta
                if direction == None:
                    print("Circuit.joinLastTo: no se encontro direccion valida.")
                    return

                self.lastPoint.addNeighbor(point, direction)

                # Se agrega linea al circuito
                lastCoords = self.lastPoint.getCoords()
                newCoords = point.getCoords()
                self.lines += [(lastCoords, newCoords)]

                self.lastPoint = point
                return

        print("Circuit.joinLastTo: no se encontro el punto deseado.")

    # Metodo para cambiar el ultimo punto del circuito
    # identif es el identificador del punto que se quiere como ultimo
    def changeLastTo(self, identif):
        for point in self.points:
            if point.getIdentif() == identif:
                self.lastPoint = point
                return

        print("Circuit.changeLastTo: no se encontro el punto deseado.")

    # Metodo para calcular la direccion de point relativo a lastPoint
    # point es un objeto tipo punto
    def detDirectionRelToLast(self, point):
        # Verifica tipo de point
        if type(point) != Point:
            print("Circuit: point no es de tipo Point.")
            return

        # Coordenadas
        xr = self.lastPoint.getCoords()['x']
        yr = self.lastPoint.getCoords()['y']
        x2 = point.getCoords()['x']
        y2 = point.getCoords()['y']

        # Identificacion de punto cardinal
        if xr == x2:
            # Verificacion de mismas coordenadas
            if yr == y2:
                print("Circuit.detDirectionRelToLast: point %d no puede tener mismas coordenadas que lastPoint %d." % (
                point.getIdentif(), self.lastPoint.getIdentif()))
                return

            elif yr > y2:
                return "N"

            else:
                return "S"

        if yr == y2:
            if xr < x2:
                return "E"

            else:
                return "O"

        print("Circuit.detDirectionRelToLast: no se encontro direccion cardinal")
        return

    # Metodo para obtener las lineas del circuito
    def getLines(self):
        return self.lines

    # Metodo para obtener puntos del circuito
    def getPoints(self):
        return self.points


# Clase que representa un carro
class Car:

    # Metodo constructor
    # self.circuit es el circuito que recorre el carro
    # self.screen es la pantalla donde se dibuja carro
    # self.status se usara para monitorear el estado del programa
    # self.color es el color del carro,                            temporal****
    # self.radius es el radio del carro representado como circulo, temporal****
    # initSpeed es la velocidad inicial del carro, pix por seg
    # self.firstPoint es el punto donde se coloca el carro al principio
    # self.lastPoint es el punto inicial de la trayectoria del carro
    # self.nextPoint es el punto final de trayectoria, o el destino del carro
    # self.speed es la velocidad actual del carro
    # self.isRunning es la condicion que indica si el carro esta en capacidad de movimiento
    # self.direction es la direccion de movimiento del carro
    # self.posX y self.posY son las coordenadas de posicion del carro dentro de la ventana
    # self.vectors es una serie de multiplicadores para calcular posiciones siguientes
    # self.possibleDirections son los puntos cardinales posibles de movimiento, independiente de los vecinos de cada punto
    def __init__(self, circuit, screen, status, color, radius=5, initSpeed=10):
        # Validacion de circuit
        if type(circuit) != Circuit:
            print("Car.__init__: circuit no es tipo Circuito, se asigna None.")
            self.circuit = None

        else:
            self.circuit = circuit

        # Validacion de screen
        if type(screen) != pg.Surface:
            print("Car.__init__: screen no es tipo pygame.Surface, se asigna None.")
            self.circuit = None

        else:
            self.screen = screen

        # Validacion de status
        if type(status) != classes.ProgramStatus:
            print("Car.__init__: screen no es tipo classes.ProgramStatus, se asigna None.")
            self.status = None

        else:
            self.status = status

        # Validacion de color
        if type(color) != tuple or len(color) != 3:
            print("Car.__init__: color no es valido, se asignara color blanco.")
            self.color = (255, 255, 255)

        else:
            self.color = color

            for chValue in color:
                if type(chValue) != int or chValue < 0 or chValue > 255:
                    print("Car.__init__: alguno de los valores de color no es valido, se asigna color blanco.")
                    self.color = (255, 255, 255)

        # Validacion de radius
        if (type(radius) != float and type(radius) != int) or radius < 0:
            print("Car.__init__: radius no es numero real positivo, se asigna valor de 10.")
            self.radius = 10

        else:
            self.radius = radius

        # Validacion de initSpeed
        if (type(initSpeed) != float and type(initSpeed) != int) or initSpeed < 0:
            print("Car.__init__: initSpeed no es numero real positivo, se asigna valor de 1.")
            self.radius = 1

        else:
            self.radius = radius

        # Declaracion de atributos
        self.firstPoint = circuit.getPoints()[0]
        self.lastPoint = self.firstPoint
        self.nextPoint = self.firstPoint.getNeighbors()["N"]


        self.minSpeed = 100 # pix/s
        self.diffSpeed = 5 # pix/s
        self.speed = initSpeed if initSpeed >= self.minSpeed else self.minSpeed # pix/s
        self.isRunning = True
        self.direction = "N"
        self.posX = self.lastPoint.getCoords()["x"]
        self.posY = self.lastPoint.getCoords()["y"]
        self.vectors = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "O": (-1, 0)}

        self.possibleDirections = ("N", "E", "S", "O")
        self.commandsByNum = {0: (),  # N/A
                              1: (0, 0),  # Gira a la derecha y acelera
                              2: (0, 1),  # Gira a la izquierda y acelera
                              3: (1, 0),  # Gira a la derecha y desacelera
                              4: (1, 1),  # Gira a la izquierda y desacelera
                              5: (0,),  # Detención
                              6: (1,)}  # Puesta en marcha

        # len 0: comando invalido
        # len 1: solo accion (action)
        # len 2: cambiar veloc y direccion (velUp, turnR)

    # Metodo para calcular la posicion siguiente del carro y actualizar el dibujo
    def move(self):
        # https://www.youtube.com/watch?v=YOCt8nsQqEo&ab_channel=ClearCode
        #Si el ultimo comando fue de detencion
        if not self.isRunning:
            currTime = pg.time.get_ticks()
            self.status.timeLeft = round(10000 - (currTime - self.status.stopTime), 3) / 1000

            if self.status.timeLeft <= 0:
                self.status.timeLeft = 0

            #Espera a que hayan pasado 10s y solo reanuda movimiento cuando se elige puesta en marcha
            if self.status.timeLeft <= 0 and self.status.nextCommandNum == 6:
                self.isRunning = True
                self.status.carIsRunning = True

            self.updateGraphic()
            return

        # Posiciones siguientes
        trueSpeed = self.speed / self.status.framerate # pix/seg * seg/frame = pix/frame

        tempX = self.posX + self.vectors[self.direction][0] * trueSpeed
        tempY = self.posY + self.vectors[self.direction][1] * trueSpeed

        #print(trueSpeed, tempX, tempY)

        gotToNext = False

        # Verifica si es movimiento vertical u horizontal
        if self.direction == "N" or self.direction == "S":
            # Verifica que no sobrepase el punto destino
            if self.vectors[self.direction][1] * (tempY - self.nextPoint.getCoords()["y"]) >= 0:
                self.posY = self.nextPoint.getCoords()["y"]
                gotToNext = True

            else:
                self.posY = tempY

        else: #E u O
            # Verfica que no sobrepase el punto destino
            if self.vectors[self.direction][0] * (tempX - self.nextPoint.getCoords()["x"]) >= 0:
                self.posX = self.nextPoint.getCoords()["x"]
                gotToNext = True

            else:
                self.posX = tempX

        # Se cambia de direccion si el carro llego a su punto destino
        if gotToNext:
            self.decideNextMovement()

        # Se mueve y dibuja el carro en screen
        self.updateGraphic()

    # Metodo para decidir el siguiente movimiento en una interseccion
    # Si no hay un comando disponible, elige entre una lista de direcciones predeterminadas
    def decideNextMovement(self):
        commandNum = self.status.activeCommandNum

        if commandNum == None:  # No se tiene un comando siguiente, el carro circula normalmente
            self.moveNormally()
            self.status.resetCmdNumber()
            return

        # Si no es un numero de comando valido
        if type(commandNum) != int or commandNum < 0 or commandNum > 6:
            print("Car.applyCommand: commandNum debe ser un entero entre 0 y 6 inclusives.")
            self.moveNormally()
            self.status.resetCmdNumber()
            return

        # Si el numero de comando corresponde a movimiento sin comando
        if commandNum == 0:
            self.moveNormally()
            self.status.resetCmdNumber()
            return

        # Decodificacion
        command = self.commandsByNum[commandNum]

        # Si el comando no tiene longitud, no hay informacion
        if len(command) == 0:
            print("Car.decideNextMovement: comando no tiene una forma valido (longitud 0).")
            self.moveNormally()
            self.status.resetCmdNumber()
            return

        currPoint = self.nextPoint

        if currPoint.getNumConns() <= 2:  # no es interseccion, sino curva o recta
            self.moveNormally()
            return

        #Si el ultimo comando no se ha mantenido lo suficiente
        if not self.status.isCommandActive():
            self.moveNormally()
            self.status.resetCmdNumber()
            return

        if len(command) == 1:  # (action)
            if command[0] == 0:  # detencion
                # https://www.youtube.com/watch?v=YOCt8nsQqEo&ab_channel=ClearCode
                self.status.stopTime = pg.time.get_ticks()
                self.isRunning = False
                self.status.carIsRunning = False

            elif command[0] == 1:  # Puesta en marcha
                self.moveNormally()

        elif len(command) == 2:  # (velUp, direction) velUp = 0: acel, turnR = 0: 90deg cw
            velUp, direction = command

            newSpeed = self.speed + round(self.diffSpeed * (1 - 2 * velUp), 2)  # (1 - 2 * velUp) unicamente tiene valores +-1

            if newSpeed < self.minSpeed:  # Si la velocidad no permite un funcionamiento adecuado del carro
                print("Car.decideNextMovement: cambio de velocidad no es válido.")

            else:
                self.speed = newSpeed

            self.atIntersectionMoveTo(direction)

        print("Comando anterior: " + str(commandNum) + "-" + self.status.commandsByNum[commandNum][0])
        self.status.resetCmdNumber()  # Se reinicia el comando y vuelve al inicial
        return

    # Calculo de movimiento en interseccion donde se desea mover a la izquierda (90deg cw) o derecha (90deg ccw)
    # direction es un valor entero/booleano donde 0 es giro a derecha y 1 es a la izquierda
    def atIntersectionMoveTo(self, direction):

        # Validacion de direction
        if type(direction) != int or (direction != 0 and direction != 1):
            print("Car.moveTo: direction no es entero o 0 o 1.")
            self.moveNormally()
            return

        rearrangedDirs = self.rearrangeDirections()  # (-:recto, 0: derecha, 1: izquierda)
        nextDirecc = rearrangedDirs[direction + 1]

        self.lastPoint = self.nextPoint
        neighbors = self.lastPoint.getNeighbors()

        if nextDirecc in neighbors:
            self.nextPoint = neighbors[nextDirecc]
            self.direction = nextDirecc

        else:
            self.moveNormally()

        return

    # Metodo para cambiar la direccion del carro cuando este llega al punto destino
    # Toma como direccion predeterminada la previa, sino gira a la derecha, sino a la izquierda
    def moveNormally(self):
        self.lastPoint = self.nextPoint
        neighbors = self.lastPoint.getNeighbors()

        for direction in self.getFavoredDirections():
            for neighborDirecc in neighbors:
                if neighborDirecc == direction:
                    self.nextPoint = neighbors[neighborDirecc]
                    self.direction = neighborDirecc
                    return

    # Para cada punto y direccion del carro, devuelve una lista con direcciones posteriores del carro en orden de prioridad
    # Simplemente llama a la funcion self.rearrangeDirections y devuelve su resultado, lo que cambia es el nombre
    # temp es una lista con strings de las direcciones dichas
    def getFavoredDirections(self):
        return self.rearrangeDirections()

    # Metodo para obtener las direcciones (recto, derecha, izquierda), desde la perspectiva del carro
    # temp es una lista con strings de las direcciones dichas
    def rearrangeDirections(self):
        temp = list(self.possibleDirections)
        numDirections = len(self.possibleDirections)
        lastDirIx = temp.index(self.direction)

        # Hace un desplazamiento de la lista para que su primer elemento sea el de direccion previa
        temp = temp[lastDirIx:] + temp[:lastDirIx]
        lastDirIx = 0
        # Remueve la direccion que devuelve el carro al punto previo
        oppIx = (lastDirIx + 2) % numDirections
        temp.pop(oppIx)

        return temp

    # Metodo para dibujar el carro en su nueva posicion dentro de screen
    def updateGraphic(self):
        pg.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)
