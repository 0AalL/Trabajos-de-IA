import numpy as np
import cv2
from skimage.util import random_noise

# =========================
# CARGAR Y GUARDAR IMAGEN
# =========================
def cargar_imagen(ruta, gris=True):
    if gris:
        img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(ruta)

    if img is None:
        raise ValueError("No se pudo cargar la imagen")

    return img


def guardar_imagen(ruta, img):
    cv2.imwrite(ruta, img)


# =========================
# RUIDO SAL Y PIMIENTA (rápido)
# =========================

def agregar_ruido_sal_pimienta(img, prob=0.05):
    noisy = random_noise(img, mode='s&p', amount=prob)
    noisy = (noisy * 255).astype('uint8')
    return noisy

# =========================
# FILTRO MEDIANA
# =========================
def filtro_mediana(img):
    padded = agregar_borde_negro(img)
    salida = np.zeros_like(img)

    for i in range(1, padded.shape[0] - 1):
        for j in range(1, padded.shape[1] - 1):
            ventana = padded[i-1:i+2, j-1:j+2].flatten()
            salida[i-1, j-1] = np.median(ventana)

    return salida

# =========================
# FILTRO MEDIA (PROMEDIO)
# =========================
def filtro_media(img, kernel_size=3):
    pad = kernel_size // 2
    padded = np.pad(img, pad, mode='constant', constant_values=0)
    salida = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            ventana = padded[i:i+kernel_size, j:j+kernel_size]
            salida[i, j] = np.mean(ventana)

    return salida


# =========================
# FILTRO MODA
# =========================
def filtro_moda(img, kernel_size=3):
    pad = kernel_size // 2
    padded = np.pad(img, pad, mode='constant', constant_values=0)
    salida = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            ventana = padded[i:i+kernel_size, j:j+kernel_size].flatten()

            valores, conteo = np.unique(ventana, return_counts=True)
            salida[i, j] = valores[np.argmax(conteo)]

    return salida


# =========================
# FFT (DOMINIO FRECUENCIA)
# =========================
def transformar_fft(img):
    f = np.fft.fft2(img)
    f_shift = np.fft.fftshift(f)
    return f_shift


def inversa_fft(f_shift):
    f_ishift = np.fft.ifftshift(f_shift)
    img_back = np.fft.ifft2(f_ishift)
    return np.abs(img_back)


# =========================
# FILTRO CIRCULAR EN FRECUENCIA
# =========================
def filtro_circular_frecuencia(f_shift, radio):
    filas, cols = f_shift.shape
    centro_fila, centro_col = filas // 2, cols // 2

    mask = np.zeros((filas, cols))

    for i in range(filas):
        for j in range(cols):
            distancia = np.sqrt((i - centro_fila)**2 + (j - centro_col)**2)
            if distancia <= radio:
                mask[i, j] = 1

    return f_shift * mask


# =========================
# CONVERSIONES
# =========================
def convertir_a_gris(img_rgb):
    return cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


def gris_a_rgb(img_gray):
    return cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)


# =========================
# NORMALIZACION HISTOGRAMA (manual)
# =========================
def normalizar_histograma(img):
    img = img.astype(np.float32)

    min_val = np.min(img)
    max_val = np.max(img)

    if max_val - min_val == 0:
        return img

    norm = (img - min_val) / (max_val - min_val)
    norm = norm * 255

    return norm.astype(np.uint8)


# =========================
# BINARIZACION
# =========================
def binarizar(img, umbral=128):
    binaria = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] > umbral:
                binaria[i, j] = 255
            else:
                binaria[i, j] = 0

    return binaria

# =========================
# PADDING BORDE NEGRO (1 pixel)
# =========================
def agregar_borde_negro(img):
    filas, cols = img.shape
    nueva = np.zeros((filas + 2, cols + 2), dtype=img.dtype)

    # copiar imagen original al centro
    nueva[1:filas+1, 1:cols+1] = img

    return nueva


def separar_canales(img_rgb):
    b, g, r = cv2.split(img_rgb)
    return r, g, b

def unir_canales(r, g, b):
    return cv2.merge((b, g, r))