import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from configuracion import (
    RANGOS,
    VARIABLES_ENTRADA,
    PARAMETROS_MEMBRESIA,
    UNIVERSOS
)

from fuzzificacion import (
    fuzzificar_entradas,
    obtener_dominantes
)

from reglas import (
    cargar_reglas,
    regla_a_texto
)

from inferencia import (
    evaluar_reglas,
    agregar_salidas
)

from defuzzificacion import (
    defuzzificar_centroide,
    clasificar_riesgo
)


# =========================================================
# INTERFAZ
# =========================================================

class Aplicacion:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Sistema Difuso - Riesgo de Incendios"
        )

        self.root.geometry(
            "1250x800"
        )

        self.root.minsize(
            1050,
            700
        )

        self.root.resizable(
            True,
            True
        )

        # ---------------------------------------------
        # CARGAR REGLAS
        # ---------------------------------------------

        try:

            self.reglas = cargar_reglas()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo cargar reglas_finales.csv\n\n{error}"
            )

            self.reglas = []

        # ---------------------------------------------
        # VARIABLES PARA LOS CAMPOS DE ENTRADA
        # ---------------------------------------------

        self.entries = {}

        # ---------------------------------------------
        # VARIABLES PARA LAS GRÁFICAS
        # ---------------------------------------------

        self.variables_graficas = (
            VARIABLES_ENTRADA
            + ["Area Quemada (Ha)"]
        )

        self.indice_grafica = 0

        self.canvas_grafica = None

        # ---------------------------------------------
        # CREAR INTERFAZ
        # ---------------------------------------------

        self.crear_interfaz()


    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        # -------------------------------------------------
        # TITULO
        # -------------------------------------------------

        titulo = ttk.Label(
            self.root,
            text="SISTEMA DIFUSO PARA EVALUACIÓN DE INCENDIOS",
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            pady=(15, 5)
        )


        subtitulo = ttk.Label(
            self.root,
            text=(
                "Inferencia Mamdani | "
                "AND = MIN | "
                "Agregación = MAX | "
                "Defuzzificación = CENTROIDE"
            ),
            font=("Arial", 10)
        )

        subtitulo.pack(
            pady=(0, 10)
        )


        # =================================================
        # PANEL SUPERIOR
        # =================================================

        panel_principal = ttk.Frame(
            self.root
        )

        panel_principal.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )


        # =================================================
        # PANEL DE ENTRADAS
        # =================================================

        frame_entradas = ttk.LabelFrame(
            panel_principal,
            text="Datos de entrada",
            padding=15
        )

        frame_entradas.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="nsew"
        )


        # -------------------------------------------------
        # NOMBRES DE LAS VARIABLES
        # -------------------------------------------------

        nombres = {

            "T_media":
                "Temperatura (°C)",

            "HR_media":
                "Humedad (%)",

            "Viento_medio":
                "Viento (m/s)",

            "Precipitacion":
                "Precipitación (mm)",

            "FFMC":
                "FFMC (Combustible Fino)",

            "DMC":
                "DMC (Capa Orgánica)",

            "DC":
                "DC (Sequía)",

            "KBDI":
                "KBDI"
        }


        # -------------------------------------------------
        # CAMPOS DE ENTRADA
        # -------------------------------------------------

        for fila, variable in enumerate(
            VARIABLES_ENTRADA
        ):

            minimo, maximo = RANGOS[
                variable
            ]


            etiqueta = ttk.Label(
                frame_entradas,
                text=nombres[variable]
            )

            etiqueta.grid(
                row=fila,
                column=0,
                padx=8,
                pady=6,
                sticky="w"
            )


            # Valor inicial
            valor_inicial = (
                minimo + maximo
            ) / 2


            entry = ttk.Entry(
                frame_entradas,
                width=14
            )

            entry.insert(
                0,
                str(valor_inicial)
            )

            entry.grid(
                row=fila,
                column=1,
                padx=8,
                pady=6
            )


            # Mostrar rango
            rango = ttk.Label(
                frame_entradas,
                text=(
                    f"{minimo} - {maximo}"
                )
            )

            rango.grid(
                row=fila,
                column=2,
                padx=8,
                pady=6,
                sticky="w"
            )


            self.entries[
                variable
            ] = entry


        # -------------------------------------------------
        # BOTÓN CALCULAR
        # -------------------------------------------------

        boton = ttk.Button(
            frame_entradas,
            text="CALCULAR RIESGO",
            command=self.calcular
        )

        boton.grid(
            row=len(VARIABLES_ENTRADA),
            column=0,
            columnspan=3,
            pady=(15, 5)
        )


        # =================================================
        # PANEL DE FUNCIONES DE PERTENENCIA
        # =================================================

        frame_pertenencia = ttk.LabelFrame(
            panel_principal,
            text="Funciones de pertenencia",
            padding=10
        )

        frame_pertenencia.grid(
            row=0,
            column=1,
            padx=(10, 0),
            sticky="nsew"
        )


        # -------------------------------------------------
        # TÍTULO DE LA VARIABLE
        # -------------------------------------------------

        self.titulo_grafica = ttk.Label(
            frame_pertenencia,
            text="",
            font=("Arial", 14, "bold")
        )

        self.titulo_grafica.pack(
            pady=(5, 5)
        )


        # -------------------------------------------------
        # CONTENEDOR DE GRÁFICA
        # -------------------------------------------------

        self.frame_grafica = ttk.Frame(
            frame_pertenencia
        )

        self.frame_grafica.pack(
            fill="both",
            expand=True
        )


        # -------------------------------------------------
        # BOTONES DE NAVEGACIÓN
        # -------------------------------------------------

        frame_botones = ttk.Frame(
            frame_pertenencia
        )

        frame_botones.pack(
            fill="x",
            pady=(5, 0)
        )


        self.boton_anterior = ttk.Button(
            frame_botones,
            text="◀ Anterior",
            command=self.grafica_anterior
        )

        self.boton_anterior.pack(
            side="left",
            padx=5
        )


        self.indicador_grafica = ttk.Label(
            frame_botones,
            text=""
        )

        self.indicador_grafica.pack(
            side="left",
            expand=True
        )


        self.boton_siguiente = ttk.Button(
            frame_botones,
            text="Siguiente ▶",
            command=self.grafica_siguiente
        )

        self.boton_siguiente.pack(
            side="right",
            padx=5
        )


        # -------------------------------------------------
        # CONFIGURAR COLUMNAS Y FILAS
        # -------------------------------------------------

        panel_principal.columnconfigure(
            0,
            weight=1
        )

        panel_principal.columnconfigure(
            1,
            weight=2
        )

        panel_principal.rowconfigure(
            0,
            weight=1
        )


        # -------------------------------------------------
        # MOSTRAR PRIMERA GRÁFICA
        # -------------------------------------------------

        self.mostrar_grafica_actual()



        # =================================================
        # BOTONES DE PREAJUSTES PARA DEMOSTRACIÓN / DEFENSA
        # =================================================

        frame_presets = ttk.LabelFrame(
            self.root,
            text="Escenarios Predefinidos de Prueba (Demostración / Defensa)",
            padding=10
        )
        frame_presets.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        btn_nulo = ttk.Button(
            frame_presets,
            text="1. Invernal (Nulo)",
            command=lambda: self.cargar_caso({
                'T_media': -10.0, 'HR_media': 85.0, 'Viento_medio': 1.0,
                'Precipitacion': 0.05, 'FFMC': 10.0, 'DMC': 80.0,
                'DC': 550.0, 'KBDI': 150.0
            })
        )
        btn_nulo.pack(side="left", padx=5, expand=True, fill="x")

        btn_bajo = ttk.Button(
            frame_presets,
            text="2. Moderado (Bajo)",
            command=lambda: self.cargar_caso({
                'T_media': 12.0, 'HR_media': 75.0, 'Viento_medio': 2.0,
                'Precipitacion': 0.001, 'FFMC': 70.0, 'DMC': 25.0,
                'DC': 150.0, 'KBDI': 15.0
            })
        )
        btn_bajo.pack(side="left", padx=5, expand=True, fill="x")

        btn_alto = ttk.Button(
            frame_presets,
            text="3. Seco/Viento (Alto)",
            command=lambda: self.cargar_caso({
                'T_media': 8.0, 'HR_media': 30.0, 'Viento_medio': 2.0,
                'Precipitacion': 0.0, 'FFMC': 92.0, 'DMC': 35.0,
                'DC': 450.0, 'KBDI': 1.0
            })
        )
        btn_alto.pack(side="left", padx=5, expand=True, fill="x")

        btn_extremo = ttk.Button(
            frame_presets,
            text="4. Ola Calor (Extremo)",
            command=lambda: self.cargar_caso({
                'T_media': 25.0, 'HR_media': 55.0, 'Viento_medio': 2.8,
                'Precipitacion': 0.0, 'FFMC': 87.0, 'DMC': 130.0,
                'DC': 550.0, 'KBDI': 80.0
            })
        )
        btn_extremo.pack(side="left", padx=5, expand=True, fill="x")


        # =================================================
        # RESULTADO
        # =================================================

        frame_resultado = ttk.LabelFrame(
            self.root,
            text="Resultado",
            padding=10
        )

        frame_resultado.pack(
            padx=20,
            pady=5,
            fill="x"
        )


        self.resultado = ttk.Label(
            frame_resultado,
            text="Área Estimada: -- Ha",
            font=("Arial", 22, "bold")
        )

        self.resultado.pack(
            pady=5
        )


        self.clasificacion = ttk.Label(
            frame_resultado,
            text="Clasificación: --",
            font=("Arial", 13)
        )

        self.clasificacion.pack(
            pady=3
        )


        # =================================================
        # NOTEBOOK
        # =================================================

        notebook = ttk.Notebook(
            self.root
        )

        notebook.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )


        # =================================================
        # TAB FUZZIFICACIÓN
        # =================================================

        frame_fuzzy = ttk.Frame(
            notebook
        )

        notebook.add(
            frame_fuzzy,
            text="Fuzzificación"
        )


        self.texto_fuzzy = tk.Text(
            frame_fuzzy,
            font=("Consolas", 10)
        )

        self.texto_fuzzy.pack(
            fill="both",
            expand=True
        )


        # =================================================
        # TAB REGLAS
        # =================================================

        frame_reglas = ttk.Frame(
            notebook
        )

        notebook.add(
            frame_reglas,
            text="Reglas activadas"
        )


        self.texto_reglas = tk.Text(
            frame_reglas,
            font=("Consolas", 10)
        )

        self.texto_reglas.pack(
            fill="both",
            expand=True
        )


        # =================================================
        # TAB INFORMACIÓN
        # =================================================

        frame_info = ttk.Frame(
            notebook
        )

        notebook.add(
            frame_info,
            text="Información"
        )


        info = (
            "SISTEMA DIFUSO\n\n"

            f"Reglas cargadas: {len(self.reglas)}\n\n"

            "Método de inferencia: Mamdani\n"

            "Operador AND: MIN\n"

            "Implicación: MIN\n"

            "Agregación: MAX\n"

            "Defuzzificación: CENTROIDE\n\n"

            "Universo de salida: Hectáreas Quemadas"
        )


        ttk.Label(
            frame_info,
            text=info,
            font=("Arial", 12),
            justify="left"
        ).pack(
            padx=20,
            pady=20,
            anchor="nw"
        )


    # =====================================================
    # FUNCIÓN TRAPEZOIDAL
    # =====================================================

    def funcion_trapezoidal(
        self,
        x,
        parametros
    ):

        a, b, c, d = parametros

        y = np.zeros_like(
            x,
            dtype=float
        )


        # -------------------------------------------------
        # ASCENSO
        # -------------------------------------------------

        if b != a:

            mascara = (
                (x > a) &
                (x < b)
            )

            y[mascara] = (
                (x[mascara] - a)
                /
                (b - a)
            )


        # -------------------------------------------------
        # PARTE SUPERIOR
        # -------------------------------------------------

        mascara = (
            (x >= b) &
            (x <= c)
        )

        y[mascara] = 1.0


        # -------------------------------------------------
        # DESCENSO
        # -------------------------------------------------

        if d != c:

            mascara = (
                (x > c) &
                (x < d)
            )

            y[mascara] = (
                (d - x[mascara])
                /
                (d - c)
            )


        return y


    # =====================================================
    # MOSTRAR GRÁFICA ACTUAL
    # =====================================================

    def mostrar_grafica_actual(
        self
    ):

        variable = (
            self.variables_graficas[
                self.indice_grafica
            ]
        )


        # -------------------------------------------------
        # NOMBRES PARA MOSTRAR EN LA INTERFAZ
        # -------------------------------------------------

        nombres = {

            "T_media":
                "Temperatura media (°C)",

            "HR_media":
                "Humedad relativa media (%)",

            "Viento_medio":
                "Velocidad media del viento (m/s)",

            "Precipitacion":
                "Precipitación (mm)",

            "FFMC":
                "Fine Fuel Moisture Code (FFMC)",

            "DMC":
                "Duff Moisture Code (DMC)",

            "DC":
                "Drought Code (DC)",

            "KBDI":
                "Keetch-Byram Drought Index (KBDI)",

            "Area Quemada (Ha)":
                "Área Quemada (Ha)"
        }


        # -------------------------------------------------
        # ACTUALIZAR TÍTULO
        # -------------------------------------------------

        self.titulo_grafica.config(
            text=nombres.get(
                variable,
                variable
            )
        )


        # -------------------------------------------------
        # ELIMINAR GRÁFICA ANTERIOR
        # -------------------------------------------------

        for widget in (
            self.frame_grafica.winfo_children()
        ):

            widget.destroy()


        # -------------------------------------------------
        # OBTENER UNIVERSO
        # -------------------------------------------------

        universo = UNIVERSOS[
            variable
        ]


        # -------------------------------------------------
        # OBTENER PARÁMETROS
        # -------------------------------------------------

        parametros_variable = (
            PARAMETROS_MEMBRESIA[
                variable
            ]
        )


        # =================================================
        # UNIVERSO EXCLUSIVO PARA VISUALIZACIÓN
        # =================================================
        #
        # IMPORTANTE:
        #
        # El universo real de "Area Quemada (Ha)"
        # continúa siendo:
        #
        # 0 -> 1 889 779.32 ha
        #
        # y se utiliza para inferencia y defuzzificación.
        #
        # Sin embargo, para visualizar las funciones
        # de pertenencia no es conveniente mostrar todo
        # ese rango porque las funciones LOW y HIGH
        # quedarían comprimidas en el extremo izquierdo.
        #
        # Por eso solamente para la gráfica se utiliza
        # una ventana de 0 -> 10 000 ha.
        #
        # =================================================

        if variable == "Area Quemada (Ha)":

            universo_grafica = np.linspace(
                0.0,
                10000.0,
                2000
            )

        else:

            universo_grafica = universo


        # -------------------------------------------------
        # CREAR FIGURA
        # -------------------------------------------------

        figura = Figure(
            figsize=(7, 4.2),
            dpi=100
        )


        ax = figura.add_subplot(
            111
        )


        # -------------------------------------------------
        # GRAFICAR FUNCIONES
        # -------------------------------------------------

        for conjunto, parametros in (
            parametros_variable.items()
        ):

            y = self.funcion_trapezoidal(
                universo_grafica,
                parametros
            )


            ax.plot(
                universo_grafica,
                y,
                linewidth=2,
                label=conjunto
            )


        # -------------------------------------------------
        # CONFIGURACIÓN DEL EJE X
        # -------------------------------------------------

        if variable == "Area Quemada (Ha)":

            ax.set_xlim(
                0,
                10000
            )

            ax.set_xlabel(
                "Área Quemada (Ha)"
            )

        else:

            ax.set_xlabel(
                nombres.get(
                    variable,
                    variable
                )
            )


        # -------------------------------------------------
        # EJE Y
        # -------------------------------------------------

        ax.set_ylabel(
            "Grado de pertenencia"
        )


        # -------------------------------------------------
        # LÍMITES DEL EJE Y
        # -------------------------------------------------

        ax.set_ylim(
            -0.05,
            1.05
        )


        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        ax.set_title(
            "Funciones de pertenencia"
        )


        # -------------------------------------------------
        # CUADRÍCULA
        # -------------------------------------------------

        ax.grid(
            True,
            alpha=0.3
        )


        # -------------------------------------------------
        # LEYENDA
        # -------------------------------------------------

        ax.legend(
            loc="best"
        )


        # -------------------------------------------------
        # AJUSTAR ESPACIADO
        # -------------------------------------------------

        figura.tight_layout()


        # -------------------------------------------------
        # INSERTAR EN TKINTER
        # -------------------------------------------------

        self.canvas_grafica = (
            FigureCanvasTkAgg(
                figura,
                master=self.frame_grafica
            )
        )


        self.canvas_grafica.draw()


        self.canvas_grafica.get_tk_widget().pack(
            fill="both",
            expand=True
        )


        # -------------------------------------------------
        # INDICADOR
        # -------------------------------------------------

        total = len(
            self.variables_graficas
        )


        self.indicador_grafica.config(
            text=(
                f"{self.indice_grafica + 1} "
                f"de {total}"
            )
        )


        # -------------------------------------------------
        # ESTADO DEL BOTÓN ANTERIOR
        # -------------------------------------------------

        if self.indice_grafica == 0:

            self.boton_anterior.config(
                state="disabled"
            )

        else:

            self.boton_anterior.config(
                state="normal"
            )


        # -------------------------------------------------
        # ESTADO DEL BOTÓN SIGUIENTE
        # -------------------------------------------------

        if (
            self.indice_grafica
            ==
            total - 1
        ):

            self.boton_siguiente.config(
                state="disabled"
            )

        else:

            self.boton_siguiente.config(
                state="normal"
            )


    # =====================================================
    # GRÁFICA SIGUIENTE
    # =====================================================

    def grafica_siguiente(
        self
    ):

        if (
            self.indice_grafica
            <
            len(
                self.variables_graficas
            ) - 1
        ):

            self.indice_grafica += 1

            self.mostrar_grafica_actual()


    # =====================================================
    # GRÁFICA ANTERIOR
    # =====================================================

    def grafica_anterior(
        self
    ):

        if self.indice_grafica > 0:

            self.indice_grafica -= 1

            self.mostrar_grafica_actual()



    # =====================================================
    # CARGAR CASO PREESTABLECIDO
    # =====================================================

    def cargar_caso(self, valores):
        for variable, valor in valores.items():
            if variable in self.entries:
                self.entries[variable].delete(0, tk.END)
                self.entries[variable].insert(0, str(valor))
        self.calcular()


    # =====================================================
    # CALCULAR
    # =====================================================

    def calcular(self):

        entradas = {}


        # -------------------------------------------------
        # LEER Y VALIDAR
        # -------------------------------------------------

        try:

            for variable in VARIABLES_ENTRADA:

                texto = self.entries[
                    variable
                ].get().strip()


                if not texto:

                    raise ValueError(
                        f"Debe ingresar {variable}."
                    )


                valor = float(
                    texto
                )


                minimo, maximo = RANGOS[
                    variable
                ]


                if (
                    valor < minimo
                    or
                    valor > maximo
                ):

                    raise ValueError(
                        f"{variable}: "
                        f"el valor debe estar entre "
                        f"{minimo} y {maximo}."
                    )


                entradas[
                    variable
                ] = valor


        except ValueError as error:

            messagebox.showerror(
                "Valor inválido",
                str(error)
            )

            return


        # -------------------------------------------------
        # FUZZIFICACIÓN
        # -------------------------------------------------

        fuzzificados = fuzzificar_entradas(
            entradas
        )


        dominantes = obtener_dominantes(
            fuzzificados
        )


        self.mostrar_fuzzificacion(
            fuzzificados,
            dominantes
        )


        # -------------------------------------------------
        # EVALUAR REGLAS
        # -------------------------------------------------

        activaciones = evaluar_reglas(
            self.reglas,
            fuzzificados
        )


        # -------------------------------------------------
        # MOSTRAR REGLAS
        # -------------------------------------------------

        self.mostrar_reglas(
            activaciones
        )


        # -------------------------------------------------
        # AGREGACIÓN
        # -------------------------------------------------

        universo, salida_agregada = (
            agregar_salidas(
                self.reglas,
                activaciones
            )
        )


        # -------------------------------------------------
        # DEFUZZIFICACIÓN
        # -------------------------------------------------

        porcentaje = defuzzificar_centroide(
            universo,
            salida_agregada
        )


        # -------------------------------------------------
        # CLASIFICACIÓN
        # -------------------------------------------------

        clasificacion = clasificar_riesgo(
            porcentaje
        )


        # -------------------------------------------------
        # MOSTRAR RESULTADO
        # -------------------------------------------------

        self.resultado.config(
            text=(
                f"Área Estimada: "
                f"{porcentaje:.2f} Ha"
            )
        )


        self.clasificacion.config(
            text=(
                f"Clasificación: "
                f"{clasificacion}"
            )
        )


    # =====================================================
    # MOSTRAR FUZZIFICACIÓN
    # =====================================================

    def mostrar_fuzzificacion(
        self,
        fuzzificados,
        dominantes
    ):

        self.texto_fuzzy.delete(
            "1.0",
            tk.END
        )


        for variable, grados in (
            fuzzificados.items()
        ):

            self.texto_fuzzy.insert(
                tk.END,
                f"\n{variable.upper()}\n"
            )


            self.texto_fuzzy.insert(
                tk.END,
                "-" * 50 + "\n"
            )


            for conjunto, grado in (
                grados.items()
            ):

                self.texto_fuzzy.insert(
                    tk.END,
                    f"{conjunto:<15} = "
                    f"{grado:.6f}\n"
                )


            self.texto_fuzzy.insert(
                tk.END,
                f"\nDominante: "
                f"{dominantes[variable]}\n"
            )


    # =====================================================
    # MOSTRAR REGLAS
    # =====================================================

    def mostrar_reglas(
        self,
        activaciones
    ):

        self.texto_reglas.delete(
            "1.0",
            tk.END
        )


        # -------------------------------------------------
        # FILTRAR REGLAS ACTIVADAS
        # -------------------------------------------------

        activadas = [
            elemento
            for elemento in activaciones
            if elemento["activacion"] > 0
        ]


        # -------------------------------------------------
        # ORDENAR
        # -------------------------------------------------

        activadas.sort(
            key=lambda x:
                x["activacion"],
            reverse=True
        )


        self.texto_reglas.insert(
            tk.END,
            f"Reglas activadas: "
            f"{len(activadas)}\n\n"
        )


        # -------------------------------------------------
        # MOSTRAR
        # -------------------------------------------------

        for elemento in activadas:

            regla = elemento[
                "regla"
            ]


            activacion = elemento[
                "activacion"
            ]


            self.texto_reglas.insert(
                tk.END,
                f"Regla {regla['numero']}\n"
            )


            self.texto_reglas.insert(
                tk.END,
                f"{regla_a_texto(regla)}\n"
            )


            self.texto_reglas.insert(
                tk.END,
                f"Activación = "
                f"{activacion:.6f}\n"
            )


            self.texto_reglas.insert(
                tk.END,
                f"Fitness = "
                f"{regla['fitness']:.6f}\n\n"
            )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = Aplicacion(
        root
    )

    root.mainloop()