import sys
import os
sys.path.append(os.path.abspath('sistema difuso'))
# pyrefly: ignore [missing-import]
from reglas import cargar_reglas
# pyrefly: ignore [missing-import]
from fuzzificacion import fuzzificar_entradas
# pyrefly: ignore [missing-import]
from inferencia import evaluar_reglas, agregar_salidas
# pyrefly: ignore [missing-import]
from defuzzificacion import defuzzificar_centroide, clasificar_riesgo

reglas = cargar_reglas()
print(f"Total reglas cargadas en el sistema difuso: {len(reglas)}")

# Caso A: Valores bajos y benignos (HR normal/alta, Viento bajo, DC medio, KBDI medio)
e_bajo = {
    'T_media': 12.0,      # medio
    'HR_media': 70.0,     # normal
    'Viento_medio': 2.0,  # bajo/medio
    'Precipitacion': 0.001,
    'FFMC': 75.0,
    'DMC': 25.0,          # medio
    'DC': 200.0,          # medio
    'KBDI': 20.0          # medio
}

fuzz_b = fuzzificar_entradas(e_bajo)
act_b = evaluar_reglas(reglas, fuzz_b)
u_b, out_b = agregar_salidas(reglas, act_b)
res_b = defuzzificar_centroide(u_b, out_b)
cat_b = clasificar_riesgo(res_b)
print(f"\nCaso A (Valores Benignos/Bajos): Area Estimada = {res_b:.2f} Ha | Riesgo = {cat_b}")
print("Reglas que se activaron:")
for a in act_b:
    if a['activacion'] > 0.05:
        print(f"  Regla {a['numero']} ({a['regla']['consecuente']}) -> Activación: {a['activacion']:.3f}")

# Caso B: Valores extremos de desastre (Viento medio/alto, DMC extremo, DC alto, KBDI alto)
e_extremo = {
    'T_media': 30.0,      # extremo
    'HR_media': 30.0,     # bajo
    'Viento_medio': 3.0,  # medio
    'Precipitacion': 0.0,
    'FFMC': 90.0,         # alto
    'DMC': 200.0,         # extremo
    'DC': 600.0,          # alto
    'KBDI': 120.0         # alto
}

fuzz_e = fuzzificar_entradas(e_extremo)
act_e = evaluar_reglas(reglas, fuzz_e)
u_e, out_e = agregar_salidas(reglas, act_e)
res_e = defuzzificar_centroide(u_e, out_e)
cat_e = clasificar_riesgo(res_e)
print(f"\nCaso B (Valores Críticos/Extremos): Area Estimada = {res_e:.2f} Ha | Riesgo = {cat_e}")
print("Reglas que se activaron:")
for a in act_e:
    if a['activacion'] > 0.05:
        print(f"  Regla {a['numero']} ({a['regla']['consecuente']}) -> Activación: {a['activacion']:.3f}")

# Caso C: Sequía estacional extrema pero sin ignición (KBDI extremo) -> NULO
e_nulo = {
    'T_media': 15.0,
    'HR_media': 50.0,     # bajo
    'Viento_medio': 2.0,
    'Precipitacion': 0.0001, # bajo
    'FFMC': 85.0,         # alto
    'DMC': 80.0,          # alto
    'DC': 500.0,          # alto
    'KBDI': 180.0         # extremo
}

fuzz_n = fuzzificar_entradas(e_nulo)
act_n = evaluar_reglas(reglas, fuzz_n)
u_n, out_n = agregar_salidas(reglas, act_n)
res_n = defuzzificar_centroide(u_n, out_n)
cat_n = clasificar_riesgo(res_n)
# Caso D: Riesgo Alto (FFMC extremo, KBDI bajo, DC alto)
e_alto = {
    'T_media': 15.0,      # medio
    'HR_media': 30.0,     # muy_bajo
    'Viento_medio': 2.5,
    'Precipitacion': 0.0001, # bajo
    'FFMC': 93.0,         # extremo
    'DMC': 40.0,          # medio
    'DC': 600.0,          # alto
    'KBDI': 1.0           # bajo
}

fuzz_a = fuzzificar_entradas(e_alto)
act_a = evaluar_reglas(reglas, fuzz_a)
u_a, out_a = agregar_salidas(reglas, act_a)
res_a = defuzzificar_centroide(u_a, out_a)
cat_a = clasificar_riesgo(res_a)
print(f"\nCaso D (Riesgo Alto): Area Estimada = {res_a:.2f} Ha | Riesgo = {cat_a}")
print("Reglas que se activaron:")
for a in act_a:
    if a['activacion'] > 0.05:
        print(f"  Regla {a['numero']} ({a['regla']['consecuente']}) -> Activación: {a['activacion']:.3f}")
