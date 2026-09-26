def puede_transformarse(inicial, final):

    # Eliminamos el espacio vacío
    a = [x for x in inicial if x != 0]
    b = [x for x in final if x != 0]

    # Calculamos la paridad de las inversiones
    def paridad(estado):

        inversiones = 0

        for i in range(len(estado)):

            for j in range(i + 1, len(estado)):

                if estado[i] > estado[j]:
                    inversiones += 1

        return inversiones % 2

    return paridad(a) == paridad(b)