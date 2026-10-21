import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import utils

# ==========================================
# TAMAÑO
# ==========================================
IMG_W = 95
IMG_H = 95

img_rgb = None

r = g = b = None
r_f = g_f = b_f = None


# ==========================================
# FFT
# ==========================================
def fft2(img):

    f = np.fft.fft2(img)

    return np.fft.fftshift(f)


def ifft2(fshift):

    f_ishift = np.fft.ifftshift(fshift)

    img = np.fft.ifft2(f_ishift)

    img = np.abs(img)

    return np.uint8(np.clip(img, 0, 255))


def espectro_desde_fft(fshift):

    mag = 20 * np.log(np.abs(fshift) + 1)

    mag = np.uint8(255 * mag / np.max(mag))

    return mag


def espectro(img):

    fshift = fft2(img)

    mag = espectro_desde_fft(fshift)

    return mag, fshift


def mascara(shape, radio):

    rows, cols = shape

    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols), np.uint8)

    cv2.circle(mask, (ccol, crow), radio, 1, -1)

    return mask


def filtrar(fshift, radio):

    mask = mascara(fshift.shape, radio)

    return fshift * mask


# ==========================================
# MOSTRAR
# ==========================================
def mostrar_color(img, label, size=(IMG_W, IMG_H)):

    img = cv2.resize(img, size)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(img)

    img = ImageTk.PhotoImage(img)

    label.config(image=img)

    label.image = img


def mostrar_gris(img, label, size=(IMG_W, IMG_H)):

    img = cv2.resize(img, size)

    img = Image.fromarray(img)

    img = ImageTk.PhotoImage(img)

    label.config(image=img)

    label.image = img


# ==========================================
# TAB
# ==========================================
def crear_tab_frecuencia(frame):

    global img_rgb, r, g, b
    global r_f, g_f, b_f

    entry = {}

    # ======================================
    # RECONSTRUIR
    # ======================================
    def reconstruir():

        if r_f is None or g_f is None or b_f is None:
            return

        img = cv2.merge([b_f, g_f, r_f])

        mostrar_color(
            img,
            lbl_final,
            size=(260, 260)
        )

    # ======================================
    # APLICAR
    # ======================================
    def aplicar(canal):

        global r_f, g_f, b_f

        try:
            radio = int(entry[canal].get())
        except:
            return

        if canal == "r":

            _, f = espectro(r)

            f_filtrado = filtrar(f, radio)

            r_f = ifft2(f_filtrado)

            fft_filtrada = espectro_desde_fft(f_filtrado)

            mostrar_gris(r_f, lbl_r_filtrada)

            mostrar_gris(
                fft_filtrada,
                lbl_r_fft_filtrada
            )

        elif canal == "g":

            _, f = espectro(g)

            f_filtrado = filtrar(f, radio)

            g_f = ifft2(f_filtrado)

            fft_filtrada = espectro_desde_fft(f_filtrado)

            mostrar_gris(g_f, lbl_g_filtrada)

            mostrar_gris(
                fft_filtrada,
                lbl_g_fft_filtrada
            )

        else:

            _, f = espectro(b)

            f_filtrado = filtrar(f, radio)

            b_f = ifft2(f_filtrado)

            fft_filtrada = espectro_desde_fft(f_filtrado)

            mostrar_gris(b_f, lbl_b_filtrada)

            mostrar_gris(
                fft_filtrada,
                lbl_b_fft_filtrada
            )

        reconstruir()

    # ======================================
    # MOSTRAR
    # ======================================
    def mostrar():

        global r_f, g_f, b_f

        mag_r, _ = espectro(r)
        mag_g, _ = espectro(g)
        mag_b, _ = espectro(b)

        # ORIGINALES
        mostrar_gris(r, lbl_r)
        mostrar_gris(g, lbl_g)
        mostrar_gris(b, lbl_b)

        # FFT
        mostrar_gris(mag_r, lbl_r_fft)
        mostrar_gris(mag_g, lbl_g_fft)
        mostrar_gris(mag_b, lbl_b_fft)

        # FILTRADAS
        r_f = r.copy()
        g_f = g.copy()
        b_f = b.copy()

        mostrar_gris(r_f, lbl_r_filtrada)
        mostrar_gris(g_f, lbl_g_filtrada)
        mostrar_gris(b_f, lbl_b_filtrada)

        # FFT FILTRADAS
        mostrar_gris(mag_r, lbl_r_fft_filtrada)
        mostrar_gris(mag_g, lbl_g_fft_filtrada)
        mostrar_gris(mag_b, lbl_b_fft_filtrada)

        # ENTRIES
        for c in ["r", "g", "b"]:

            entry[c].delete(0, tk.END)

            entry[c].insert(0, "0")

        reconstruir()

    # ======================================
    # CARGAR
    # ======================================
    def cargar():

        global img_rgb, r, g, b

        path = filedialog.askopenfilename()

        if not path:
            return

        img_rgb = utils.cargar_imagen(
            path,
            gris=False
        )

        img_ruidosa = utils.agregar_ruido_sal_pimienta(
            img_rgb,
            prob=0.05
        )

        r, g, b = utils.separar_canales(img_ruidosa)

        mostrar()

    # ======================================
    # BOTON
    # ======================================
    tk.Button(
        frame,
        text="Cargar Imagen",
        font=("Arial", 11, "bold"),
        command=cargar
    ).pack(pady=8)

    # ======================================
    # CONTENEDOR GENERAL
    # ======================================
    contenedor_general = tk.Frame(frame)

    contenedor_general.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ======================================
    # IZQUIERDA -> CANALES
    # ======================================
    principal = tk.Frame(contenedor_general)

    principal.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ======================================
    # DERECHA -> IMAGEN FINAL
    # ======================================
    final_frame = tk.LabelFrame(
        contenedor_general,
        text="Imagen Reconstruida",
        padx=10,
        pady=10,
        font=("Arial", 11, "bold")
    )

    final_frame.pack(
        side="left",
        padx=10,
        anchor="n"
    )

    lbl_final = tk.Label(
        final_frame,
        bd=2,
        relief="solid"
    )

    lbl_final.pack()

    # ======================================
    # PANEL CANAL
    # ======================================
    def crear_panel(parent, titulo, canal):

        panel = tk.LabelFrame(
            parent,
            text=titulo,
            padx=5,
            pady=5,
            font=("Arial", 10, "bold")
        )

        panel.pack(
            fill="x",
            pady=5
        )

        # ==================================
        # CONTENEDOR HORIZONTAL
        # ==================================
        fila = tk.Frame(panel)

        fila.pack()

        # ==================================
        # ORIGINAL
        # ==================================
        c1 = tk.Frame(fila)

        c1.pack(side="left", padx=5)

        tk.Label(
            c1,
            text="Original"
        ).pack()

        lbl_original = tk.Label(
            c1,
            bd=2,
            relief="solid"
        )

        lbl_original.pack()

        # ==================================
        # FFT
        # ==================================
        c2 = tk.Frame(fila)

        c2.pack(side="left", padx=5)

        tk.Label(
            c2,
            text="FFT"
        ).pack()

        lbl_fft = tk.Label(
            c2,
            bd=2,
            relief="solid"
        )

        lbl_fft.pack()

        # ==================================
        # FILTRADA
        # ==================================
        c3 = tk.Frame(fila)

        c3.pack(side="left", padx=5)

        tk.Label(
            c3,
            text="Filtrada"
        ).pack()

        lbl_filtrada = tk.Label(
            c3,
            bd=2,
            relief="solid"
        )

        lbl_filtrada.pack()

        # ==================================
        # FFT FILTRADA
        # ==================================
        c4 = tk.Frame(fila)

        c4.pack(side="left", padx=5)

        tk.Label(
            c4,
            text="FFT Filtrada"
        ).pack()

        lbl_fft_filtrada = tk.Label(
            c4,
            bd=2,
            relief="solid"
        )

        lbl_fft_filtrada.pack()

        # ==================================
        # CONTROLES
        # ==================================
        control = tk.Frame(panel)

        control.pack(pady=5)

        tk.Label(
            control,
            text="Radio:"
        ).pack(side="left")

        entry[canal] = tk.Entry(
            control,
            width=5,
            justify="center"
        )

        entry[canal].pack(
            side="left",
            padx=5
        )

        tk.Button(
            control,
            text="Aplicar",
            command=lambda: aplicar(canal)
        ).pack(side="left")

        return (
            lbl_original,
            lbl_fft,
            lbl_filtrada,
            lbl_fft_filtrada
        )

    # ======================================
    # CANALES
    # ======================================
    (
        lbl_r,
        lbl_r_fft,
        lbl_r_filtrada,
        lbl_r_fft_filtrada
    ) = crear_panel(
        principal,
        "Canal R",
        "r"
    )

    (
        lbl_g,
        lbl_g_fft,
        lbl_g_filtrada,
        lbl_g_fft_filtrada
    ) = crear_panel(
        principal,
        "Canal G",
        "g"
    )

    (
        lbl_b,
        lbl_b_fft,
        lbl_b_filtrada,
        lbl_b_fft_filtrada
    ) = crear_panel(
        principal,
        "Canal B",
        "b"
    )