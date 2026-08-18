import time

from resultados import mostrar_resultado


def ejecutar(
    nombre,
    funcion,
    problema,
    complejidad_tiempo,
    complejidad_espacio,
    es_bidireccional=False,
    mostrar_arbol=True
):

    inicio_tiempo = time.perf_counter()

    resultado = funcion(problema)

    fin_tiempo = time.perf_counter()

    tiempo = fin_tiempo - inicio_tiempo

    salida, salida_consola = mostrar_resultado(
        nombre,
        resultado,
        es_bidireccional=es_bidireccional,
        mostrar_arbol=mostrar_arbol
    )

    informacion = ""

    informacion += "\nTiempo:\n"
    informacion += str(tiempo) + " segundos\n"

    informacion += "\nComplejidad temporal:\n"
    informacion += complejidad_tiempo + "\n"

    informacion += "\nComplejidad espacial:\n"
    informacion += complejidad_espacio + "\n"

    salida += informacion
    salida_consola += informacion

    print(salida_consola)

    return salida, resultado, tiempo