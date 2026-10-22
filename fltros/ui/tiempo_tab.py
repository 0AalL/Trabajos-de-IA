import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk

import utils


PREVIEW_SIZE = (400, 400)


def mostrar_color_bgr(img, label):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imagen = Image.fromarray(img_rgb)
    imagen.thumbnail(PREVIEW_SIZE)
    imagen_tk = ImageTk.PhotoImage(imagen)

    label.config(image=imagen_tk, text="")
    label.image = imagen_tk


def filtrar_rgb(img, tipo):
    filtros = {
        "media": utils.filtro_media,
        "moda": utils.filtro_moda,
        "mediana": utils.filtro_mediana
    }
    canales_filtrados = [
        filtros[tipo](canal)
        for canal in cv2.split(img)
    ]
    return cv2.merge(canales_filtrados)


def crear_tab_tiempo(frame):
    img_rgb = None
    img_ruidosa = None
    nivel_ruido = tk.IntVar(value=5)

    def actualizar_ruido():
        nonlocal img_ruidosa

        if img_rgb is None:
            return

        img_ruidosa = utils.agregar_ruido_sal_pimienta(
            img_rgb,
            prob=nivel_ruido.get() / 100
        )
        mostrar_color_bgr(img_ruidosa, lbl_ruido)
        lbl_resultado.config(image="", text="Aplica un filtro")
        lbl_resultado.image = None

    def cargar():
        nonlocal img_rgb

        ruta = filedialog.askopenfilename(
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp")
            ]
        )

        if not ruta:
            return

        img_rgb = utils.cargar_imagen(ruta, gris=False)
        mostrar_color_bgr(img_rgb, lbl_original)
        actualizar_ruido()

    def aplicar(tipo):
        if img_ruidosa is None:
            return

        resultado_rgb = filtrar_rgb(img_ruidosa, tipo)
        mostrar_color_bgr(resultado_rgb, lbl_resultado)

    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    controles = tk.Frame(frame, bg="#f4f4f4")
    controles.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=10,
        pady=10
    )

    tk.Button(
        controles,
        text="📂 Cargar Imagen",
        font=("Arial", 11, "bold"),
        bg="#3498db",
        fg="white",
        command=cargar
    ).pack(side="left")

    tk.Label(
        controles,
        text="Nivel de ruido:",
        bg="#f4f4f4"
    ).pack(side="left", padx=(15, 5))

    tk.Scale(
        controles,
        from_=0,
        to=100,
        resolution=1,
        orient=tk.HORIZONTAL,
        variable=nivel_ruido,
        length=180,
        showvalue=True,
        bg="#f4f4f4"
    ).pack(side="left")

    tk.Label(
        controles,
        text="%",
        bg="#f4f4f4"
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        controles,
        text="Aplicar nivel",
        command=actualizar_ruido
    ).pack(side="left")

    principal = tk.Frame(frame, bg="#f4f4f4")
    principal.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=10,
        pady=10
    )

    for columna in range(3):
        principal.columnconfigure(columna, weight=1)

    vistas = [
        ("RGB Original", 0),
        ("RGB con Ruido", 1),
        ("Resultado RGB", 2)
    ]
    etiquetas = []

    for titulo, columna in vistas:
        panel = tk.LabelFrame(
            principal,
            text=titulo,
            font=("Arial", 12, "bold"),
            bg="#f4f4f4",
            padx=5,
            pady=5
        )
        panel.grid(
            row=0,
            column=columna,
            padx=5,
            pady=5,
            sticky="n"
        )

        etiqueta = tk.Label(
            panel,
            bd=2,
            relief="solid",
            bg="white",
            text="Carga una imagen",
            compound=tk.CENTER
        )
        etiqueta.pack()
        etiquetas.append(etiqueta)

    lbl_original, lbl_ruido, lbl_resultado = etiquetas

    acciones = tk.Frame(principal, bg="#f4f4f4")
    acciones.grid(
        row=1,
        column=0,
        columnspan=3,
        pady=10
    )

    for tipo in ("media", "moda", "mediana"):
        tk.Button(
            acciones,
            text=f"Filtro {tipo.capitalize()}",
            width=16,
            command=lambda t=tipo: aplicar(t)
        ).pack(side="left", padx=5)
