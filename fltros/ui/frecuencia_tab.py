import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk

import utils


PREVIEW_SIZE = (220, 220)
SPECTRUM_PREVIEW_SIZE = (155, 155)


def ifft2(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    return np.fft.ifft2(f_ishift).real


def mascara(shape, radio, tipo):
    filas, columnas = shape
    centro = (columnas // 2, filas // 2)
    pasabajos = np.zeros((filas, columnas), np.uint8)
    cv2.circle(pasabajos, centro, radio, 1, -1)

    if tipo == "pasabajos":
        return pasabajos
    if tipo == "pasaltos":
        return 1 - pasabajos

    raise ValueError(f"Tipo de filtro no válido: {tipo}")


def espectros_magnitud_canales(fourier_canales):
    return [
        cv2.normalize(
            20 * np.log(np.abs(canal) + 1),
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)
        for canal in fourier_canales
    ]


def transformar_canales_frecuencia(img):
    return [
        np.fft.fftshift(np.fft.fft2(canal))
        for canal in cv2.split(img)
    ]


def filtrar_rgb_frecuencia(img, radio, tipo):
    fourier_entrada = transformar_canales_frecuencia(img)
    mask = mascara(img.shape[:2], radio, tipo)
    fourier_filtrada = [
        canal * mask
        for canal in fourier_entrada
    ]

    canales_resultado = []
    for canal in fourier_filtrada:
        respuesta = ifft2(canal)
        if tipo == "pasaltos":
            respuesta = cv2.normalize(
                np.abs(respuesta),
                None,
                0,
                255,
                cv2.NORM_MINMAX
            )
        else:
            respuesta = np.clip(respuesta, 0, 255)

        canales_resultado.append(respuesta.astype(np.uint8))

    resultado_rgb = cv2.merge(canales_resultado)
    espectro_entrada = espectros_magnitud_canales(fourier_entrada)
    espectro_filtrado = espectros_magnitud_canales(fourier_filtrada)
    return resultado_rgb, espectro_entrada, espectro_filtrado


def mostrar_color_bgr(img, label):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imagen = Image.fromarray(img_rgb)
    imagen.thumbnail(PREVIEW_SIZE)
    imagen_tk = ImageTk.PhotoImage(imagen)

    label.config(image=imagen_tk, text="")
    label.image = imagen_tk


def mostrar_espectro(img, label):
    imagen = Image.fromarray(img)
    imagen.thumbnail(SPECTRUM_PREVIEW_SIZE)
    imagen_tk = ImageTk.PhotoImage(imagen)

    label.config(image=imagen_tk, text="")
    label.image = imagen_tk


def crear_tab_frecuencia(frame):
    img_rgb = None
    img_ruidosa = None
    nivel_ruido = tk.IntVar(value=5)
    radio = tk.StringVar(value="30")

    def actualizar_ruido():
        nonlocal img_ruidosa

        if img_rgb is None:
            return

        img_ruidosa = utils.agregar_ruido_sal_pimienta(
            img_rgb,
            prob=nivel_ruido.get() / 100
        )
        mostrar_color_bgr(img_ruidosa, lbl_ruido)
        espectros_entrada = espectros_magnitud_canales(
            transformar_canales_frecuencia(img_ruidosa)
        )
        for canal, espectro in zip(("B", "G", "R"), espectros_entrada):
            mostrar_espectro(espectro, lbl_espectro_entrada[canal])
        for etiqueta in lbl_espectro_filtrado.values():
            etiqueta.config(image="", text="Aplica un filtro")
            etiqueta.image = None
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

        try:
            radio_filtro = int(radio.get())
        except ValueError:
            messagebox.showerror(
                "Radio no válido",
                "Ingresa un radio entero mayor o igual a 0."
            )
            return

        if radio_filtro < 0:
            messagebox.showerror(
                "Radio no válido",
                "El radio debe ser mayor o igual a 0."
            )
            return

        resultado_rgb, espectro_entrada, espectro_filtrado = (
            filtrar_rgb_frecuencia(
                img_ruidosa,
                radio_filtro,
                tipo
            )
        )
        for canal, espectro in zip(("B", "G", "R"), espectro_entrada):
            mostrar_espectro(espectro, lbl_espectro_entrada[canal])
        for canal, espectro in zip(("B", "G", "R"), espectro_filtrado):
            mostrar_espectro(espectro, lbl_espectro_filtrado[canal])
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
        length=150,
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

    tk.Label(
        controles,
        text="Radio:",
        bg="#f4f4f4"
    ).pack(side="left", padx=(15, 5))

    tk.Entry(
        controles,
        textvariable=radio,
        width=6,
        justify="center"
    ).pack(side="left")

    tk.Button(
        controles,
        text="Pasabajos",
        command=lambda: aplicar("pasabajos")
    ).pack(side="left", padx=(8, 2))

    tk.Button(
        controles,
        text="Pasaltos",
        command=lambda: aplicar("pasaltos")
    ).pack(side="left", padx=2)

    principal = tk.Frame(frame, bg="#f4f4f4")
    principal.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=10,
        pady=10
    )

    for columna in range(5):
        principal.columnconfigure(columna, weight=1)

    vistas = [
        ("RGB Original", "color"),
        ("RGB con Ruido", "color"),
        ("Espectro de entrada", "espectro_entrada"),
        ("Espectro filtrado", "espectro_filtrado"),
        ("Resultado RGB", "color")
    ]
    etiquetas = []
    lbl_espectro_entrada = {}
    lbl_espectro_filtrado = {}

    for columna, (titulo, tipo_vista) in enumerate(vistas):
        panel = tk.LabelFrame(
            principal,
            text=titulo,
            font=("Arial", 10, "bold"),
            bg="#f4f4f4",
            padx=4,
            pady=4
        )
        panel.grid(
            row=0,
            column=columna,
            padx=3,
            pady=5,
            sticky="n"
        )

        if tipo_vista.startswith("espectro"):
            etiquetas_canal = (
                lbl_espectro_entrada
                if tipo_vista == "espectro_entrada"
                else lbl_espectro_filtrado
            )
            for canal in ("B", "G", "R"):
                panel_canal = tk.LabelFrame(
                    panel,
                    text=f"Canal {canal}",
                    bg="#f4f4f4",
                    padx=2,
                    pady=2
                )
                panel_canal.pack(pady=2)
                etiqueta = tk.Label(
                    panel_canal,
                    bd=2,
                    relief="solid",
                    bg="white",
                    text=(
                        "Carga una imagen"
                        if tipo_vista == "espectro_entrada"
                        else "Aplica un filtro"
                    ),
                    compound=tk.CENTER
                )
                etiqueta.pack()
                etiquetas_canal[canal] = etiqueta
            continue

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
