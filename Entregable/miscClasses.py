#Clase que mantiene global variables globales, y presenta el estado del programa para tomar decisiones
class ProgramStatus():

    #Metodo constructor
    def __init__(self):
        # Atributo que corresponde a un continuo movimiento del carro
        self.carIsRunning = True

        #Imagen actual recuperada del feed de camara
        self.currImage = None

        #Atributo correspondiente a si el interfaz de pygame esta corriendo
        self.running = True

        #Numero de comando y descripcion
        self.commandsByNum = {0: ("N/A", "N/A"),
                              1: ("Gira a la derecha y acelera", "R, V+"),
                              2: ("Gira a la izquierda y acelera", "L, V+"),
                              3: ("Gira a la derecha y desacelera", "R, V-"),
                              4: ("Gira a la izquierda y desacelera", "L, V-"),
                              5: ("Detención", "Det"),
                              6: ("Puesta en marcha", "Cont")}

        #0: N/A
        #1: "Gira a la derecha y acelera"
        #2: "Gira a la izquierda y acelera"
        #3: "Gira a la derecha y desacelera"
        #4: "Gira a la izquierda y desacelera"
        #5: "Detención"
        #6: "Puesta en marcha"


        #Numero del comando
        self.nextCommandNum = 0
        #Numero del comando activado debido a lecturas consecutivas
        self.activeCommandNum = 0
        #Numero del comando anterior
        self.lastCommandNum = 0
        # Condicion si el comando es activo
        self.cmdIsActive = False


        # Conteo de detección consecutiva del mismo comando
        self.sameCommandCount = 0
        # Conteo máximo para que un comando se mantenga activo hasta la siguiente intersección
        self.sameCommandMaxCount = 5


        # Condicion si se detecto click
        self.clickDetected = False
        #Condicion si se mantiene click
        self.clickHeld = False


        #Reloj global
        self.clock = None #Tipo pygame.time.Clock


        #Tiempos usados para comando de detencion
        self.stopTime = 0 #entero, milisegundos
        self.timeLeft = 0 #en segundos


        #Taza de refrescado
        self.framerate = 60 #frames p sec

    # Metodo para cambiar el comando en algunas variables de la instancia
    # El numero number puede ser:
    # 0: N/A
    # 1: "Gira a la derecha y acelera"
    # 2: "Gira a la izquierda y acelera"
    # 3: "Gira a la derecha y desacelera"
    # 4: "Gira a la izquierda y desacelera"
    # 5: "Detención"
    # 6: "Puesta en marcha"
    def changeNextCmd(self, number):
        # Validacion de number
        if type(number) != int:
            self.resetCmdNumber()
            return

        #Memoria del comando anterior para conteo
        self.lastCommandNum = self.nextCommandNum

        #Nunca considera 0 para un comando valido
        if number >= 1 and number <= 6:
            self.nextCommandNum = number

            if number == self.lastCommandNum:
                self.sameCommandCount += 1

            else:
                self.sameCommandCount = 0

            self.changeActiveCmd(number)

    #Metodo para verificar si se activo el ultimo comando
    def isCommandActive(self):
        return self.sameCommandCount > self.sameCommandMaxCount

    # Metodo para cambiar el comando activo en algunas variables de la instancia
    def changeActiveCmd(self, command):
        if not self.cmdIsActive:
            self.activeCommandNum = command #Se actualiza solo si aun no ha llegado al maximo posible

            if self.isCommandActive():
                self.cmdIsActive = True

    #Metodo para activacion forzada de un comando, posiblemente por boton
    def forceActiveCmd(self, command):
        # Validacion de command
        if type(command) != int or (command < 0 and command > 6):
            return

        if 1 <= command <= 6:
            self.cmdIsActive = True
            self.activeCommandNum = command

        else:
            self.resetActiveCmd()


    # Metodo para reiniciar los atributos relacionados al comando
    def resetCmdNumber(self):
        self.nextCommandNum = 0
        self.sameCommandCount = 0

    # Metodo para reiniciar la bandera de comando activo
    def resetActiveCmd(self):
        self.cmdIsActive = False
        self.activeCommandNum = 0




































