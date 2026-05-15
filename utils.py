import os
from pathlib import Path
import pandas as pd
import json
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent
print("ROOT FILES:", list(BASE_DIR.glob("*")))
print("DATA FILES:", list((BASE_DIR / "Data").glob("*")))
print("BASE_DIR:", BASE_DIR)

csv_path = BASE_DIR / "Data" / "mortalidad_limpia.csv"

print("CSV PATH:", csv_path)
print("CSV EXISTS:", csv_path.exists())

df = pd.read_csv(
    csv_path
)
geojson_path = BASE_DIR / "Data" / "colombia_departamentos.geojson"

print("GEOJSON EXISTS:", geojson_path.exists())

with open(
        geojson_path,
        encoding="utf-8"
) as f:
    geojson = json.load(f)

print("\nCOLUMNAS DEL DATASET:")
print(df.columns.tolist())


def grafico_lineas():
    mensual = (
        df.groupby("MES")
        .size()
        .reset_index(name="TOTAL")
    )

    fig = px.line(
        mensual,
        x="MES",
        y="TOTAL",
        markers=True,
        title="Muertes por mes"
    )
    return fig


def grafico_homicidios():
    homicidios = df[

        df["ES_HOMICIDIO"] == True

        ].copy()

    print(
        "\nTOTAL HOMICIDIOS:",
        len(homicidios)
    )
    top = (
        homicidios
        .groupby(
            "MUNICIPIO"
        )
        .size()
        .reset_index(
            name="TOTAL"
        )
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .head(5)
    )
    print(
        "\nTOP HOMICIDIOS:"
    )
    print(top)

    fig = px.bar(
        top,
        x="MUNICIPIO",
        y="TOTAL",
        text="TOTAL",
        title="Top 5 ciudades más violentas"

    )
    fig.update_layout(
        height=500
    )
    return fig


def grafico_sexo():
    datos = (
        df.groupby(
            ["DEPARTAMENTO", "SEXO_NOMBRE"]
        )
        .size()
        .reset_index(name="TOTAL")
    )

    fig = px.bar(
        datos,
        x="DEPARTAMENTO",
        y="TOTAL",
        color="SEXO_NOMBRE",
        barmode="stack",
        title="Muertes por sexo"
    )

    return fig


def obtener_departamentos():
    return sorted(
        df["DEPARTAMENTO"]
        .dropna()
        .unique()
    )


def grafico_lineas_filtrado(
        mensual
):
    fig = px.line(
        mensual,
        x="MES",
        y="TOTAL",
        markers=True,
        title="Muertes por mes"
    )

    return fig


geojson_path = os.path.join(
    BASE_DIR,
    "Data",
    "colombia_departamentos.geojson"
)
with open(
        geojson_path,
        encoding="utf-8"
) as f:
    geojson = json.load(f)


def grafico_mapa():
    deptos = (
        df.groupby("DEPARTAMENTO")
        .size()
        .reset_index(name="TOTAL")
    )
    # normalizar nombres
    deptos["DEPARTAMENTO"] = (
        deptos["DEPARTAMENTO"]
        .astype(str)
        .str.upper()
        .str.strip()
    )
    fig = px.choropleth(
        deptos,
        geojson=geojson,
        locations="DEPARTAMENTO",
        featureidkey="properties.NOMBRE_DPT",
        color="TOTAL",
        hover_name="DEPARTAMENTO",
        projection="mercator",
        title="Mortalidad en Colombia por departamento"
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=False,
        showcoastlines=False,
        showland=True
    )
    fig.update_layout(
        height=700,
        margin={
            "r": 0,
            "t": 50,
            "l": 0,
            "b": 0
        }

    )
    return fig


print(
    df["COD_MUERTE"]
    .astype(str)
    .str.startswith("X95")
    .value_counts()
)

df = pd.read_csv("Data/mortalidad_limpia.csv"
)

print("\nCODIGOS QUE CONTIENEN X95:")

x95 = df[
    df["COD_MUERTE"]
    .astype(str)
    .str.upper()
    .str.contains("X95", na=False)
]["COD_MUERTE"].unique()

print(x95)

print("\nTOTAL ENCONTRADOS:", len(x95))


def grafico_sexo_departamento():
    datos = (
        df.groupby(
            [
                "DEPARTAMENTO",
                "SEXO_NOMBRE"
            ]
        )
        .size()
        .reset_index(
            name="TOTAL"
        )
    )
    fig = px.bar(
        datos,
        x="DEPARTAMENTO",
        y="TOTAL",
        color="SEXO_NOMBRE",
        barmode="stack",
        title="Muertes por sexo en cada departamento"
    )
    fig.update_layout(
        height=600
    )
    return fig


def grafico_edades():
    edades = (
        df.groupby(
            "CATEGORIA_EDAD"
        )
        .size()
        .reset_index(
            name="TOTAL"
        )
    )
    fig = px.bar(
        edades,
        x="CATEGORIA_EDAD",
        y="TOTAL",
        text="TOTAL",
        title="Distribución de mortalidad por grupos etarios"
    )
    fig.update_layout(
        height=500
    )
    return fig


def top_causas():
    causas = (
        df.groupby(
            [
                "COD_MUERTE",
                "NOM_CAUSA"
            ]
        )
        .size()
        .reset_index(
            name="TOTAL"
        )
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .head(10)
    )
    return causas


def grafico_menor_mortalidad():
    ciudades = (
        df.groupby(
            "MUNICIPIO"
        )
        .size()
        .reset_index(
            name="TOTAL"
        )
        .sort_values(
            "TOTAL",
            ascending=True
        )
        .head(10)

    )
    print(
        "\nCIUDADES MENOR MORTALIDAD:"
    )
    print(ciudades)
    fig = px.pie(
        ciudades,
        names="MUNICIPIO",
        values="TOTAL",
        title="10 ciudades con menor índice de mortalidad"
    )
    fig.update_layout(
        height=600
    )
    return fig