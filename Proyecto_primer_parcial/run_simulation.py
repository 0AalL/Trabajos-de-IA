from hospital import Hospital
from patients import generar_lista_pacientes
from config import *
from simulation import Simulation


def main(num_patients, doctors):

    simulation = Simulation(
        NUM_PATIENTS=num_patients,
        DOCTORS=doctors
    )

    result = simulation.history()

    hospital = result["hospital"]
    best_ind = result["best_ind"]

    return {
        "best_ind": best_ind,
        "waits": hospital.waits,
        "history_fitness": result["history_fitness"],
        "history_ratio_graves": result["history_ratio_graves"],
        "history_promedios": result["history_promedios"]
    }