import xarray as xr
import pandas as pd
import os

# =========================================================
# CONFIGURACIÓN
# =========================================================

ARCHIVO_ENTRADA = "GlobalRx_v2024.1.csv"
ARCHIVO_SALIDA = "dataset_numerico.csv"

# Número máximo de registros para el sistema difuso
NUM_REGISTROS = 20000


columnas = [
    "T_mean",
    "RH_mean",
    "Wind_mean",
    "PPT_tot",
    "FFMC",
    "DMC",
    "DC",
    "KBDI",
    "Area Burned (Ha)"
]

# ============================================================
# LEER DATASET ORIGINAL
# ============================================================

df = pd.read_csv(ARCHIVO_ENTRADA)

print("Dataset original:")
print(f"Filas: {len(df)}")
print(f"Columnas: {len(df.columns)}")

# ============================================================
# VERIFICAR QUE LAS COLUMNAS EXISTAN
# ============================================================

columnas_faltantes = [
    columna for columna in columnas
    if columna not in df.columns
]

if columnas_faltantes:

    print("\nERROR: No se encontraron las siguientes columnas:")

    for columna in columnas_faltantes:
        print(f" - {columna}")

    raise ValueError(
        "Faltan columnas necesarias en el dataset."
    )

# ============================================================
# SELECCIONAR SOLO LAS COLUMNAS NECESARIAS
# ============================================================

df_fuzzy = df[columnas].copy()

# ============================================================
# CONVERTIR LAS COLUMNAS A VALORES NUMÉRICOS
# ============================================================

for columna in columnas:

    df_fuzzy[columna] = pd.to_numeric(
        df_fuzzy[columna],
        errors="coerce"
    )

# ============================================================
# MOSTRAR VALORES FALTANTES
# ============================================================

print("\nValores faltantes antes de eliminar registros:")

print(
    df_fuzzy.isnull().sum()
)

# ============================================================
# ELIMINAR FILAS SIN ÁREA QUEMADA
# ============================================================

df_fuzzy = df_fuzzy.dropna(
    subset=["Area Burned (Ha)"]
)

# ============================================================
# ELIMINAR FILAS QUE TENGAN DATOS FALTANTES
# ============================================================

df_fuzzy = df_fuzzy.dropna()

# ============================================================
# REDUCIR EL DATASET
# ============================================================

print("\n==============================================")
print("REDUCCIÓN DEL DATASET")
print("==============================================")

print(
    f"Registros disponibles después de limpiar: "
    f"{len(df_fuzzy)}"
)

if len(df_fuzzy) > NUM_REGISTROS:

    print(
        f"Seleccionando aleatoriamente "
        f"{NUM_REGISTROS} registros..."
    )

    df_fuzzy = df_fuzzy.sample(
        n=NUM_REGISTROS,
        random_state=42
    )

    # Reiniciar los índices
    df_fuzzy = df_fuzzy.reset_index(
        drop=True
    )

else:

    print(
        f"El dataset tiene {len(df_fuzzy)} registros, "
        f"por lo que no es necesario reducirlo."
    )

# ============================================================
# GUARDAR NUEVO DATASET
# ============================================================

df_fuzzy.to_csv(
    ARCHIVO_SALIDA,
    index=False
)

# ============================================================
# INFORMACIÓN FINAL
# ============================================================

print("\n==============================================")
print("DATASET PARA EL SISTEMA DIFUSO")
print("==============================================")

print(
    f"Filas originales: {len(df)}"
)

print(
    f"Filas finales:    {len(df_fuzzy)}"
)

print(
    f"Columnas:         {len(df_fuzzy.columns)}"
)

print("\nColumnas utilizadas:")

for columna in df_fuzzy.columns:

    print(
        f" - {columna}"
    )

print("\nPrimeros registros:")

print(
    df_fuzzy.head()
)

print(
    f"\nDataset guardado como: {ARCHIVO_SALIDA}"
)