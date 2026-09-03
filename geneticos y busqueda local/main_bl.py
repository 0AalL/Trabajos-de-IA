print(">>> Iniciando main_bl.py")

from busqueda_local import busqueda_local_con_reinicios
from visualizacion import obtener_datos_individuo, visualizar_solucion
from iluminacion import cuadricula_a_coordenadas
from configuracion import NUM_FOCOS


def ejecutar():
    print(">>> Ejecutando búsqueda local...")

    mejor, fitness, historial = busqueda_local_con_reinicios(
        reinicios=10,
        max_iter=120,
        max_sin_mejora=30
    )

    print(">>> Búsqueda terminada.")

    datos = obtener_datos_individuo(mejor)

    print("=" * 60)
    print("BÚSQUEDA LOCAL (HILL CLIMBING + REINICIOS)")
    print("=" * 60)
    print(f"Fitness: {datos['fitness']:.6f}")
    print(f"Cobertura: {datos['cobertura']:.2f}%")
    print(f"Potencia total: {datos['potencia']} W")
    print(f"Focos encendidos: {datos['focos']}")

    print("\nUbicación de focos:")
    for i in range(NUM_FOCOS):
        c = mejor[i * 2]
        p = mejor[i * 2 + 1]
        x, y = cuadricula_a_coordenadas(c)
        estado = "ENCENDIDO" if p > 0 else "APAGADO"
        print(f"Foco {i+1}: Cuadrícula {c} -> ({x:.2f}, {y:.2f}) - {p} W - {estado}")

    visualizar_solucion(mejor)


if __name__ == "__main__":
    print(">>> Entró al __main__")
    ejecutar()