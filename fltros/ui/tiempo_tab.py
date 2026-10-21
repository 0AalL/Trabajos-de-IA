import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import utils

# =====================================================
# CONFIG
# =====================================================
IMG_W = 120
IMG_H = 120

# =====================================================
# VARIABLES
# =====================================================
img_rgb = None

canales_ruido = {
    "r": None,
    "g": None,
    "b": None
}

canales_filtrados = {
    "r": None,
    "g": None,
    "b": None
}

labels_ruido = {}
labels_filtrado = {}
titulos = {}

# =====================================================
# MOSTRAR IMAGEN COLOR
# =====================================================
def mostrar_color_bgr(img, label):

    # BGR -> RGB
    img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(img)

    img = ImageTk.PhotoImage(img)

    label.config(image=img)

    label.image = img


# =====================================================
# MOSTRAR IMAGEN GRIS
# =====================================================
def mostrar_gris(img, label):

    rgb = utils.gris_a_rgb(img)

    rgb = cv2.resize(
        rgb,
        (IMG_W, IMG_H)
    )

    rgb = Image.fromarray(rgb)

    rgb = ImageTk.PhotoImage(rgb)

    label.config(image=rgb)

    label.image = rgb


# =====================================================
# UI PRINCIPAL
# =====================================================
def crear_tab_tiempo(frame):

    frame.rowconfigure(1, weight=1)

    frame.columnconfigure(0, weight=1)

    # =====================================================
    # RECONSTRUIR RGB
    # =====================================================
    def reconstruir():

        for canal in ["r", "g", "b"]:

            if canales_filtrados[canal] is None:
                return

        img = cv2.merge([
            canales_filtrados["b"],
            canales_filtrados["g"],
            canales_filtrados["r"]
        ])

        mostrar_color_bgr(
            img,
            lbl_reconstruida
        )

    # =====================================================
    # CARGAR IMAGEN
    # =====================================================
    def cargar():

        global img_rgb

        ruta = filedialog.askopenfilename(
            filetypes=[
                (
                    "Imágenes",
                    "*.png *.jpg *.jpeg *.bmp"
                )
            ]
        )

        if not ruta:
            return

        # =========================================
        # CARGAR
        # =========================================
        img_rgb = utils.cargar_imagen(
            ruta,
            gris=False
        )

        # =========================================
        # SEPARAR RGB
        # =========================================
        r, g, b = utils.separar_canales(
            img_rgb
        )

        originales = {
            "r": r,
            "g": g,
            "b": b
        }

        # =========================================
        # AGREGAR RUIDO
        # =========================================
        for canal in ["r", "g", "b"]:

            ruido = utils.agregar_ruido_sal_pimienta(
                originales[canal]
            )

            canales_ruido[canal] = ruido

        # =========================================
        # MOSTRAR ORIGINAL
        # =========================================
        mostrar_color_bgr(
            img_rgb,
            lbl_original
        )

        # =========================================
        # RGB CON RUIDO
        # =========================================
        ruido_rgb = cv2.merge([
            canales_ruido["b"],
            canales_ruido["g"],
            canales_ruido["r"]
        ])

        mostrar_color_bgr(
            ruido_rgb,
            lbl_ruido_rgb
        )

        # =========================================
        # MOSTRAR CANALES
        # =========================================
        for canal in ["r", "g", "b"]:

            # Mostrar ruido
            mostrar_gris(
                canales_ruido[canal],
                labels_ruido[canal]
            )

            # Filtro inicial
            filtrada = utils.filtro_mediana(
                canales_ruido[canal]
            )

            canales_filtrados[canal] = filtrada

            # Mostrar filtrada
            mostrar_gris(
                filtrada,
                labels_filtrado[canal]
            )

            titulos[canal].config(
                text=f"Canal {canal.upper()} (Mediana)"
            )

        # =========================================
        # RECONSTRUIR
        # =========================================
        reconstruir()

    # =====================================================
    # APLICAR FILTRO
    # =====================================================
    def aplicar(canal, tipo):

        img = canales_ruido[canal]

        if img is None:
            return

        filtros = {
            "media": utils.filtro_media,
            "moda": utils.filtro_moda,
            "mediana": utils.filtro_mediana
        }

        nombres = {
            "media": "Media",
            "moda": "Moda",
            "mediana": "Mediana"
        }

        # =========================================
        # FILTRAR
        # =========================================
        filtrada = filtros[tipo](img)

        canales_filtrados[canal] = filtrada

        # =========================================
        # MOSTRAR FILTRADA
        # =========================================
        mostrar_gris(
            filtrada,
            labels_filtrado[canal]
        )

        # =========================================
        # ACTUALIZAR TITULO
        # =========================================
        titulos[canal].config(
            text=f"Canal {canal.upper()} ({nombres[tipo]})"
        )

        # =========================================
        # RECONSTRUIR
        # =========================================
        reconstruir()

    # =====================================================
    # BOTON CARGAR
    # =====================================================
    tk.Button(
        frame,
        text="📂 Cargar Imagen",
        font=("Arial", 11, "bold"),
        bg="#3498db",
        fg="white",
        command=cargar
    ).grid(
        row=0,
        column=0,
        sticky="ew",
        padx=10,
        pady=10
    )

    # =====================================================
    # CONTENEDOR PRINCIPAL
    # =====================================================
    main = tk.Frame(
        frame,
        bg="#f4f4f4"
    )

    main.grid(
        row=1,
        column=0,
        sticky="nsew"
    )

    main.columnconfigure(0, weight=3)
    main.columnconfigure(1, weight=2)

    main.rowconfigure(0, weight=1)

    # =====================================================
    # PANEL IZQUIERDO
    # =====================================================
    left = tk.Frame(
        main,
        bg="#f4f4f4"
    )

    left.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=10,
        pady=10
    )

    for i in range(12):
        left.rowconfigure(i, weight=1)

    for j in range(3):
        left.columnconfigure(j, weight=1)

    # =====================================================
    # TITULOS SUPERIORES
    # =====================================================
    tk.Label(
        left,
        text="Original",
        font=("Arial", 12, "bold"),
        bg="#f4f4f4"
    ).grid(row=0, column=0)

    tk.Label(
        left,
        text="RGB con Ruido",
        font=("Arial", 12, "bold"),
        bg="#f4f4f4"
    ).grid(row=0, column=1)

    # =====================================================
    # IMAGENES SUPERIORES
    # =====================================================
    lbl_original = tk.Label(
        left,
        bd=2,
        relief="solid",
        bg="white"
    )

    lbl_original.grid(
        row=1,
        column=0,
        padx=5,
        pady=5
    )

    lbl_ruido_rgb = tk.Label(
        left,
        bd=2,
        relief="solid",
        bg="white"
    )

    lbl_ruido_rgb.grid(
        row=1,
        column=1,
        padx=5,
        pady=5
    )

    # =====================================================
    # ENCABEZADOS
    # =====================================================
    headers = [
        "Ruido",
        "Filtrado",
        "Acciones"
    ]

    for i, h in enumerate(headers):

        tk.Label(
            left,
            text=h,
            font=("Arial", 11, "bold"),
            bg="#f4f4f4"
        ).grid(
            row=2,
            column=i
        )

    # =====================================================
    # CANALES RGB
    # =====================================================
    canales = ["r", "g", "b"]

    fila = 3

    for canal in canales:

        # =========================================
        # TITULO
        # =========================================
        titulo = tk.Label(
            left,
            text=f"Canal {canal.upper()}",
            font=("Arial", 11, "bold"),
            bg="#f4f4f4"
        )

        titulo.grid(
            row=fila,
            column=0,
            columnspan=3,
            pady=(10, 0)
        )

        titulos[canal] = titulo

        # =========================================
        # LABEL RUIDO
        # =========================================
        lbl_ruido = tk.Label(
            left,
            bd=2,
            relief="solid",
            bg="white"
        )

        lbl_ruido.grid(
            row=fila + 1,
            column=0,
            padx=5,
            pady=5
        )

        # =========================================
        # LABEL FILTRADO
        # =========================================
        lbl_filtrado = tk.Label(
            left,
            bd=2,
            relief="solid",
            bg="white"
        )

        lbl_filtrado.grid(
            row=fila + 1,
            column=1,
            padx=5,
            pady=5
        )

        labels_ruido[canal] = lbl_ruido
        labels_filtrado[canal] = lbl_filtrado

        # =========================================
        # BOTONES
        # =========================================
        frame_btn = tk.Frame(
            left,
            bg="#f4f4f4"
        )

        frame_btn.grid(
            row=fila + 1,
            column=2
        )

        for tipo in [
            "media",
            "moda",
            "mediana"
        ]:

            tk.Button(
                frame_btn,
                text=tipo.capitalize(),
                width=12,
                command=lambda c=canal, t=tipo:
                aplicar(c, t)
            ).pack(
                pady=2
            )

        fila += 2

    # =====================================================
    # PANEL DERECHO
    # =====================================================
    right = tk.Frame(
        main,
        bg="#dfe6e9",
        bd=3,
        relief="ridge"
    )

    right.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=10,
        pady=10
    )

    right.rowconfigure(1, weight=1)

    right.columnconfigure(0, weight=1)

    # =====================================================
    # TITULO FINAL
    # =====================================================
    tk.Label(
        right,
        text="RGB Reconstruido",
        font=("Arial", 16, "bold"),
        bg="#dfe6e9"
    ).grid(
        row=0,
        column=0,
        pady=10
    )

    # =====================================================
    # IMAGEN FINAL
    # =====================================================
    lbl_reconstruida = tk.Label(
        right,
        bd=4,
        relief="solid",
        bg="white"
    )

    lbl_reconstruida.grid(
        row=1,
        column=0,
        padx=15,
        pady=15
    )