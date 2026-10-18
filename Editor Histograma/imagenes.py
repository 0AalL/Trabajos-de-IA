
import numpy as np
from PIL import Image, ImageOps


def cargar_imagen(ruta):
    """Carga la imagen y corrige la orientación EXIF."""
    with Image.open(ruta) as archivo:
        imagen = ImageOps.exif_transpose(archivo).convert("RGB")
        return imagen.copy()


def calcular_histogramas(imagen):
    """Calcula los histogramas exactos de los canales R, G y B."""
    rgb = np.asarray(imagen, dtype=np.uint8)
    histogramas = np.zeros((3, 256), dtype=np.int64)

    for canal in range(3):
        histogramas[canal] = np.bincount(
            rgb[:, :, canal].ravel(),
            minlength=256
        )

    return histogramas


def construir_transformacion(histograma_origen, histograma_objetivo):
    """
    Genera una transformación por especificación de histogramas
    mediante comparación de distribuciones acumuladas.
    """
    origen = np.maximum(
        np.asarray(histograma_origen, dtype=float), 0
    )
    objetivo = np.maximum(
        np.asarray(histograma_objetivo, dtype=float), 0
    )

    if origen.sum() == 0:
        return np.arange(256, dtype=np.uint8)

    if objetivo.sum() == 0:
        raise ValueError(
            "El histograma objetivo debe tener al menos una barra positiva."
        )

    cdf_origen = np.cumsum(origen) / origen.sum()
    cdf_objetivo = np.cumsum(objetivo) / objetivo.sum()

    # Búsqueda del nivel de salida con CDF más cercana.
    mapa = np.searchsorted(
        cdf_objetivo, cdf_origen, side="left"
    )
    mapa = np.clip(mapa, 0, 255)

    # En caso de empate se conserva la intensidad inferior, como antes.
    anterior = np.maximum(mapa - 1, 0)
    usar_anterior = (
        (mapa > 0)
        & (np.abs(cdf_objetivo[anterior] - cdf_origen)
           <= np.abs(cdf_objetivo[mapa] - cdf_origen))
    )
    mapa[usar_anterior] = anterior[usar_anterior]

    return mapa.astype(np.uint8)


def calcular_histogramas_transformados(histogramas_origen, histogramas_objetivo):
    """Calcula los histogramas de salida directamente desde los mapas."""
    origen = np.asarray(histogramas_origen)
    objetivos = np.asarray(histogramas_objetivo, dtype=float)

    if origen.shape != (3, 256) or objetivos.shape != (3, 256):
        raise ValueError("Se esperaban tres histogramas de 256 intensidades.")

    salida = np.zeros((3, 256), dtype=np.int64)

    for canal in range(3):
        mapa = construir_transformacion(origen[canal], objetivos[canal])
        salida[canal] = np.bincount(
            mapa,
            weights=origen[canal],
            minlength=256
        ).astype(np.int64)

    return salida


def transformar_rgb(
    imagen_original, histogramas_objetivo, histogramas_origen=None
):
    """
    Transforma cada canal por separado a partir de la imagen original.
    No acumula transformaciones previas.
    """
    rgb = np.asarray(imagen_original, dtype=np.uint8)
    if histogramas_origen is None:
        histogramas_origen = calcular_histogramas(imagen_original)
    else:
        histogramas_origen = np.asarray(histogramas_origen)

    objetivos = np.asarray(histogramas_objetivo, dtype=float)

    if objetivos.shape != (3, 256):
        raise ValueError(
            "Se esperaban tres histogramas de 256 intensidades."
        )

    salida = np.empty_like(rgb)

    for canal in range(3):
        mapa = construir_transformacion(
            histogramas_origen[canal],
            objetivos[canal]
        )

        salida[:, :, canal] = mapa[rgb[:, :, canal]]

    return Image.fromarray(salida)


def guardar_imagen(imagen, ruta):
    """Guarda el resultado en el formato indicado por la extensión."""
    imagen.save(ruta)
