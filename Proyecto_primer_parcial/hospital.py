import copy
import simpy
from fuzzy_system import FuzzySystem
from config import *

class Hospital:

    def __init__(self, doctors, genes, pacientes):

        self.env = simpy.Environment()
        self.doctors = doctors
        self.fuzzy = FuzzySystem(genes)

        self.pacientes = copy.deepcopy(pacientes)
        self.queue = []

        self.waits = []

        # Métricas reales (independientes del fuzzy)
        self.graves_1min = 0
        self.graves_atendidos = 0

        self.total_pacientes = len(self.pacientes)
        self.total_graves = sum(1 for p in self.pacientes if p["grave"])

        self.atendidos = 0

    # -------------------
    # LLEGADA
    # -------------------
    def llegada(self):
        for p in self.pacientes:
            yield self.env.timeout(p["arrival"] - self.env.now)
            self.queue.append(p)

    # -------------------
    # DOCTOR
    # -------------------
    def doctor(self, id_doc):

        while self.atendidos < self.total_pacientes:

            if not self.queue:
                yield self.env.timeout(0.1)
                continue

            best_p = None
            best_priority = -1

            # Selección del paciente con mayor prioridad
            for p in self.queue:
                wait = self.env.now - p["arrival"]

                priority = self.fuzzy.infer(
                    p["hr"], p["rr"], p["spo2"], wait
                )

                if priority > best_priority:
                    best_priority = priority
                    best_p = p

            # Tiempo de espera correcto
            wait = self.env.now - best_p["arrival"]
            self.waits.append(wait)

            # Métricas basadas en gravedad real (no fuzzy)
            if best_p["grave"]:
                self.graves_atendidos += 1

                if wait >= 1:
                    self.graves_1min += 1

            self.queue.remove(best_p)

            # Servicio
            service_time = self.service_time(best_p)
            yield self.env.timeout(service_time)

            self.atendidos += 1

    # -------------------
    # TIEMPO SERVICIO
    # -------------------
    def service_time(self, p):
        if p["grave"]:
            return TIEMPO_MAXIMO_DE_CONSULTA
        else:
            return TIEMPO_MAXIMO_DE_CONSULTA * 0.5

    # -------------------
    # RUN
    # -------------------
    def run(self):

        self.env.process(self.llegada())

        for i in range(self.doctors):
            self.env.process(self.doctor(i))

        self.env.run()