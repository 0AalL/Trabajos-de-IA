import random
from fuzzy_rules import FuzzyRules

NUM_GENES =  len(FuzzyRules().rules)


# ------------------------
# CREAR INDIVIDUO
# ------------------------
def crear():
    return [random.random() for _ in range(NUM_GENES)]


# ------------------------
# CROSSOVER (uniforme)
# ------------------------
def crossover(a, b):

    hijo = []

    for x, y in zip(a, b):
        if random.random() < 0.5:
            hijo.append(x)
        else:
            hijo.append(y)

    return hijo


# ------------------------
# MUTACIÓN (más agresiva)
# ------------------------
def mutar(ind, prob=0.3, intensidad=0.2):

    nuevo = ind[:]  # copiar

    for i in range(len(nuevo)):

        if random.random() < prob:
            nuevo[i] += random.uniform(-intensidad, intensidad)
            nuevo[i] = max(0, min(1, nuevo[i]))

    return nuevo


# ------------------------
# SELECCIÓN TORNEO (MEJOR QUE RULETA)
# ------------------------
def torneo(poblacion, fitnesses, k=3):

    participantes = random.sample(list(zip(poblacion, fitnesses)), k)
    participantes.sort(key=lambda x: x[1])  # menor fitness gana

    return participantes[0][0]


# ------------------------
# EVOLUCIÓN
# ------------------------
def evolucionar(poblacion, fitnesses):

    nueva_poblacion = []

    # ELITISMO (guardar mejores 2)
    ordenados = sorted(zip(poblacion, fitnesses), key=lambda x: x[1])
    elites = [ind for ind, _ in ordenados[:2]]

    nueva_poblacion.extend([e[:] for e in elites])

    #  generar resto
    while len(nueva_poblacion) < len(poblacion):

        p1 = torneo(poblacion, fitnesses)
        p2 = torneo(poblacion, fitnesses)

        hijo = crossover(p1, p2)
        hijo = mutar(hijo)

        nueva_poblacion.append(hijo)

    return nueva_poblacion