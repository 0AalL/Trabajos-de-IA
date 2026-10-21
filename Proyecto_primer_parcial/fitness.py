def fitness(hospital):

    if len(hospital.waits) == 0:
        return 0

    # tiempo promedio
    t = sum(hospital.waits) / len(hospital.waits)

    # ratio de críticos atendidos tarde
    if hospital.total_graves == 0:
        ratio = 0
    else:
        ratio = hospital.graves_1min / hospital.total_graves

    # fitness final
    fitness = t + ratio * 200

    return fitness