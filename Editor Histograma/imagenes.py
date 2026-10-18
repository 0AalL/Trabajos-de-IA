
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


def _repartir_en_menos_poblados(cuentas, candidatos, cantidad, limite):
    reparticion = np.zeros(256, dtype=np.int64)
    restante = int(cantidad)

    while restante > 0:
        disponibles = candidatos[cuentas[candidatos] < limite]
        if len(disponibles) == 0:
            raise ValueError(
                "No hay intensidades disponibles para recibir esos píxeles."
            )

        minimo = int(cuentas[disponibles].min())
        grupo = disponibles[cuentas[disponibles] == minimo]
        superiores = cuentas[disponibles][cuentas[disponibles] > minimo]
        siguiente = min(int(superiores.min()), limite) if len(superiores) else limite
        capacidad = (siguiente - minimo) * len(grupo)

        if restante >= capacidad:
            cuentas[grupo] += siguiente - minimo
            reparticion[grupo] += siguiente - minimo
            restante -= capacidad
        else:
            incremento, sobrante = divmod(restante, len(grupo))
            cuentas[grupo] += incremento
            reparticion[grupo] += incremento
            if sobrante:
                cuentas[grupo[:sobrante]] += 1
                reparticion[grupo[:sobrante]] += 1
            restante = 0

    return reparticion


def _construir_redistribucion(histograma_origen, histograma_objetivo):
    origen = np.maximum(
        np.asarray(histograma_origen, dtype=np.int64), 0
    )
    objetivo = np.asarray(histograma_objetivo, dtype=float)

    if origen.shape != (256,) or objetivo.shape != (256,):
        raise ValueError("Se esperaba un histograma de 256 intensidades.")

    total = int(origen.sum())
    if total == 0:
        return origen.copy(), []

    objetivo = np.nan_to_num(
        objetivo, nan=0.0, posinf=float(total), neginf=0.0
    )
    objetivo = np.clip(objetivo, 0, total)
    solicitado = np.rint(objetivo).astype(np.int64)
    modificadas = solicitado != origen
    libres = np.flatnonzero(~modificadas)
    subidas = np.flatnonzero(solicitado > origen)
    bajadas = np.flatnonzero(solicitado < origen)

    if not len(subidas) and not len(bajadas):
        return origen.copy(), []

    finales = origen.copy()
    finales[modificadas] = solicitado[modificadas]
    movimientos = []
    donantes = libres[np.argsort(-origen[libres], kind="stable")]
    demanda_subidas = {
        int(destino): int(solicitado[destino] - origen[destino])
        for destino in subidas
    }

    for destino in subidas:
        restante = demanda_subidas[int(destino)]
        for fuente in donantes:
            cantidad = min(restante, int(finales[fuente]))
            if cantidad:
                finales[fuente] -= cantidad
                movimientos.append((int(fuente), int(destino), cantidad))
                restante -= cantidad
            if restante == 0:
                break
        demanda_subidas[int(destino)] = restante

    for fuente in bajadas:
        cantidad = int(origen[fuente] - solicitado[fuente])
        restante = cantidad

        for destino in subidas:
            demanda = demanda_subidas[int(destino)]
            trasladar = min(restante, demanda)
            if trasladar:
                movimientos.append((int(fuente), int(destino), trasladar))
                demanda_subidas[int(destino)] -= trasladar
                restante -= trasladar
            if restante == 0:
                break

        if restante:
            reparticion = _repartir_en_menos_poblados(
                finales, libres, restante, total
            )
            for destino in np.flatnonzero(reparticion):
                movimientos.append((int(fuente), int(destino), int(reparticion[destino])))

    if any(demanda_subidas.values()):
        raise ValueError(
            "No hay suficientes píxeles para aumentar las barras seleccionadas."
        )

    return finales, movimientos


def _aplicar_movimientos(canal, movimientos):
    plano = np.asarray(canal, dtype=np.uint8).ravel()
    salida = plano.copy()

    if not movimientos:
        return salida.reshape(canal.shape)

    por_fuente = {}
    for fuente, destino, cantidad in movimientos:
        por_fuente.setdefault(fuente, []).append((destino, cantidad))

    if len(por_fuente) <= 8:
        for fuente, destinos in por_fuente.items():
            posiciones = np.flatnonzero(plano == fuente)
            inicio = 0
            for destino, cantidad in destinos:
                fin = inicio + cantidad
                salida[posiciones[inicio:fin]] = destino
                inicio = fin
    else:
        cuentas = np.bincount(plano, minlength=256)
        orden = np.argsort(plano, kind="stable")
        inicios = np.concatenate(([0], np.cumsum(cuentas[:-1])))
        usados = np.zeros(256, dtype=np.int64)

        for fuente, destino, cantidad in movimientos:
            inicio = int(inicios[fuente] + usados[fuente])
            fin = inicio + cantidad
            salida[orden[inicio:fin]] = destino
            usados[fuente] += cantidad

    return salida.reshape(canal.shape)


def calcular_histogramas_transformados(histogramas_origen, histogramas_objetivo):
    """Calcula los conteos resultantes respetando las barras editadas."""
    origen = np.asarray(histogramas_origen)
    objetivos = np.asarray(histogramas_objetivo, dtype=float)

    if origen.shape != (3, 256) or objetivos.shape != (3, 256):
        raise ValueError("Se esperaban tres histogramas de 256 intensidades.")

    salida = np.zeros((3, 256), dtype=np.int64)

    for canal in range(3):
        salida[canal], _ = _construir_redistribucion(
            origen[canal], objetivos[canal]
        )

    return salida


def transformar_canal(
    canal_original, histograma_objetivo, histograma_origen, contraste=1.0
):
    """Transforma un solo canal para evitar recorrer los demás."""
    canal = np.asarray(canal_original, dtype=np.uint8)
    origen = np.asarray(histograma_origen, dtype=np.int64)
    objetivo = np.asarray(histograma_objetivo, dtype=float)

    _, movimientos = _construir_redistribucion(origen, objetivo)
    valores = _aplicar_movimientos(canal, movimientos).astype(float)
    factor = float(np.clip(np.nan_to_num(contraste, nan=1.0), 1.0, 3.0))
    valores = (valores - 127.5) * factor + 127.5

    return np.clip(np.rint(valores), 0, 255).astype(np.uint8)


def transformar_rgb(
    imagen_original,
    histogramas_objetivo,
    histogramas_origen=None,
    contrastes=None
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

    if contrastes is None:
        contrastes = np.ones(3, dtype=float)
    else:
        contrastes = np.asarray(contrastes, dtype=float)
        if contrastes.shape != (3,):
            raise ValueError("Se esperaban tres factores de contraste.")
        contrastes = np.clip(
            np.nan_to_num(contrastes, nan=1.0), 1.0, 3.0
        )

    salida = np.empty_like(rgb)

    for canal in range(3):
        salida[:, :, canal] = transformar_canal(
            rgb[:, :, canal],
            objetivos[canal],
            histogramas_origen[canal],
            contrastes[canal]
        )

    return Image.fromarray(salida)


def guardar_imagen(imagen, ruta):
    """Guarda el resultado en el formato indicado por la extensión."""
    imagen.save(ruta)
