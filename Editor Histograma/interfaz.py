
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import numpy as np
from PIL import Image, ImageTk

from imagenes import (
    cargar_imagen,
    calcular_histogramas,
    transformar_canal,
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
        self.zoom = 1.0
        self.escala_ajuste = None
        self.seleccion_inicio = None
        self.seleccion_roi = None
        self.rectangulo_seleccion = None
        self.ajustes_region = [[], [], []]

        self.crear_interfaz()

    def crear_interfaz(self):
        barra = tk.Frame(self.ventana, padx=8, pady=6)
        barra.pack(fill="x")

        botones = [
            ("Abrir imagen", self.abrir),
            ("Restablecer", self.restablecer),
            ("Guardar resultado", self.guardar),
        ]

        self.botones_generales = []
        for texto, accion in botones:
            boton = tk.Button(
                barra, text=texto, command=accion
            )
            boton.pack(side="left", padx=3)
            self.botones_generales.append(boton)

        self.estado = tk.Label(
            barra, text="Abre una imagen.", anchor="w"
        )
        self.estado.pack(side="left", padx=10)

        area_desplazable = tk.Frame(self.ventana)
        area_desplazable.pack(fill="both", expand=True)
        self.canvas_pagina = tk.Canvas(
            area_desplazable, highlightthickness=0
        )
        barra_vertical = tk.Scrollbar(
            area_desplazable,
            orient="vertical",
            command=self.canvas_pagina.yview
        )
        self.canvas_pagina.configure(yscrollcommand=barra_vertical.set)
        barra_vertical.pack(side="right", fill="y")
        self.canvas_pagina.pack(side="left", fill="both", expand=True)

        contenido = tk.Frame(self.canvas_pagina)
        self.ventana_contenido = self.canvas_pagina.create_window(
            (0, 0), window=contenido, anchor="nw"
        )
        contenido.bind(
            "<Configure>",
            lambda evento: self.canvas_pagina.configure(
                scrollregion=self.canvas_pagina.bbox("all")
            )
        )
        self.canvas_pagina.bind(
            "<Configure>",
            lambda evento: self.canvas_pagina.itemconfigure(
                self.ventana_contenido, width=evento.width
            )
        )

        marco = tk.LabelFrame(
            contenido, text="Previsualización RGB",
            padx=5, pady=5
        )
        marco.pack(fill="x", padx=10, pady=4)

        controles_imagen = tk.Frame(marco)
        controles_imagen.pack(fill="x", pady=(0, 4))
        self.botones_zoom = []
        boton_zoom_menos = tk.Button(
            controles_imagen, text="-", command=lambda: self.cambiar_zoom(0.8)
        )
        boton_zoom_menos.pack(side="left", padx=2)
        boton_zoom_mas = tk.Button(
            controles_imagen, text="+", command=lambda: self.cambiar_zoom(1.25)
        )
        boton_zoom_mas.pack(side="left", padx=2)
        boton_zoom_ajustar = tk.Button(
            controles_imagen, text="Ajustar", command=self.ajustar_zoom
        )
        boton_zoom_ajustar.pack(side="left", padx=4)
        self.botones_zoom.extend(
            (boton_zoom_menos, boton_zoom_mas, boton_zoom_ajustar)
        )
        self.boton_bajar_intensidad = tk.Button(
            controles_imagen,
            text="- Intensidad",
            command=lambda: self.ajustar_intensidad_seleccionada(-12),
            state=tk.DISABLED
        )
        self.boton_bajar_intensidad.pack(side="left", padx=(8, 2))
        self.boton_subir_intensidad = tk.Button(
            controles_imagen,
            text="+ Intensidad",
            command=lambda: self.ajustar_intensidad_seleccionada(12),
            state=tk.DISABLED
        )
        self.boton_subir_intensidad.pack(side="left", padx=2)
        self.boton_quitar_seleccion = tk.Button(
            controles_imagen,
            text="Quitar selección",
            command=self.quitar_seleccion,
            state=tk.DISABLED
        )
        self.boton_quitar_seleccion.pack(side="left", padx=(4, 2))
        self.boton_borrar_muestras = tk.Button(
            controles_imagen, text="Borrar muestras",
            command=self.borrar_muestras
        )
        self.boton_borrar_muestras.pack(side="right", padx=2)

        area_imagen = tk.Frame(marco)
        area_imagen.pack(fill="both", expand=True)
        self.canvas_imagen = tk.Canvas(
            area_imagen, height=520, bg="#252525",
            highlightthickness=0
        )
        barra_imagen_y = tk.Scrollbar(
            area_imagen,
            orient="vertical",
            command=self.canvas_imagen.yview
        )
        barra_imagen_x = tk.Scrollbar(
            area_imagen,
            orient="horizontal",
            command=self.canvas_imagen.xview
        )
        self.canvas_imagen.configure(
            xscrollcommand=barra_imagen_x.set,
            yscrollcommand=barra_imagen_y.set
        )
        barra_imagen_y.pack(side="right", fill="y")
        barra_imagen_x.pack(side="bottom", fill="x")
        self.canvas_imagen.pack(side="left", fill="both", expand=True)

        self.canvas_imagen.bind(
            "<Motion>", self.mostrar_valores
        )
        self.canvas_imagen.bind(
            "<ButtonPress-1>", self.iniciar_seleccion
        )
        self.canvas_imagen.bind(
            "<B1-Motion>", self.actualizar_seleccion
        )
        self.canvas_imagen.bind(
            "<ButtonRelease-1>", self.finalizar_seleccion
        )
        self.placeholder_imagen = self.canvas_imagen.create_text(
            0, 0,
            text="Carga una imagen para comenzar",
            fill="#d0d0d0",
            font=("TkDefaultFont", 16),
            anchor="center",
            tags="placeholder"
        )
        self.canvas_imagen.bind(
            "<Configure>", self.centrar_placeholder
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

        self.info_seleccion = tk.Label(
            marco,
            text="Arrastra sobre la imagen para seleccionar una zona.",
            anchor="w"
        )
        self.info_seleccion.pack(fill="x")

        marco_hist = tk.LabelFrame(
            contenido,
            text="Histograma: original, objetivo y previsualización",
            padx=5, pady=5
        )
        marco_hist.pack(
            fill="x", padx=10, pady=5
        )

        self.editor = EditorHistogramasRGB(
            marco_hist,
            self.actualizar_previsualizacion,
            self.actualizar_contraste,
            self.restablecer_canal_imagen
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
            self.zoom = 1.0
            self.escala_ajuste = None
            self.seleccion_inicio = None
            self.seleccion_roi = None
            self.rectangulo_seleccion = None
            self.ajustes_region = [[], [], []]
            self._actualizar_estado_seleccion()

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
        alto_canvas = max(self.canvas_imagen.winfo_height(), 500)
        if self.escala_ajuste is None:
            self.escala_ajuste = min(
                ancho_canvas / imagen.width,
                alto_canvas / imagen.height,
                1.0
            )

        escala = self.escala_ajuste * self.zoom
        escala = min(escala, 6000 / max(imagen.width, imagen.height))
        ancho_vista = max(1, round(imagen.width * escala))
        alto_vista = max(1, round(imagen.height * escala))
        vista = imagen.resize(
            (ancho_vista, alto_vista), Image.Resampling.BILINEAR
        )

        self.foto = ImageTk.PhotoImage(vista)

        self.ancho_vista = vista.width
        self.alto_vista = vista.height
        self.offset_x = 0
        self.offset_y = 0

        self.factor_x = imagen.width / vista.width
        self.factor_y = imagen.height / vista.height

        self.canvas_imagen.create_image(
            0, 0,
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

        if self.seleccion_roi is not None:
            x0, y0, x1, y1 = self.seleccion_roi
            self.rectangulo_seleccion = self.canvas_imagen.create_rectangle(
                x0 / self.factor_x,
                y0 / self.factor_y,
                x1 / self.factor_x,
                y1 / self.factor_y,
                outline="#ffe066",
                width=2,
                dash=(5, 3),
                tags="seleccion"
            )

        self.canvas_imagen.configure(
            scrollregion=self.canvas_imagen.bbox("all")
        )

    def iniciar_seleccion(self, evento):
        if self.original is None:
            return

        punto = self._coordenadas_imagen(evento.x, evento.y)
        if punto is None:
            self.seleccion_inicio = None
            return

        self.seleccion_inicio = (
            self.canvas_imagen.canvasx(evento.x),
            self.canvas_imagen.canvasy(evento.y),
            punto
        )
        if self.rectangulo_seleccion is not None:
            self.canvas_imagen.delete(self.rectangulo_seleccion)
            self.rectangulo_seleccion = None

    def actualizar_seleccion(self, evento):
        if self.seleccion_inicio is None:
            return

        x0, y0, _ = self.seleccion_inicio
        x1 = self.canvas_imagen.canvasx(evento.x)
        y1 = self.canvas_imagen.canvasy(evento.y)
        if self.rectangulo_seleccion is None:
            self.rectangulo_seleccion = self.canvas_imagen.create_rectangle(
                x0, y0, x1, y1,
                outline="#ffe066",
                width=2,
                dash=(5, 3),
                tags="seleccion"
            )
        else:
            self.canvas_imagen.coords(
                self.rectangulo_seleccion, x0, y0, x1, y1
            )

    def finalizar_seleccion(self, evento):
        if self.seleccion_inicio is None:
            return

        inicio_x, inicio_y, punto_inicio = self.seleccion_inicio
        punto_fin = self._coordenadas_imagen(evento.x, evento.y)
        fin_x = self.canvas_imagen.canvasx(evento.x)
        fin_y = self.canvas_imagen.canvasy(evento.y)
        es_rectangulo = (
            punto_fin is not None
            and (abs(fin_x - inicio_x) >= 5 or abs(fin_y - inicio_y) >= 5)
        )

        if self.rectangulo_seleccion is not None:
            self.canvas_imagen.delete(self.rectangulo_seleccion)
            self.rectangulo_seleccion = None

        if es_rectangulo:
            x0 = min(punto_inicio[0], punto_fin[0])
            y0 = min(punto_inicio[1], punto_fin[1])
            x1 = min(max(punto_inicio[0], punto_fin[0]) + 1, self.original.width)
            y1 = min(max(punto_inicio[1], punto_fin[1]) + 1, self.original.height)
            if x1 > x0 and y1 > y0:
                self.seleccion_roi = (x0, y0, x1, y1)
                self.info_seleccion.config(
                    text=f"Zona seleccionada: {x1 - x0} × {y1 - y0} píxeles"
                )
                self._actualizar_estado_seleccion()
                self.mostrar_imagen(self.resultado)
        else:
            self.seleccion_roi = None
            self.info_seleccion.config(
                text="Arrastra sobre la imagen para seleccionar una zona."
            )
            self._actualizar_estado_seleccion()
            self.agregar_muestra(evento)

        self.seleccion_inicio = None

    def _actualizar_botones_intensidad(self):
        estado = (
            tk.NORMAL
            if self.seleccion_roi is not None and self.resultado is not None
            else tk.DISABLED
        )
        self.boton_bajar_intensidad.config(state=estado)
        self.boton_subir_intensidad.config(state=estado)

    def _actualizar_estado_seleccion(self):
        seleccion_activa = self.seleccion_roi is not None
        estado = tk.DISABLED if seleccion_activa else tk.NORMAL

        for boton in self.botones_generales:
            boton.config(state=estado)
        for boton in self.botones_zoom:
            boton.config(state=estado)
        self.boton_borrar_muestras.config(state=estado)
        self.boton_quitar_seleccion.config(
            state=tk.NORMAL if seleccion_activa else tk.DISABLED
        )
        self._actualizar_botones_intensidad()
        self.editor.establecer_seleccion_imagen(seleccion_activa)

    def quitar_seleccion(self):
        self.seleccion_roi = None
        self.seleccion_inicio = None
        if self.rectangulo_seleccion is not None:
            self.canvas_imagen.delete(self.rectangulo_seleccion)
            self.rectangulo_seleccion = None
        self.info_seleccion.config(
            text="Arrastra sobre la imagen para seleccionar una zona."
        )
        self._actualizar_estado_seleccion()
        if self.resultado is not None:
            self.mostrar_imagen(self.resultado)

    def ajustar_intensidad_seleccionada(self, cantidad):
        if self.seleccion_roi is None or self.resultado is None:
            return
        if self.editor.canales_histograma_pendientes:
            self.estado.config(
                text="Aplica primero los cambios del histograma."
            )
            return

        x0, y0, x1, y1 = self.seleccion_roi
        pixeles = np.asarray(self.resultado, dtype=np.int16).copy()
        for canal in range(3):
            pixeles[y0:y1, x0:x1, canal] = np.clip(
                pixeles[y0:y1, x0:x1, canal] + cantidad, 0, 255
            )
            self.ajustes_region[canal].append(
                (x0, y0, x1, y1, cantidad)
            )

        self.resultado = Image.fromarray(pixeles.astype(np.uint8))
        histogramas = self.editor.actuales.copy()
        for canal in range(3):
            histogramas[canal] = np.bincount(
                pixeles[:, :, canal].astype(np.uint8).ravel(),
                minlength=256
            )
        self.editor.actualizar_actuales(histogramas, [0, 1, 2])
        self.mostrar_imagen(self.resultado)
        self.actualizar_texto_muestras()
        self.estado.config(text="Intensidad de la zona actualizada.")

    def _aplicar_ajustes_region(self, canal, valores):
        salida = np.asarray(valores, dtype=np.int16).copy()
        for x0, y0, x1, y1, cantidad in self.ajustes_region[canal]:
            salida[y0:y1, x0:x1] = np.clip(
                salida[y0:y1, x0:x1] + cantidad, 0, 255
            )
        return salida.astype(np.uint8)

    def centrar_placeholder(self, evento):
        if self.original is None:
            self.canvas_imagen.coords(
                self.placeholder_imagen,
                self.canvas_imagen.canvasx(evento.width / 2),
                self.canvas_imagen.canvasy(evento.height / 2)
            )
            self.canvas_imagen.configure(
                scrollregion=(0, 0, evento.width, evento.height)
            )

    def cambiar_zoom(self, factor):
        if self.resultado is None:
            return
        self.zoom = float(np.clip(self.zoom * factor, 0.25, 6.0))
        self.mostrar_imagen(self.resultado)

    def ajustar_zoom(self):
        if self.resultado is None:
            return
        self.zoom = 1.0
        self.escala_ajuste = None
        self.mostrar_imagen(self.resultado)

    def actualizar_previsualizacion(
        self, objetivos, contrastes, canales_modificados
    ):
        if self.original is None:
            return False
        if not canales_modificados:
            return True

        try:
            histograma_nuevo = self.hist_objetivo.copy()
            transformaciones = {}
            for canal in canales_modificados:
                histograma_nuevo[canal] = objetivos[canal]
                valores = transformar_canal(
                    np.asarray(self.original.getchannel(canal)),
                    histograma_nuevo[canal],
                    self.hist_original[canal],
                    contrastes[canal]
                )
                valores = self._aplicar_ajustes_region(canal, valores)
                transformaciones[canal] = Image.fromarray(valores)

            imagen_actual = (
                self.resultado
                if self.resultado is not None
                else self.original
            )
            canales_resultado = list(imagen_actual.split())
            for canal, transformacion in transformaciones.items():
                canales_resultado[canal] = transformacion
            self.resultado = Image.merge("RGB", tuple(canales_resultado))
            self.hist_objetivo = histograma_nuevo

            histogramas = self.editor.actuales.copy()
            for canal in canales_modificados:
                valores = np.asarray(self.resultado.getchannel(canal))
                histogramas[canal] = np.bincount(
                    valores.ravel(), minlength=256
                )

            self.editor.actualizar_actuales(histogramas, canales_modificados)
            self.mostrar_imagen(self.resultado)

            self.estado.config(text="Previsualización actualizada.")
            self.actualizar_texto_muestras()
            return True

        except Exception as error:
            self.estado.config(text=f"Error: {error}")
            return False

    def actualizar_contraste(self, canal, contraste):
        if self.original is None:
            return False

        try:
            valores = transformar_canal(
                np.asarray(self.original.getchannel(canal)),
                self.hist_objetivo[canal],
                self.hist_original[canal],
                contraste
            )
            valores = self._aplicar_ajustes_region(canal, valores)
            canal_resultado = Image.fromarray(valores)
            canales_resultado = list(self.resultado.split())
            canales_resultado[canal] = canal_resultado
            self.resultado = Image.merge("RGB", tuple(canales_resultado))

            histograma = np.bincount(valores.ravel(), minlength=256)
            self.editor.actualizar_contraste_actual(canal, histograma)
            self.mostrar_imagen(self.resultado)
            self.actualizar_texto_muestras()
            self.estado.config(text="Contraste actualizado.")
            return True
        except Exception as error:
            self.estado.config(text=f"Error: {error}")
            return False

    def restablecer_canal_imagen(self, canal):
        if self.original is None:
            return False

        self.ajustes_region[canal].clear()
        canales = list(self.resultado.split())
        canales[canal] = self.original.getchannel(canal)
        self.resultado = Image.merge("RGB", tuple(canales))
        self.hist_objetivo[canal] = self.hist_original[canal]
        self.mostrar_imagen(self.resultado)
        self.actualizar_texto_muestras()
        self.estado.config(text="Canal restablecido al original.")
        return True

    def _coordenadas_imagen(self, x, y):
        px = self.canvas_imagen.canvasx(x) - self.offset_x
        py = self.canvas_imagen.canvasy(y) - self.offset_y

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
        self.ajustes_region = [[], [], []]
        self.seleccion_roi = None
        self.info_seleccion.config(
            text="Arrastra sobre la imagen para seleccionar una zona."
        )
        self._actualizar_botones_intensidad()
        self.zoom = 1.0
        self.escala_ajuste = None

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
