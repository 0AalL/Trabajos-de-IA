import sys
import os
sys.path.append(os.path.abspath('sistema difuso'))
# pyrefly: ignore [missing-import]
import fuzzificacion as fz
# pyrefly: ignore [missing-import]
import inferencia as inf
# pyrefly: ignore [missing-import]
import defuzzificacion as dfz
# pyrefly: ignore [missing-import]
import reglas as rgl

reglas_cargadas = rgl.cargar_reglas()
print(f"Total de reglas cargadas en base de conocimiento: {len(reglas_cargadas)}")

casos = [
    ("CASO 0: VALORES POR DEFECTO DE LA INTERFAZ (PUNTOS MEDIOS)", {
        'T_media': 0.33,
        'HR_media': 52.9,
        'Viento_medio': 7.58,
        'Precipitacion': 0.05,
        'FFMC': 51.0,
        'DMC': 130.0,
        'DC': 1759.7,
        'KBDI': 101.38
    }),
    ("CASO 1: CONDICIONES INVERNALES / SIN RIESGO (NULO)", {

        'T_media': -10.0,
        'HR_media': 85.0,
        'Viento_medio': 1.0,
        'Precipitacion': 0.05,
        'FFMC': 10.0,
        'DMC': 80.0,
        'DC': 550.0,
        'KBDI': 150.0
    }),
    ("CASO 2: CONDICIONES NORMALES / PRIMAVERA (BAJO)", {
        'T_media': 12.0,
        'HR_media': 75.0,
        'Viento_medio': 2.0,
        'Precipitacion': 0.001,
        'FFMC': 70.0,
        'DMC': 25.0,
        'DC': 150.0,
        'KBDI': 15.0
    }),
    ("CASO 3: CONDICIONES DE VERANO SECO / RIESGO ALTO", {
        'T_media': 8.0,
        'HR_media': 30.0,
        'Viento_medio': 2.0,
        'Precipitacion': 0.0,
        'FFMC': 92.0,
        'DMC': 35.0,
        'DC': 450.0,
        'KBDI': 1.0
    }),
    ("CASO 4: OLA DE CALOR Y SEQUÍA PROFUNDA / RIESGO EXTREMO", {
        'T_media': 25.0,
        'HR_media': 55.0,
        'Viento_medio': 2.8,
        'Precipitacion': 0.0,
        'FFMC': 87.0,
        'DMC': 130.0,
        'DC': 550.0,
        'KBDI': 80.0
    }),
]


for nombre, entradas in casos:
    print("=" * 80)
    print(nombre)
    print("Entradas:", entradas)
    fuzzificados = fz.fuzzificar_entradas(entradas)
    activaciones = inf.evaluar_reglas(reglas_cargadas, fuzzificados)
    
    activas = [a for a in activaciones if a['activacion'] > 0]
    print(f"Reglas activadas: {len(activas)}")
    for a in activas:
        c = a['regla']['consecuente']
        num = a['numero']
        txt = rgl.regla_a_texto(a['regla'])
        grado = a['activacion']
        print(f"  -> R{num:<2} [Salida={c:<7}]: Grado={grado:.3f} | {txt}")

        
    universo, salida_agregada = inf.agregar_salidas(reglas_cargadas, activaciones)
    resultado = dfz.defuzzificar_centroide(universo, salida_agregada)
    categoria = dfz.clasificar_riesgo(resultado)
    print(f">> RESULTADO DEFUZZIFICADO: {resultado:.2f} Ha")
    print(f">> CATEGORIA FINAL: {categoria}")
