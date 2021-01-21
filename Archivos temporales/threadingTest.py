import threading
import tkinter as tk
import time


class Mem:
    def __init__(self):
        self.entry = None
        self.text = None
        self.available = False


def interfaz():
    root = tk.Tk()
    root.geometry("200x100")
    f = tk.Frame(root)
    f.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Label(f, text="Ingrese texto:").pack()
    mem.entry = tk.Entry(f)
    mem.entry.pack()

    mem.text = tk.Label(f, text="-Texto-")
    mem.text.pack()

    mem.available = True

    # tk.Button(f, text = "Enviar", command = lambda:transmitMessage(e.get())).pack()

    tk.mainloop()


def transmitMessage():
    while True:
        print(mem.entry.get())
        mem.text.configure(text=mem.entry.get())


if __name__ == "__main__":
    mem = Mem()

    # https://realpython.com/intro-to-python-threading/
    threading.Thread(target=interfaz).start()

    while not mem.available:
        continue

    transmitMessage()
