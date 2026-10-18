
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import numpy as np
from PIL import Image, ImageTk

from imagenes import (
    cargar_imagen,
    calcular_histogramas,
    calcular_histogramas_transformados,
    transformar_rgb,
    guardar_imagen
)
from histogramas import EditorHistogramasRGB


class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Editor de histogramas RGB")
        self.ventana.geometry("1250x900")
        self.ventana.minsize(900, 650)

        self.original = None
        self.resultado = None
        self.hist_original = None
        self.hist_objetivo = None

        self.foto = None
        self.factor_x = 1.0
        self.factor_y = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.ancho_vista = 1
        self.alto_vista = 1
        self.muestras = []

        self.crear_interfaz()

    def crear_interfaz(self):
        barra = tk.Frame(self.ventana, padx=8, pady=6)
        barra.pack(fill="x")

        botones = [
            ("Abrir imagen", self.abrir),
            ("Restablecer", self.restablecer),
            ("Guardar resultado", self.guardar),
        ]

        for texto, accion in botones:
            tk.Button(
                barra, text=texto, command=accion
            ).pack(side="left", padx=3)

        self.estado = tk.Label(
            barra, text="Abre una imagen.", anchor="w"
        )
        self.estado.pack(side="left", padx=10)

        marco = tk.LabelFrame(
            self.ventana, text="Previsualización RGB",
            padx=5, pady=5
        )
        marco.pack(fill="x", padx=10, pady=4)

        self.canvas_imagen = tk.Canvas(
            marco, height=250, bg="#252525",
            highlightthickness=0
        )
        self.canvas_imagen.pack(fill="x", expand=True)

        self.canvas_imagen.bind(
            "<Motion>", self.mostrar_valores
        )
        self.canvas_imagen.bind(
            "<Button-1>", self.agregar_muestra
        )

        self.info_color = tk.Label(
            marco,
            text="Valores RGB: mueve el cursor sobre la imagen.",
            anchor="w"
        )
        self.info_color.pack(fill="x", pady=(5, 0))

        self.info_muestras = tk.Label(
            marco,
            text="Muestras de color: ninguna",
            anchor="w"
        )
        self.info_muestras.pack(fill="x")

        tk.Button(
            marco,
            text="Borrar muestras",
            command=self.borrar_muestras
        ).pack(anchor="e")

        marco_hist = tk.LabelFrame(
            self.ventana,
            text="Histograma: original, objetivo y previsualización",
            padx=5, pady=5
        )
        marco_hist.pack(
            fill="both", expand=True, padx=10, pady=5
        )

        self.editor = EditorHistogramasRGB(
            marco_hist, self.actualizar_previsualizacion
        )

        # Para arrastrar y soltar se necesita tkinterdnd2.
        try:
            from tkinterdnd2 import DND_FILES

            self.canvas_imagen.drop_target_register(DND_FILES)
            self.canvas_imagen.dnd_bind(
                "<<Drop>>", self.al_soltar_archivo
            )
        except (ImportError, tk.TclError):
            pass

    def abrir(self):
        ruta = filedialog.askopenfilename(
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.cargar(ruta)

    def al_soltar_archivo(self, evento):
        try:
            rutas = self.ventana.tk.splitlist(evento.data)
            if rutas:
                self.cargar(rutas[0])
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def cargar(self, ruta):
        try:
            self.original = cargar_imagen(ruta)
            self.resultado = self.original.copy()
            self.hist_original = calcular_histogramas(self.original)
            self.hist_objetivo = self.hist_original.astype(float)

            self.muestras.clear()
            self.actualizar_texto_muestras()

            self.editor.establecer_histogramas(self.hist_original)
            self.mostrar_imagen(self.resultado)

            self.estado.config(
                text=f"{Path(ruta).name} | "
                     f"{self.original.width} × {self.original.height}"
            )
        except Exception as error:
            messagebox.showerror("Error al abrir", str(error))

    def mostrar_imagen(self, imagen):
        self.canvas_imagen.delete("all")

        ancho_canvas = max(self.canvas_imagen.winfo_width(), 700)
        alto_canvas = 250

        vista = imagen.copy()
        vista.thumbnail((ancho_canvas, alto_canvas), Image.Resampling.LANCZOS)

        self.foto = ImageTk.PhotoImage(vista)

        self.ancho_vista = vista.width
        self.alto_vista = vista.height

        self.offset_x = (ancho_canvas - vista.width) // 2
        self.offset_y = (alto_canvas - vista.height) // 2

        self.factor_x = imagen.width / vista.width
        self.factor_y = imagen.height / vista.height

        self.canvas_imagen.configure(height=alto_canvas)
        self.canvas_imagen.create_image(
            self.offset_x, self.offset_y,
            image=self.foto, anchor="nw", tags="imagen"
        )

        # Dibujar las muestras sobre la vista previa.
        for numero, (x, y) in enumerate(self.muestras, 1):
            px = self.offset_x + x / self.factor_x
            py = self.offset_y + y / self.factor_y

            self.canvas_imagen.create_oval(
                px - 5, py - 5, px + 5, py + 5,
                outline="white", width=2
            )
            self.canvas_imagen.create_text(
                px + 10, py - 10,
                text=str(numero), fill="white"
            )

    def actualizar_previsualizacion(self, objetivos):
        if self.original is None:
            return False

        try:
            self.hist_objetivo = objetivos.copy()
            self.resultado = transformar_rgb(
                self.original,
                self.hist_objetivo,
                self.hist_original
            )

            histogramas = calcular_histogramas_transformados(
                self.hist_original, self.hist_objetivo
            )

            self.editor.actualizar_actuales(histogramas)
            self.mostrar_imagen(self.resultado)

            self.estado.config(text="Previsualización actualizada.")
            self.actualizar_texto_muestras()
            return True

        except Exception as error:
            self.estado.config(text=f"Error: {error}")
            return False

    def _coordenadas_imagen(self, x, y):
        px = x - self.offset_x
        py = y - self.offset_y

        if not (
            0 <= px < self.ancho_vista
            and 0 <= py < self.alto_vista
        ):
            return None

        ix = int(px * self.factor_x)
        iy = int(py * self.factor_y)

        ix = min(ix, self.original.width - 1)
        iy = min(iy, self.original.height - 1)

        return ix, iy

    def mostrar_valores(self, evento):
        if self.original is None or self.resultado is None:
            return

        coordenadas = self._coordenadas_imagen(evento.x, evento.y)
        if coordenadas is None:
            return

        x, y = coordenadas

        rgb_original = self.original.getpixel((x, y))
        rgb_ajustado = self.resultado.getpixel((x, y))

        self.info_color.config(
            text=(
                f"Píxel ({x}, {y}) | "
                f"Original RGB: {rgb_original} | "
                f"Ajustado RGB: {rgb_ajustado}"
            )
        )

    def agregar_muestra(self, evento):
        if self.original is None:
            return

        coordenadas = self._coordenadas_imagen(evento.x, evento.y)
        if coordenadas is None:
            return

        if len(self.muestras) >= 4:
            messagebox.showinfo(
                "Límite de muestras",
                "Puedes colocar hasta cuatro muestras. "
                "Borra las muestras para añadir otras."
            )
            return

        self.muestras.append(coordenadas)
        self.mostrar_imagen(self.resultado)
        self.actualizar_texto_muestras()

    def actualizar_texto_muestras(self):
        if not self.muestras or self.original is None:
            self.info_muestras.config(text="Muestras de color: ninguna")
            return

        lineas = []

        for i, (x, y) in enumerate(self.muestras, 1):
            original = self.original.getpixel((x, y))
            ajustado = self.resultado.getpixel((x, y))

            lineas.append(
                f"{i}: ({x},{y}) original={original}, ajustado={ajustado}"
            )

        self.info_muestras.config(text=" | ".join(lineas))

    def borrar_muestras(self):
        self.muestras.clear()

        if self.resultado is not None:
            self.mostrar_imagen(self.resultado)

        self.actualizar_texto_muestras()

    def restablecer(self):
        if self.original is None:
            return

        self.resultado = self.original.copy()
        self.hist_objetivo = self.hist_original.astype(float)

        self.muestras.clear()
        self.editor.establecer_histogramas(self.hist_original)
        self.mostrar_imagen(self.resultado)
        self.actualizar_texto_muestras()

        self.estado.config(text="Ajustes restablecidos.")

    def guardar(self):
        if self.resultado is None:
            messagebox.showinfo("Sin imagen", "Primero abre una imagen.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("TIFF", "*.tif"),
                ("BMP", "*.bmp")
            ]
        )

        if not ruta:
            return

        try:
            guardar_imagen(self.resultado, ruta)
            self.estado.config(
                text=f"Guardado: {Path(ruta).name}"
            )
        except Exception as error:
            messagebox.showerror("Error al guardar", str(error))
