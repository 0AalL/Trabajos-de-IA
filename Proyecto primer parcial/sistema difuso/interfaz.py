import tkinter as tk
from tkinter import ttk, messagebox

from configuracion import (
    RANGOS,
    VARIABLES_ENTRADA
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
            "1100x750"
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
        # VARIABLES DE ENTRADA
        # ---------------------------------------------

        self.entries = {}

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
            pady=15
        )


        subtitulo = ttk.Label(
            self.root,
            text="Inferencia Mamdani | AND = MIN | Agregación = MAX | Defuzzificación = CENTROIDE",
            font=("Arial", 10)
        )

        subtitulo.pack(
            pady=(0, 15)
        )


        # -------------------------------------------------
        # FRAME PRINCIPAL
        # -------------------------------------------------

        frame_entradas = ttk.LabelFrame(
            self.root,
            text="Datos de entrada",
            padding=15
        )

        frame_entradas.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # -------------------------------------------------
        # CREAR CAMPOS
        # -------------------------------------------------

        nombres = {
            "T_mean": "Temperatura (°C)",
            "RH_mean": "Humedad (%)",
            "Wind_mean": "Viento (m/s)",
            "PPT_tot": "Precipitación (mm)",
            "FFMC": "FFMC (Combustible Fino)",
            "DMC": "DMC (Capa Orgánica)",
            "DC": "DC (Sequía)",
            "KBDI": "KBDI"
        }


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
                padx=10,
                pady=5,
                sticky="w"
            )


            valor_inicial = (
                minimo + maximo
            ) / 2


            entry = ttk.Entry(
                frame_entradas,
                width=15
            )

            entry.insert(
                0,
                str(valor_inicial)
            )

            entry.grid(
                row=fila,
                column=1,
                padx=10,
                pady=5
            )


            rango = ttk.Label(
                frame_entradas,
                text=f"Rango válido: {minimo} - {maximo}"
            )

            rango.grid(
                row=fila,
                column=2,
                padx=10,
                pady=5,
                sticky="w"
            )


            self.entries[
                variable
            ] = entry


        # -------------------------------------------------
        # BOTÓN
        # -------------------------------------------------

        boton = ttk.Button(
            self.root,
            text="CALCULAR RIESGO",
            command=self.calcular
        )

        boton.pack(
            pady=15
        )


        # -------------------------------------------------
        # RESULTADO
        # -------------------------------------------------

        frame_resultado = ttk.LabelFrame(
            self.root,
            text="Resultado",
            padding=15
        )

        frame_resultado.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        self.resultado = ttk.Label(
            frame_resultado,
            text="Área Quemada: -- Ha",
            font=("Arial", 26, "bold")
        )

        self.resultado.pack(
            pady=10
        )


        self.clasificacion = ttk.Label(
            frame_resultado,
            text="Clasificación: --",
            font=("Arial", 14)
        )

        self.clasificacion.pack(
            pady=5
        )


        # -------------------------------------------------
        # NOTEBOOK
        # -------------------------------------------------

        notebook = ttk.Notebook(
            self.root
        )

        notebook.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )


        # -------------------------------------------------
        # TAB FUZZIFICACIÓN
        # -------------------------------------------------

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


        # -------------------------------------------------
        # TAB REGLAS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # TAB INFORMACIÓN
        # -------------------------------------------------

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

                if valor < minimo or valor > maximo:

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

        universo, salida_agregada = agregar_salidas(
            self.reglas,
            activaciones
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
            text=f"Área Estimada: {porcentaje:.2f} Ha"
        )

        self.clasificacion.config(
            text=f"Clasificación: {clasificacion}"
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


        for variable, grados in fuzzificados.items():

            self.texto_fuzzy.insert(
                tk.END,
                f"\n{variable.upper()}\n"
            )

            self.texto_fuzzy.insert(
                tk.END,
                "-" * 50 + "\n"
            )


            for conjunto, grado in grados.items():

                self.texto_fuzzy.insert(
                    tk.END,
                    f"{conjunto:<15} = {grado:.6f}\n"
                )


            self.texto_fuzzy.insert(
                tk.END,
                f"\nDominante: {dominantes[variable]}\n"
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


        activadas = [
            elemento
            for elemento in activaciones
            if elemento["activacion"] > 0
        ]


        # Ordenar por activación
        activadas.sort(
            key=lambda x: x["activacion"],
            reverse=True
        )


        self.texto_reglas.insert(
            tk.END,
            f"Reglas activadas: {len(activadas)}\n\n"
        )


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
                f"Activación = {activacion:.6f}\n"

            )

            self.texto_reglas.insert(
                tk.END,
                f"Fitness = {regla['fitness']:.6f}\n\n"
            )