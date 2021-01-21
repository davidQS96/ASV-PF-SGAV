import multiprocessing as mp
import transmitter as trm
import tkinter as tk



def interfaz():
    root = tk.Tk()
    root.geometry("200x100")
    f = tk.Frame(root)
    f.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
    tk.Label(f, text = "Ingrese texto:").pack()
    e = tk.Entry(f)
    e.pack()
    tk.Button(f, text = "Enviar", command = lambda:transmitMessage(e.get())).pack()


    tk.mainloop()



if __name__ == "__main__":
    #https://www.youtube.com/watch?v=sp7EhjLkFY4&ab_channel=codebasics
    #https://docs.python.org/3/library/multiprocessing.html
    # numbers = [2, 3, 6, 10, 20]
    q = mp.Queue()
    # print("alo")
    p = mp.Process(target = trm.interfaz, args = (q, ))

    p.start()
    p.join()

    interfaz()

    while q.empty() is False:
        print(q.get())



