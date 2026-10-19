
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class EditorHistogramasRGB:
    NOMBRES = ["Rojo (R)", "Verde (G)", "Azul (B)"]
    COLORES = ["red", "green", "blue"]

    def __init__(
        self,
        contenedor,
        al_modificar,
        al_cambiar_contraste,
        al_restablecer_canal
    ):
        self.al_modificar = al_modificar
        self.al_cambiar_contraste = al_cambiar_contraste
        self.al_restablecer_canal = al_restablecer_canal
        self.actuales = np.zeros((3, 256), dtype=float)
        self.originales = np.zeros((3, 256), dtype=float)
        self.objetivos = np.zeros((3, 256), dtype=float)
        self.contrastes = np.ones(3, dtype=float)
        self.contrastes_aplicados = np.ones(3, dtype=float)

        self.canal_activo = None
        self.intensidad_activa = None
        self.altura_previa = None
        self.maximos_canales = np.ones(3, dtype=float)
        self.barras_objetivo = []
        self.barras_modificadas = [set(), set(), set()]
        self.perfiles_originales = []
        self.fondos = {}
        self.canales_histograma_pendientes = set()
        self.histogramas_establecidos = False
        self.arrastrando = False
        self.seleccion_imagen_activa = False
        self.botones_contraste = []

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

        tk.Label(
            contenedor,
            text="Arrastra las barras con el ratón para editar el histograma.",
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

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

        controles_contraste = tk.Frame(contenedor)
        controles_contraste.pack(fill="x", pady=(0, 4))
        for canal, nombre in enumerate(("R", "G", "B")):
            marco_contraste = tk.Frame(controles_contraste)
            marco_contraste.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(marco_contraste, text=f"Contraste {nombre}").pack(
                side="left", padx=(0, 4)
            )
            boton_menos = tk.Button(
                marco_contraste,
                text="-",
                command=lambda canal=canal: self.cambiar_contraste(
                    canal, -0.1
                ),
                state=tk.DISABLED
            )
            boton_menos.pack(side="left")
            tk.Button(
                marco_contraste,
                text="+",
                command=lambda canal=canal: self.cambiar_contraste(
                    canal, 0.1
                ),
                state=tk.DISABLED
            ).pack(side="left")
            self.botones_contraste.extend(
                (boton_menos, marco_contraste.winfo_children()[-1])
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
        self.canvas.mpl_connect("draw_event", self._guardar_fondos)

    def establecer_histogramas(self, histogramas):
        h = np.asarray(histogramas, dtype=float)

        self.originales = h.copy()
        self.actuales = h.copy()
        self.objetivos = h.copy()
        self.maximos_canales = np.maximum(h.max(axis=1), 1)
        self.contrastes[:] = 1.0
        self.contrastes_aplicados[:] = 1.0
        self.canales_histograma_pendientes.clear()
        self.histogramas_establecidos = True
        self.arrastrando = False
        self.boton_aplicar.config(state=tk.DISABLED)
        self._actualizar_estado_controles()
        for boton in self.botones_restablecer:
            boton.config(state=tk.NORMAL)

        self.dibujar()

    def actualizar_actuales(self, histogramas, canales):
        histogramas = np.asarray(histogramas, dtype=float)
        for canal in canales:
            self.actuales[canal] = histogramas[canal]
            self.objetivos[canal] = self.actuales[canal]
            self.maximos_canales[canal] = max(
                float(self.actuales[canal].max()), 1
            )
        self._actualizar_barras(canales)

    def dibujar(self):
        x = np.arange(256)
        self.barras_objetivo = []
        self.barras_modificadas = [set(), set(), set()]
        self.perfiles_originales = []
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

            maximo_original = max(float(self.originales[c].max()), 1)
            perfil, = eje.step(
                x, self.originales[c] / maximo_original,
                where="mid",
                color="#333333",
                linewidth=1.4,
                linestyle="--",
                label="Perfil original",
                zorder=5,
                transform=eje.get_xaxis_transform()
            )
            perfil.set_animated(True)
            self.perfiles_originales.append(perfil)

            eje.set_xlim(0, 255)
            eje.set_ylim(0, self.maximos_canales[c] * 1.05)
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

        for canal, (eje, barras) in enumerate(
            zip(self.ejes, self.barras_objetivo)
        ):
            for barra in barras:
                eje.draw_artist(barra)
            eje.draw_artist(self.perfiles_originales[canal])
            self.canvas.blit(eje.bbox)

    def _actualizar_barras(self, canales):
        for canal in canales:
            eje = self.ejes[canal]
            barras = self.barras_objetivo[canal]
            for intensidad, barra in enumerate(barras):
                barra.set_height(self.objetivos[canal, intensidad])

            eje.set_ylim(0, self.maximos_canales[canal] * 1.05)
            fondo = self.fondos.get(canal)
            if fondo is None:
                self.canvas.draw_idle()
                continue

            self.canvas.restore_region(fondo)
            for barra in barras:
                eje.draw_artist(barra)
            eje.draw_artist(self.perfiles_originales[canal])
            self.canvas.blit(eje.bbox)

    def actualizar_contraste_actual(self, canal, histograma):
        self.actuales[canal] = np.asarray(histograma, dtype=float)
        if canal not in self.canales_histograma_pendientes:
            self.objetivos[canal] = self.actuales[canal]
            self.maximos_canales[canal] = max(
                float(self.actuales[canal].max()), 1
            )
            self._actualizar_barras([canal])

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
        self.arrastrando = True
        self._actualizar_estado_controles()
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
        altura = float(np.clip(altura, 0, self.maximos_canales[c]))

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

        for indice, nueva_altura in zip(intensidades, alturas):
            self.objetivos[c, indice] = nueva_altura
            barra = self.barras_objetivo[c][indice]
            barra.set_height(nueva_altura)
            self.barras_modificadas[c].add(int(indice))
        self.canales_histograma_pendientes.add(c)

        self.intensidad_activa = intensidad
        self.altura_previa = altura

        self._actualizar_estado_aplicar()

        fondo = self.fondos.get(c)
        if fondo is None:
            self.canvas.draw_idle()
            return

        self.canvas.restore_region(fondo)
        for indice in self.barras_modificadas[c]:
            self.ejes[c].draw_artist(self.barras_objetivo[c][indice])
        self.ejes[c].draw_artist(self.perfiles_originales[c])
        self.canvas.blit(self.ejes[c].bbox)

    def aplicar(self):
        canales_modificados = sorted(self.canales_histograma_pendientes)
        if not canales_modificados:
            return

        aplicado = self.al_modificar(
            self.objetivos.copy(), self.contrastes.copy(), canales_modificados
        )
        if aplicado is not False:
            self.canales_histograma_pendientes.difference_update(
                canales_modificados
            )
            self._actualizar_barras(canales_modificados)
            self._actualizar_estado_controles()

    def cambiar_contraste(self, canal, incremento):
        if (
            not self.histogramas_establecidos
            or self.arrastrando
            or self.canales_histograma_pendientes
        ):
            return

        nuevo_contraste = np.clip(
            round(self.contrastes[canal] + incremento, 1), 1.0, 3.0
        )
        if np.isclose(nuevo_contraste, self.contrastes[canal]):
            return

        aplicado = self.al_cambiar_contraste(canal, nuevo_contraste)
        if aplicado is not False:
            self.contrastes[canal] = nuevo_contraste
            self.contrastes_aplicados[canal] = nuevo_contraste
            self._actualizar_estado_controles()

    def _actualizar_estado_aplicar(self):
        pendientes = bool(self.canales_histograma_pendientes)
        self.boton_aplicar.config(
            state=(
                tk.NORMAL
                if pendientes and not self.seleccion_imagen_activa
                else tk.DISABLED
            )
        )

    def establecer_seleccion_imagen(self, activa):
        self.seleccion_imagen_activa = bool(activa)
        self._actualizar_estado_controles()

    def _actualizar_estado_controles(self):
        self._actualizar_estado_aplicar()
        estado = (
            tk.NORMAL
            if self.histogramas_establecidos
            and not self.arrastrando
            and not self.canales_histograma_pendientes
            and not self.seleccion_imagen_activa
            else tk.DISABLED
        )
        for boton in self.botones_contraste:
            boton.config(state=estado)
        estado_restablecer = (
            tk.NORMAL
            if self.histogramas_establecidos
            and not self.arrastrando
            and not self.seleccion_imagen_activa
            else tk.DISABLED
        )
        for boton in self.botones_restablecer:
            boton.config(state=estado_restablecer)

    def restablecer_canal(self, canal):
        aplicado = self.al_restablecer_canal(canal)
        if aplicado is False:
            return

        self.actuales[canal] = self.originales[canal]
        self.objetivos[canal] = self.originales[canal]
        self.maximos_canales[canal] = max(
            float(self.originales[canal].max()), 1
        )
        self.contrastes[canal] = 1.0
        self.contrastes_aplicados[canal] = 1.0
        self.canales_histograma_pendientes.discard(canal)
        self._actualizar_barras([canal])
        self._actualizar_estado_controles()

    def al_soltar(self, evento):
        self.canal_activo = None
        self.intensidad_activa = None
        self.altura_previa = None
        self.arrastrando = False
        self._actualizar_estado_controles()

    def restablecer(self):
        self.actuales = self.originales.copy()
        self.objetivos = self.originales.copy()
        self.contrastes[:] = 1.0
        self.contrastes_aplicados[:] = 1.0
        self.canales_histograma_pendientes.clear()
        self.arrastrando = False
        self.dibujar()
        self.al_modificar(
            self.objetivos.copy(), self.contrastes.copy(), [0, 1, 2]
        )
        self._actualizar_estado_controles()
