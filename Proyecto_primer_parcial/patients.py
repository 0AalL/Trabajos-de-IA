import random
from config import *

# ----------------------------
# PROBABILIDAD DE SER GRAVE
# (sin sigmoide, suma ponderada)
# ----------------------------
def probabilidad_grave(hr, rr, spo2):

    prob = 0.0

    # SPO2 (más importante)
    if spo2 < 90:
        prob += 0.6
    elif spo2 < 94:
        prob += 0.25

    # Frecuencia cardíaca
    if hr > 130:
        prob += 0.3
    elif hr > 110:
        prob += 0.15

    # Frecuencia respiratoria
    if rr > 30:
        prob += 0.3
    elif rr > 22:
        prob += 0.15

    # Limitar probabilidad
    prob = min(prob, 0.95)

    return prob


# ----------------------------
# GENERADOR DE PACIENTES
# ----------------------------
def generar_lista_pacientes(n=30):

    pacientes = []
    tiempo_actual = 0

    for i in range(n):

        # ----------------------------
        # Llegadas
        # ----------------------------
        delta = random.uniform(
            TIEMPO_MIN_ESPERA_ENTRE_PACIENTES,
            TIEMPO_MAX_ESPERA_ENTRE_PACIENTES
        )
        tiempo_actual += delta

        # ----------------------------
        # SESGO HACIA GRAVES
        # ----------------------------
        bias = random.random()

        if bias < 0.20:
            # graves
            hr = random.gauss(140, 50)
            rr = random.gauss(35, 12)
            spo2 = random.gauss(88, 10)

        elif bias < 0.75:
            # moderados
            hr = random.gauss(110, 30)
            rr = random.gauss(25, 8)
            spo2 = random.gauss(93, 5)

        else:
            # leves
            hr = random.gauss(85, 20)
            rr = random.gauss(18, 5)
            spo2 = random.gauss(97, 2)

        # ----------------------------
        # CLAMP (valores realistas)
        # ----------------------------
        hr = max(30, min(240, hr))
        rr = max(5, min(60, rr))
        spo2 = max(50, min(100, spo2))

        # ----------------------------
        # GRAVEDAD PROBABILÍSTICA
        # ----------------------------
        prob = probabilidad_grave(hr, rr, spo2)
        grave = random.random() < prob

        # ----------------------------
        # PACIENTE FINAL
        # ----------------------------
        pacientes.append({
            "id": i,
            "hr": hr,
            "rr": rr,
            "spo2": spo2,
            "arrival": tiempo_actual,
            "grave": grave,        #  ground truth
            "prob_grave": prob     # útil para debug
        })

    return pacientes