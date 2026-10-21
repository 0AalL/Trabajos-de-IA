import simpy
import matplotlib.pyplot as plt

from config import *
from patients import generar_lista_pacientes
from hospital import Hospital
from fitness import fitness
from ga import crear, evolucionar


class Simulation:
    def __init__(self, NUM_PATIENTS=NUM_PATIENTS, DOCTORS=DOCTORS):
        self.doctors = DOCTORS
        self.pacientes = generar_lista_pacientes(NUM_PATIENTS)

    def run(self, ind):
        """
        Ejecuta un hospital con un individuo
        y retorna SOLO fitness.
        """
        hospital = Hospital(self.doctors, ind, self.pacientes.copy())
        hospital.run()
        return fitness(hospital)

    def history(self):

        pop = [crear() for _ in range(POPULATION_SIZE)]

        history_fitness = []
        history_promedios = []
        history_ratio_graves = []

        best_ind = None
        best_hospital = None

        for g in range(GENERATIONS):

            # evaluar población
            scored = [(self.run(i), i) for i in pop]

            # ordenar por fitness (ya es escalar)
            scored_sorted = sorted(scored, key=lambda x: x[0])

            best = scored_sorted[0]

            best_fitness = best[0]
            best_ind = best[1]

            # reconstruir hospital del mejor individuo
            best_hospital = Hospital(self.doctors, best_ind, self.pacientes.copy())
            best_hospital.run()

            # métricas reales (para graficar)
            t = sum(best_hospital.waits) / len(best_hospital.waits)

            if best_hospital.total_graves == 0:
                ratio = 0
            else:
                ratio = best_hospital.graves_1min / best_hospital.total_graves

            # guardar historial
            history_fitness.append(best_fitness)
            history_promedios.append(t)
            history_ratio_graves.append(ratio)

            # evolución GA
            fitnesses = [s[0] for s in scored]
            pop = evolucionar(pop, fitnesses)

        return {
            "hospital": best_hospital,
            "best_ind": best_ind,

            "history_fitness": history_fitness,
            "history_ratio_graves": history_ratio_graves,
            "history_promedios": history_promedios
        }