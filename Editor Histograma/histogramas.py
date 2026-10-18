
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        self.max_pixeles = 1

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

    def establecer_histogramas(self, histogramas):
        h = np.asarray(histogramas, dtype=float)

        self.originales = h.copy()
        self.actuales = h.copy()
        self.objetivos = h.copy()
        self.max_pixeles = max(float(h.max()), 1)

        self.dibujar()

    def actualizar_actuales(self, histogramas):
        self.actuales = np.asarray(
            histogramas, dtype=float
        ).copy()
        self.dibujar()

    def dibujar(self):
        x = np.arange(256)

        for c, eje in enumerate(self.ejes):
            eje.clear()

            eje.bar(
                x, self.objetivos[c],
                width=0.9,
                color=self.COLORES[c],
                alpha=0.35,
                label="Objetivo"
            )

            eje.step(
                x, self.actuales[c],
                where="mid",
                color="black",
                linewidth=1.0,
                label="Previsualización"
            )

            eje.step(
                x, self.originales[c],
                where="mid",
                color="#888888",
                linewidth=0.8,
                linestyle="--",
                label="Original"
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

    def al_presionar(self, evento):
        if (
            evento.button != 1
            or evento.inaxes not in self.ejes
            or evento.xdata is None
            or evento.ydata is None
        ):
            return

        self.canal_activo = self.ejes.index(evento.inaxes)
        self.intensidad_activa = int(
            np.clip(round(evento.xdata), 0, 255)
        )

        self._editar(evento.ydata)

    def al_mover(self, evento):
        if (
            self.canal_activo is None
            or evento.inaxes != self.ejes[self.canal_activo]
            or evento.ydata is None
        ):
            return

        self._editar(evento.ydata)

    def _editar(self, altura):
        c = self.canal_activo
        i = self.intensidad_activa

        if c is None or i is None:
            return

        self.objetivos[c, i] = np.clip(
            altura, 0, self.max_pixeles
        )

        self.dibujar()

        # Solicita una nueva previsualización.
        self.al_modificar(self.objetivos.copy())

    def al_soltar(self, evento):
        self.canal_activo = None
        self.intensidad_activa = None

    def restablecer(self):
        self.actuales = self.originales.copy()
        self.objetivos = self.originales.copy()
        self.dibujar()
        self.al_modificar(self.objetivos.copy())
