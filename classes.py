#Clase que mantiene global variables globales, y presenta el estado del programa para tomar decisiones
class ProgramStatus():

    #Metodo constructor
    def __init__(self):
        self.canContinue = False
        self.idleCar = False
        self.intVarCmd = None #prueba

        self.commandsByNum = {0: "N/A",
                              1: "Gira a la derecha y acelera",
                              2: "Gira a la izquierda y acelera",
                              3: "Gira a la derecha y desacelera",
                              4: "Gira a la izquierda y desacelera",
                              5: "Detención",
                              6: "Puesta en marcha"}

        #0: N/A
        #1: "Gira a la derecha y acelera"
        #2: "Gira a la izquierda y acelera"
        #3: "Gira a la derecha y desacelera"
        #4: "Gira a la izquierda y desacelera"
        #5: "Detención"
        #6: "Puesta en marcha"

        self.nextCommandNum = 0
        self.nextCommand = "N/A"

        self.clock = None #Tipo pygame.time.Clock
        self.stopTime = 0 #entero, milisegundos
        self.timeLeft = 0 #en segundos
        self.framerate = 60 #frames p sec


        # PRUEBAS----------------------------
        self.entry = None
        self.label = None

        # ------------------------------------

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
        #Validacion de number, caso nulo 0 se considera en else
        if type(number) == int and number >= 1 and number <= 6:
            self.nextCommandNum = number
            self.nextCommand = self.commandsByNum[number]

        else:
            self.nextCommandNum = 0
            self.nextCommand = self.commandsByNum[number]
            self.intVarCmd.set(0)




























