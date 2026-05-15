import pandas as pd

# =========================
# 1. CARGA DE DATOS
# =========================
df = pd.read_excel("data/Anexo1.NoFetal2019_CE_15-03-23.xlsx")
divipola = pd.read_excel("data/Divipola_CE_.xlsx")
cie = pd.read_excel(
    "data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx",
    sheet_name="Final",
    skiprows=8
)
# limpiar nombres de columnas
cie.columns = cie.columns.str.strip()
# renombrar columnas del catálogo
cie = cie.rename(
    columns={
        "Código de la CIE-10 cuatro caracteres":
            "COD_MUERTE",
        "Descripcion  de códigos mortalidad a cuatro caracteres":
            "NOM_CAUSA"
    }
)
df = df.merge(
    cie[
        [
            "COD_MUERTE",
            "NOM_CAUSA"
        ]
    ],
    on="COD_MUERTE",
    how="left"
)

# =========================
# 2. LIMPIEZA DE COLUMNAS
# =========================

df.columns = df.columns.str.strip().str.upper()
divipola.columns = divipola.columns.str.strip().str.upper()
cie.columns = cie.columns.str.strip().str.upper()

# Renombrar columnas clave si es necesario
divipola = divipola.rename(columns={
    "CODIGO DANE DEL MUNICIPIO": "COD_DANE",
    "NOMBRE DEL DEPARTAMENTO": "DEPARTAMENTO",
    "NOMBRE DEL MUNICIPIO": "MUNICIPIO"
})

cie = cie.rename(columns={
    "CODIGO": "COD_MUERTE",
    "DESCRIPCION": "NOM_CAUSA"
})

# =========================
# 3. UNIONES
# =========================

# unión con nombres de municipios
df = df.merge(
    divipola[["COD_DANE","DEPARTAMENTO","MUNICIPIO"]],
    on="COD_DANE",
    how="left"
)

# df = df.merge(
#     cie[["COD_MUERTE","NOM_CAUSA"]],
#     on="COD_MUERTE",
#     how="left"
# )
cie = pd.read_excel(
    "data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx",
    sheet_name="Final",
    skiprows=8
)
print("\nCOLUMNAS DEL ARCHIVO CIE:")
print(cie.columns.tolist())

print("\nPRIMERAS FILAS:")
print(cie.head(10))



# unión con causas de muerte
print("Columnas CIE:")
print(cie.columns.tolist())

# =========================
# 4. TRANSFORMACIONES
# =========================

# Sexo
def map_sexo(x):
    if x == 1:
        return "Hombre"
    elif x == 2:
        return "Mujer"
    else:
        return "No definido"

df["SEXO_NOMBRE"] = df["SEXO"].apply(map_sexo)

# Categorías de edad
def categorizar_edad(x):

    if pd.isna(x):
        return "Sin dato"

    if x <= 4:
        return "Neonatal"
    elif x <= 6:
        return "Infantil"
    elif x <= 8:
        return "Primera infancia"
    elif x <= 10:
        return "Niñez"
    elif x == 11:
        return "Adolescencia"
    elif x <= 13:
        return "Juventud"
    else:
        return "Adulto"

df["CATEGORIA_EDAD"] = df["GRUPO_EDAD1"].apply(categorizar_edad)

# Año
df["AÑO"] = 2019

# =========================
# 5. VARIABLES CLAVE
# =========================

# Homicidios (prefijo X95)
df["ES_HOMICIDIO"] = df["COD_MUERTE"].astype(str).str.startswith("X95")

# =========================
# 6. LIMPIEZA FINAL
# =========================

# eliminar filas sin departamento o municipio
df = df.dropna(subset=["DEPARTAMENTO","MUNICIPIO"])

# asegurar tipos
df["MES"] = pd.to_numeric(df["MES"], errors="coerce")

# =========================
# 7. EXPORTAR
# =========================

df.to_csv("data/mortalidad_limpia.csv", index=False)

print("✅ ETL completado")
print("Filas:", len(df))
print("Columnas:", df.columns.tolist())
print(
    df[
        [
            "COD_MUERTE",
            "NOM_CAUSA"
        ]
    ].head()
)