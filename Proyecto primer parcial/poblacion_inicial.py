from individuo import crear_individuo

from configuracion import TAM_POBLACION


# ============================================================
# CREAR POBLACIÓN INICIAL
# ============================================================

def crear_poblacion_inicial():

    poblacion = []

    for _ in range(
        TAM_POBLACION
    ):

        individuo = crear_individuo()

        poblacion.append(
            individuo
        )

    return poblacion