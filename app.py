from dash import (
    Dash,
    html,
    dcc,
    dash_table,
    Input,
    Output
)
from utils import *

app = Dash(__name__)
server = app.server

app.layout = html.Div([

    html.H1(
        "Mortalidad en Colombia 2019"
    ),

    dcc.Dropdown(
        id="filtro_departamento",
        options=[
            {
                "label": d,
                "value": d
            }
            for d in obtener_departamentos()
        ],
        placeholder="Seleccione departamento"
    ),

    dcc.Graph(
        id="grafico_linea"
    ),
#dcc.Graph(
#    figure=grafico_mapa()
#),
#dcc.Graph(
 #   figure=grafico_homicidios()
#),
#dcc.Graph(
#    figure=grafico_sexo_departamento()
#),
dcc.Graph(
    figure=grafico_edades()
),
html.H3(
    "Top 10 causas de muerte"
),
dash_table.DataTable(
    data=top_causas().to_dict(
        "records"
    ),
    columns=[
        {
            "name": i,
            "id": i
        }
        for i in top_causas().columns
    ],
    page_size=10,
    sort_action="native",
    style_table={
        "overflowX": "auto"
    }
),
dcc.Graph(
    figure=grafico_menor_mortalidad()
)
])

@app.callback(
    Output(
        "grafico_linea",
        "figure"
    ),
    Input(
        "filtro_departamento",
        "value"
    )
)

def actualizar_grafico(departamento):

    datos = df.copy()

    if departamento:

        datos = datos[
            datos["DEPARTAMENTO"]
            == departamento
        ]

    mensual = (
        datos.groupby("MES")
        .size()
        .reset_index(name="TOTAL")
    )

    return grafico_lineas_filtrado(
        mensual
    )


if __name__=="__main__":
    app.run(debug=True)

dcc.Graph(
    figure=grafico_mapa()
),
app.layout = html.Div([

    html.H1(
        "Mortalidad en Colombia 2019"
    ),

    dcc.Graph(
        figure=grafico_mapa()
    ),

    dcc.Dropdown(
        id="filtro_departamento"
    ),

    dcc.Graph(
        id="grafico_linea"
    ),
    dcc.Graph(
    figure=grafico_homicidios()
    )
])

app.layout = html.Div([

    html.H1("Mortalidad Colombia 2019"),

    dcc.Graph(
        figure=grafico_mapa()
    ),

    dcc.Dropdown(
        id="filtro_departamento",
        options=[
            {"label": dep, "value": dep}
            for dep in sorted(df["DEPARTAMENTO"].unique())
        ],
        placeholder="Seleccione un departamento",
        clearable=True
    ),
    dcc.Graph(
        id="grafico_homicidios",
        figure=grafico_homicidios()
    )
])