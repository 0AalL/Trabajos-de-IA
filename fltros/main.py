import tkinter as tk
from tkinter import ttk

from ui.tiempo_tab import crear_tab_tiempo
from ui.frecuencia_tab import crear_tab_frecuencia

root = tk.Tk()
root.title("Procesamiento de Imágenes")
root.geometry("1400x900")
root.state("zoomed")

# Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tabs
tab_tiempo = tk.Frame(notebook)
tab_freq = tk.Frame(notebook)

notebook.add(tab_tiempo, text="Filtros en el Tiempo")
notebook.add(tab_freq, text="Filtros en Frecuencia")

# Crear contenido
crear_tab_tiempo(tab_tiempo)
crear_tab_frecuencia(tab_freq)

root.mainloop()