
import tkinter as tk

try:
    from tkinterdnd2 import TkinterDnD
    ventana = TkinterDnD.Tk()
except ImportError:
    ventana = tk.Tk()

from interfaz import Aplicacion

if __name__ == "__main__":
    aplicacion = Aplicacion(ventana)
    ventana.mainloop()
