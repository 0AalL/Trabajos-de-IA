
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class EditorHistogramasRGB:
    NOMBRES = ["Rojo (R)", "Verde (G)", "Azul (B)"]
    COLORES = ["red", "green", "blue"]

    def __init__(self, contenedor, al_modificar):
        self.al_modificar = al_modificar
        self.actuales = np.zeros((3, 256), dtype=float)
        self.originales = np.zeros((3, 256), dtype=float)
        self.objetivos = np.zeros((3, 256), dtype=float)

        self.canal_activo = None
        self.intensidad_activa = None
        self.altura_previa = None
        self.max_pixeles = 1
        self.barras_objetivo = []
        self.fondos = {}

        self.figura = Figure(figsize=(11, 7), dpi=85)
        self.ejes = [
            self.figura.add_subplot(311),
            self.figura.add_subplot(312),
            self.figura.add_subplot(313)
        ]

        self.figura.subplots_adjust(
            left=0.09, right=0.98,
            top=0.96, bottom=0.07, hspace=0.55
        )

        barra_controles = tk.Frame(contenedor)
        barra_controles.pack(fill="x", pady=(0, 4))

        self.botones_restablecer = []
        for canal, nombre in enumerate(("rojo", "verde", "azul")):
            boton = tk.Button(
                barra_controles,
                text=f"Restablecer {nombre}",
                command=lambda canal=canal: self.restablecer_canal(canal),
                state=tk.DISABLED
            )
            boton.pack(side="left", padx=(0, 4))
            self.botones_restablecer.append(boton)

        self.boton_aplicar = tk.Button(
            barra_controles,
            text="Aplicar cambios",
            command=self.aplicar,
            state=tk.DISABLED
        )
        self.boton_aplicar.pack(side="right")

        self.canvas = FigureCanvasTkAgg(
            self.figura, master=contenedor
        )
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        self.canvas.mpl_connect(
            "button_press_event", self.al_presionar
        )
        self.canvas.mpl_connect(
            "motion_notify_event", self.al_mover
        )
        self.canvas.mpl_connect(
            "button_release_event", self.al_soltar
        )
        self.canvas.mpl_connect("draw_event", self._guardar_fondos)

    def establecer_histogramas(self, histogramas):
        h = np.asarray(histogramas, dtype=float)

        self.originales = h.copy()
        self.actuales = h.copy()
        self.objetivos = h.copy()
        self.max_pixeles = max(float(h.max()), 1)
        self.boton_aplicar.config(state=tk.DISABLED)
        for boton in self.botones_restablecer:
            boton.config(state=tk.NORMAL)

        self.dibujar()

    def actualizar_actuales(self, histogramas):
        self.actuales = np.asarray(
            histogramas, dtype=float
        ).copy()
        self.max_pixeles = max(
            self.max_pixeles,
            float(self.actuales.max()),
            float(self.objetivos.max())
        )
        self.dibujar()

    def dibujar(self):
        x = np.arange(256)
        self.barras_objetivo = []
        self.fondos.clear()

        for c, eje in enumerate(self.ejes):
            eje.clear()

            barras = eje.bar(
                x, self.objetivos[c],
                width=0.9,
                color=self.COLORES[c],
                alpha=0.55,
                label="Histograma"
            )
            self.barras_objetivo.append(barras.patches)
            for barra in barras.patches:
                barra.set_animated(True)

            eje.step(
                x, self.originales[c],
                where="mid",
                color="#888888",
                linewidth=1.0,
                linestyle="--",
                label="Perfil original"
            )

            eje.set_xlim(0, 255)
            eje.set_ylim(0, self.max_pixeles * 1.05)
            eje.set_ylabel("Píxeles")
            eje.set_xlabel("Intensidad (0–255)")
            eje.set_title(self.NOMBRES[c])

            # Regiones tonales orientativas.
            eje.axvspan(0, 84, color="#777777", alpha=0.07)
            eje.axvspan(85, 170, color="#777777", alpha=0.04)
            eje.axvspan(171, 255, color="#777777", alpha=0.07)

            eje.text(
                0.16, 0.88, "Sombras",
                transform=eje.transAxes,
                ha="center", fontsize=8, color="#555555"
            )
            eje.text(
                0.50, 0.88, "Medios tonos",
                transform=eje.transAxes,
                ha="center", fontsize=8, color="#555555"
            )
            eje.text(
                0.84, 0.88, "Iluminaciones",
                transform=eje.transAxes,
                ha="center", fontsize=8, color="#555555"
            )

            eje.grid(axis="y", alpha=0.15)
            eje.legend(loc="upper right", fontsize=7)

        self.canvas.draw_idle()

    def _guardar_fondos(self, evento):
        self.fondos = {
            c: self.canvas.copy_from_bbox(eje.bbox)
            for c, eje in enumerate(self.ejes)
        }

        for eje, barras in zip(self.ejes, self.barras_objetivo):
            for barra in barras:
                eje.draw_artist(barra)
            self.canvas.blit(eje.bbox)

    def al_presionar(self, evento):
        if (
            evento.button != 1
            or evento.inaxes not in self.ejes
            or evento.xdata is None
            or evento.ydata is None
        ):
            return

        self.canal_activo = self.ejes.index(evento.inaxes)
        self.intensidad_activa = None
        self.altura_previa = None
        self._editar(evento.xdata, evento.ydata)

    def al_mover(self, evento):
        if (
            self.canal_activo is None
            or evento.inaxes != self.ejes[self.canal_activo]
            or evento.ydata is None
        ):
            return

        self._editar(evento.xdata, evento.ydata)

    def _editar(self, intensidad, altura):
        c = self.canal_activo
        if c is None:
            return

        intensidad = int(np.clip(round(intensidad), 0, 255))
        altura = float(np.clip(altura, 0, self.max_pixeles))

        if self.intensidad_activa is None:
            intensidades = np.array([intensidad])
            alturas = np.array([altura])
        else:
            paso = 1 if intensidad >= self.intensidad_activa else -1
            intensidades = np.arange(
                self.intensidad_activa, intensidad + paso, paso
            )
            alturas = np.linspace(
                self.altura_previa, altura, len(intensidades)
            )

        barras = []
        for indice, nueva_altura in zip(intensidades, alturas):
            self.objetivos[c, indice] = nueva_altura
            barra = self.barras_objetivo[c][indice]
            barra.set_height(nueva_altura)
            barras.append(barra)

        self.intensidad_activa = intensidad
        self.altura_previa = altura

        self._actualizar_estado_aplicar()

        fondo = self.fondos.get(c)
        if fondo is None:
            self.canvas.draw_idle()
            return

        self.canvas.restore_region(fondo)
        for barra in barras:
            self.ejes[c].draw_artist(barra)
        self.canvas.blit(self.ejes[c].bbox)

    def aplicar(self):
        aplicado = self.al_modificar(self.objetivos.copy())
        if aplicado is not False:
            self.objetivos = self.actuales.copy()
            self._actualizar_estado_aplicar()
            self.dibujar()

    def _actualizar_estado_aplicar(self):
        pendientes = not np.allclose(self.objetivos, self.actuales)
        self.boton_aplicar.config(
            state=tk.NORMAL if pendientes else tk.DISABLED
        )

    def restablecer_canal(self, canal):
        self.objetivos[canal] = self.originales[canal]
        self.dibujar()
        self._actualizar_estado_aplicar()

    def al_soltar(self, evento):
        self.canal_activo = None
        self.intensidad_activa = None
        self.altura_previa = None

    def restablecer(self):
        self.actuales = self.originales.copy()
        self.objetivos = self.originales.copy()
        self.dibujar()
        self.al_modificar(self.objetivos.copy())
        self.boton_aplicar.config(state=tk.DISABLED)
