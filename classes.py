#Clase para guardar cada punto del circuito
class Point:

    #Metodo constructor
    #self.identif es un numero entero para identificar y llamar a un punto
    #self.coords son las coordenadas en tupla, en pixeles, dentro de la ventana
    #self.neigbors es una lista con los puntos conectados al punto
    #self.numConns es la cantidad entera de puntos conectados al punto
    def __init__(self, identif, coords):
        if type(coords) != tuple or len(coords) != 2:
            print("Point: coords", coords, "no es valido.")
            return

        for elem in coords:
            if type(elem) != int or elem < 0:
                print("Point: coordenadas", coords, "no validas.")
                return

        self.identif = identif
        self.coords = coords
        self.neighbors = []
        self.numConns = 0

    #Metodo para agregar un punto vecino conectado al punto
    #point debe ser un objeto Point, aunque esto no se verifica
    def addNeighbor(self, point):
        #Verifica si el punto a agregar no es el objeto mismo
        if point == self:
            print("Point: punto no puede ser su propio vecino.")
            return

        #Verifica si punto a agregar ya esta en la lista
        for neighbor in self.neighbors:
            if point == neighbor:
                print("Point: vecino %d repetido dentro de punto %d." % (point.identif, self.identif))
                return

        self.neighbors += [point]
        self.numConns += 1

        #Debido a que cada conexion es bidireccional, verifica que no se agregue
        #el mimso punto al punto agregado
        for neighbor in point.neighbors:

            if neighbor == self:
                return

        point.addNeighbor(self)

    #Metodo para obtener puntos vecinos
    def getNeighbors(self):
        return self.neighbors

    #Metodo para obtener coordenadas del punto
    def getCoords(self):
        return self.coords

    #Metodo para obtener identificador del punto
    def getIdentif(self):
        return self.identif


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
        self.points += [newPoint]

        #Si ya el circuito tiene por lo menos un punto, i.e. no es None
        if self.lastPoint != None:
            self.lastPoint.addNeighbor(newPoint)

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
                self.lastPoint.addNeighbor(point)

                #Se agrega linea al circuito
                lastCoords = self.lastPoint.getCoords()
                newCoords = point.getCoords()
                self.lines += [(lastCoords, newCoords)]

                self.lastPoint = point
                return

        print("Circuit: no se encontro el punto deseado.")

    #Metodo para cambiar el ultimo punto del circuito
    #identif es el identificador del punto que se quiere como ultimo
    def changeLastTo(self, identif):
        for point in self.points:
            if point.getIdentif() == identif:
                self.lastPoint = point
                return

        print("Circuit: no se encontro el punto deseado.")

    #Metodo para obtener las lineas del circuito
    def getLines(self):
        return self.lines



















