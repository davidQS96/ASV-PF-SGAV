import pygame

#Clase para guardar cada punto del circuito
class Point:

    #Metodo constructor
    #self.identif es un numero entero para identificar y llamar a un punto
    #self.coords son las coordenadas representadas con un diccionario, en pixeles, dentro de la ventana
    #self.neigbors es una lista con los puntos conectados al punto, y su angulo relativo
    #self.numConns es la cantidad entera de puntos conectados al punto
    #self.possibleDirections son los puntos cardinales posibles, ya que cada punto solo tiene vecinos en estas direcciones
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
        self.neighbors = {}
        self.numConns = 0
        self.possibleDirections = ("N", "E", "S", "O")

    #Metodo para agregar un punto vecino conectado al punto
    #point es un objeto Point
    #direction es un string igual a "N", "E", "S" u "O"
    def addNeighbor(self, point, direction):
        #Verifica tipo de point
        if type(point) != Point:
            print("Point.addNeighbor: point no es de tipo Point.")
            return

        #Verifica si la direccion es de tipo y valor correctos
        if direction not in self.possibleDirections:
            print("Point.addNeighbor: direction no es valido.")
            return

        #Verifica si el punto a agregar no es el objeto mismo
        if point == self:
            print("Point.addNeighbor: punto no puede ser su propio vecino.")
            return

        #Verifica si punto a agregar ya esta en la lista
        for neighbor in self.neighbors:
            if point == neighbor:
                print("Point.addNeighbor: vecino %d repetido dentro de punto %d." % (point.identif, self.identif))
                return

        #Verifica si el punto ya tiene un vecino en la direccion ingresada
        if direction in self.neighbors:
            print("Point.addNeighbor: punto %d ya tiene un vecino en la direccion %s." %(self.identif, direction))
            return

        self.neighbors[direction] = point
        self.numConns += 1

        #Debido a que cada conexion es bidireccional, verifica que no se agregue
        #el mimso punto al punto agregado
        for neighborDir in point.neighbors:

            if point.neighbors[neighborDir] == self:
                return

        #Se agrega direccion contraria de vuelta a lastPoint (relativo a newPoint)
        newIx = -1
        numDirections = len(self.possibleDirections)
        for ix in range(numDirections):
            if self.possibleDirections[ix] == direction:
                newIx = ix
                break

        newIx = (newIx + 2) % numDirections #newIx es el el indice del punto cardinal contrario al actual
        newDirection = self.possibleDirections[newIx]

        point.addNeighbor(self, newDirection)

    #Metodo para obtener puntos vecinos
    def getNeighbors(self):
        return self.neighbors

    #Metodo para obtener coordenadas del punto
    def getCoords(self):
        return self.coords

    #Metodo para obtener identificador del punto
    def getIdentif(self):
        return self.identif

    #Metodo para obtener numero de conexiones o vecinos del punto
    def getNumConns(self):
        return self.numConns

    #Metodo para debug, muestra vecinos por su identificador
    def getNeighborsAsIdentif(self):
        temp = {}
        for key in self.neighbors:
            temp[key] = self.neighbors[key].identif

        return temp


#Clase que representa al circuito donde circulara el carro
class Circuit:

    #Metodo constructor
    #self.points son los puntos que conforman el circuito
    #self.lastPoints se usa para construir el circuito, es el ultimo punto agregado
    #self.lines son todas las lineas entre 2 puntos, sin repetir, que conforman el circuito
    def __init__(self):
        self.points = []
        self.lastPoint = None
        self.lines = []

    #Metodo para agregar un punto vecino al ultimo punto agregado
    #identif es el identificador del punto
    #coords son las coordenadas del punto
    def addNeighborToLast(self, identif, coords):
        newPoint = Point(identif, coords)
        #Se verifica si se creo un newPoint correctamente
        if newPoint == None:
            print("Circuit.addNeighborToLast: newPoint no valido.")
            return

        self.points += [newPoint]

        #Si ya el circuito tiene por lo menos un punto, i.e. no es None
        if self.lastPoint != None:
            #Se calcula direccion de newPoint relativo a lastPoint
            direction = self.detDirectionRelToLast(newPoint)
            #Verificacion de direccion correcta
            if direction == None:
                print("Circuit.addNeighborToLast: no se encontro direccion valida.")
                return

            self.lastPoint.addNeighbor(newPoint, direction)

            #Se agrega linea al circuito
            lastCoords = self.lastPoint.getCoords()
            newCoords = newPoint.getCoords()
            self.lines += [(lastCoords, newCoords)]

        self.lastPoint = newPoint

    #Metodo para agregar una conexion del ultimo punto a un punto ya agregado
    #identif es el identificador del punto al que se quiere conectar el ultimo punto
    def joinLastTo(self, identif):
        #Busca el punto con identificador identif
        for point in self.points:
            if point.getIdentif() == identif:

                #Se calcula direccion de newPoint relativo a lastPoint
                direction = self.detDirectionRelToLast(point)
                #Verificacion de direccion correcta
                if direction == None:
                    print("Circuit.joinLastTo: no se encontro direccion valida.")
                    return

                self.lastPoint.addNeighbor(point, direction)

                #Se agrega linea al circuito
                lastCoords = self.lastPoint.getCoords()
                newCoords = point.getCoords()
                self.lines += [(lastCoords, newCoords)]

                self.lastPoint = point
                return

        print("Circuit.joinLastTo: no se encontro el punto deseado.")

    #Metodo para cambiar el ultimo punto del circuito
    #identif es el identificador del punto que se quiere como ultimo
    def changeLastTo(self, identif):
        for point in self.points:
            if point.getIdentif() == identif:
                self.lastPoint = point
                return

        print("Circuit.changeLastTo: no se encontro el punto deseado.")


    #Metodo para calcular la direccion de point relativo a lastPoint
    #point es un objeto tipo punto
    def detDirectionRelToLast(self, point):
        #Verifica tipo de point
        if type(point) != Point:
            print("Circuit: point no es de tipo Point.")
            return

        #Coordenadas
        xr = self.lastPoint.getCoords()['x']
        yr = self.lastPoint.getCoords()['y']
        x2 = point.getCoords()['x']
        y2 = point.getCoords()['y']

        #Identificacion de punto cardinal
        if xr == x2:
            #Verificacion de mismas coordenadas
            if yr == y2:
                print("Circuit.detDirectionRelToLast: point %d no puede tener mismas coordenadas que lastPoint %d." %(point.getIdentif(), self.lastPoint.getIdentif()))
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

    #Metodo para obtener las lineas del circuito
    def getLines(self):
        return self.lines

    #Metodo para obtener puntos del circuito
    def getPoints(self):
        return self.points

#Clase que representa un carro
class Car:

    #Metodo constructor
    #self.circuit es el circuito que recorre el carro
    #self.screen es la pantalla donde se dibuja carro
    #self.color es el color del carro,                            temporal****
    #self.radius es el radio del carro representado como circulo, temporal****
    #initSpeed es la velocidad inicial del carro
    #self.firstPoint es el punto donde se coloca el carro al principio
    #self.lastPoint es el punto inicial de la trayectoria del carro
    #self.nextPoint es el punto final de trayectoria, o el destino del carro
    #self.speed es la velocidad actual del carro
    #self.direction es la direccion de movimiento del carro
    #self.posX y self.posY son las coordenadas de posicion del carro dentro de la ventana
    #self.vectors es una serie de multiplicadores para calcular posiciones siguientes
    #self.possibleDirections son los puntos cardinales posibles de movimiento, independiente de los vecinos de cada punto
    def __init__(self, circuit, screen, color, radius = 5, initSpeed = 1):
        #Validacion de circuit
        if type(circuit) != Circuit:
            print("Car.__init__: circuit no es tipo Circuito, se asigna None.")
            self.circuit = None

        else:
            self.circuit = circuit

        #Validacion de screen
        if type(screen) != pygame.Surface:
            print("Car.__init__: screen no es tipo pygame.Surface, se asigna None.")
            self.circuit = None

        else:
            self.screen = screen

        #Validacion de color
        if type(color) != tuple or len(color) != 3:
            print("Car.__init__: color no es valido, se asignara color blanco.")
            self.color = (255, 255, 255)

        else:
            self.color = color

            for chValue in color:
                if type(chValue) != int or chValue < 0 or chValue > 255:
                    print("Car.__init__: alguno de los valores de color no es valido, se asigna color blanco.")
                    self.color = (255, 255, 255)

        #Validacion de radius
        if (type(radius) != float and type(radius) != int) or radius < 0:
            print("Car.__init__: radius no es numero real positivo, se asigna valor de 10.")
            self.radius = 10

        else:
            self.radius = radius

        #Validacion de initSpeed
        if (type(initSpeed) != float and type(initSpeed) != int) or initSpeed < 0:
            print("Car.__init__: initSpeed no es numero real positivo, se asigna valor de 1.")
            self.radius = 1

        else:
            self.radius = radius

        #Declaracion de atributos
        self.firstPoint         = circuit.getPoints()[0]
        self.lastPoint          = self.firstPoint
        self.nextPoint          = self.firstPoint.getNeighbors()["N"]

        self.speed              = initSpeed #pix/s
        self.direction          = "N"
        self.posX               = self.lastPoint.getCoords()["x"]
        self.posY               = self.lastPoint.getCoords()["y"]
        self.vectors            = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "O": (-1, 0)}

        self.possibleDirections = ("N", "E", "S", "O")

    #Metodo para calcular la posicion siguiente del carro y actualizar el dibujo
    def move(self):
        #Posiciones siguientes
        tempX = self.posX + self.vectors[self.direction][0] * self.speed
        tempY = self.posY + self.vectors[self.direction][1] * self.speed

        gotToNext = False

        #Verifica si es movimiento vertical u horizontal
        if self.direction == "N" or self.direction == "S":
            #Verifica que no sobrepase el punto destino
            if self.vectors[self.direction][1] * (tempY - self.nextPoint.getCoords()["y"]) >= 0:
                self.posY = self.nextPoint.getCoords()["y"]
                gotToNext = True

            else:
                self.posY = tempY

        else:
            #Verfica que no sobrepase el punto destino
            if self.vectors[self.direction][0] * (tempX - self.nextPoint.getCoords()["x"]) >= 0:
                self.posX = self.nextPoint.getCoords()["x"]
                gotToNext = True

            else:
                self.posX = tempX

        #Se cambia de direccion si el carro llego a su punto destino
        if gotToNext:
            self.changeDirection()

        #Se mueve y dibuja el carro en screen
        self.updateGraphic()

    #Metodo para cambiar la direccion del carro cuando este llega al punto destino
    #Toma como direccion predeterminada la previa, sino gira a la derecha, sino a la izquierda
    def changeDirection(self):
        self.lastPoint = self.nextPoint

        neighbors = self.lastPoint.getNeighbors()

        for direction in self.getFavoredDirections():
            for neighborDirecc in neighbors:
                if neighborDirecc == direction:
                    self.nextPoint = neighbors[neighborDirecc]
                    self.direction = neighborDirecc
                    return

    #Para cada punto y direccion del carro, devuelve una lista con direcciones posteriores del carro en orden de prioridad
    #temp es una lista con strings de las direcciones dichas
    def getFavoredDirections(self):
        temp = list(self.possibleDirections)
        numDirections = len(self.possibleDirections)
        lastDirIx = temp.index(self.direction)

        #Hace un desplazamiento de la lista para que su primer elemento sea el de direccion previa
        temp = temp[lastDirIx:] + temp[:lastDirIx]
        lastDirIx = 0
        #Remueve la direccion que devuelve el carro al punto previo
        oppIx = (lastDirIx + 2) % numDirections
        temp.pop(oppIx)

        return temp

    #Metodo para dibujar el carro en su nueva posicion dentro de screen
    def updateGraphic(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)


















