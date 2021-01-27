#Clase que mantiene global variables globales, y presenta el estado del programa para tomar decisiones
class ProgramStatus():

    #Metodo constructor
    def __init__(self):

        self.carIsRunning = True

        #Imagen actual recuperada del feed de camara
        self.currImage = None

        # Conteo de detección consecutiva del mismo comando
        self.sameCommandCount = 0

        # Conteo máximo para que un comando se mantenga activo hasta la siguiente intersección
        self.sameCommandMaxCount = 5

        #Atributo correspondiente a si el interfaz de pygame esta corriendo
        self.running = True

        #Numero de comando y descripcion
        self.commandsByNum = {0: ("N/A", "N/A"),
                              1: ("Gira a la derecha y acelera", "Der, Acc"),
                              2: ("Gira a la izquierda y acelera", "Izq, Acc"),
                              3: ("Gira a la derecha y desacelera", "Der, Des"),
                              4: ("Gira a la izquierda y desacelera", "Izq, Des"),
                              5: ("Detención", "Det"),
                              6: ("Puesta en marcha", "Cont")}

        #0: N/A
        #1: "Gira a la derecha y acelera"
        #2: "Gira a la izquierda y acelera"
        #3: "Gira a la derecha y desacelera"
        #4: "Gira a la izquierda y desacelera"
        #5: "Detención"
        #6: "Puesta en marcha"

        #Numero y texto del comando
        self.nextCommandNum = 0
        self.nextCommand = "N/A"

        #Reloj global
        self.clock = None #Tipo pygame.time.Clock

        #Tiempos usados para comando de detencion
        self.stopTime = 0 #entero, milisegundos
        self.timeLeft = 0 #en segundos

        #Taza de refrescado
        self.framerate = 60 #frames p sec

    #Metodo para cambiar el comando en algunas variables de la instancia
    #El numero number puede ser:
    # 0: N/A
    # 1: "Gira a la derecha y acelera"
    # 2: "Gira a la izquierda y acelera"
    # 3: "Gira a la derecha y desacelera"
    # 4: "Gira a la izquierda y desacelera"
    # 5: "Detención"
    # 6: "Puesta en marcha"
    def changeNextCmd(self, number):
        #Validacion de number, caso nulo 0 solo se considera si no se ha detectado ningun comando
        if type(number) == int and number >= 1 and number <= 6:
            self.nextCommandNum = number
            self.nextCommand = self.commandsByNum[number][1]

    #Metodo para reiniciar los atributos relacionados al comando
    def resetCmdNumber(self):
        self.nextCommandNum = 0
        self.nextCommand = self.commandsByNum[0][1]
        self.sameCommandCount = 0

    def resetSameCount(self):
        self.sameCommandCount = 0




























