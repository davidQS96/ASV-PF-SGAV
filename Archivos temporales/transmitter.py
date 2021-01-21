import tkinter as tk

def interfaz(queue):
    root = tk.Tk()
    root.geometry("200x100")
    f = tk.Frame(root)
    f.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
    tk.Label(f, text = "Ingrese texto:").pack()
    e = tk.Entry(f)
    e.pack()
    tk.Button(f, text = "Enviar", command = lambda:transmitMessage(e.get(), queue)).pack()


    tk.mainloop()


def transmitMessage(entryStr, queue):
    queue.put(entryStr)





