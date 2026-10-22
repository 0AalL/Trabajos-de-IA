
# poblacion.py

from individuo import crear_individuo
from configuracion import TAM_POBLACION


def crear_poblacion():

    poblacion = []

    for _ in range(TAM_POBLACION):

        individuo = crear_individuo()

        poblacion.append(individuo)

    return poblacion