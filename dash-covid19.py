#COSAS POR CAMBIAR:
#CONVERTIR EL TEXTBOX EN DROPDOWN
#SUPERPONER GRAFICAS POR PAIS
#CAMBIAR EL NOMBRE DE LA APP EN HEROKU
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#CREACION DATAFRAME CORONAVIRUS CHILE
url = 'https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/'
tables = pd.read_html(url)
df = tables[0]
df = df.drop([0,18])
header = df.iloc[0]
header[0] = 'Region'
df = df[1:]
df.columns = header
df['Casos totales acumulados'] = df['Casos totales acumulados'].str.replace(".","").astype(int)
df['Casos nuevos totales'] = df['Casos nuevos totales'].str.replace(".","").astype(int)
df['% Total'] = df['% Total'].str.replace(".",",")

#DESCARGAR E IMPORTAR DATOS GLOBALES DE CORONAVIRUS DESDE GITHUB
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
data = pd.read_csv(url, index_col = 0)
#PREPARACION Y LIMPIEZA DE LA TABLA
data = data.drop(['Lat', 'Long'], axis = 1)
data = data.groupby(['Country/Region']).sum()
data = data.T

#INICIAR APLICACION DASH
app = dash.Dash()
server = app.server #Importante

#Preparar el layout de la app, se colocan 2 graficos estativos y el textbox para hacer la consulta de un pais a graficar
app.layout = html.Div(children=[
    html.H1(children='Datos COVID-19 en Chile'),
    
    dcc.Graph(
        id='example',
        figure={
            'data': [{
                'x': df['Region'],
                'y': df['Casos totales acumulados'],
                'type': 'bar',
                'name': 'Casos totales'},
            ],
            'layout': {
                'title': 'Contagios por Covid 19',
            }
        }
    ),    

    dcc.Graph(
        id='example2',
        figure={
            'data': [{
                'x': df['Region'],
                'y': df['Casos nuevos totales'],
                'type': 'bar',
                'name': 'Casos nuevos'
            }],
            'layout': {
                'title': 'Casos Nuevos Covid 19'
            }
        }
    ),

    html.H2(children='Datos COVID-19 por Pais'),
    html.Div(children=[
        html.Div(children='Ingrese pais'),
        dcc.Input(id='input', value='Ej: Chile', type='text'),
        html.Div(id='output-graph')
    ])    
])

#LEER DATOS DEL TEXTBOX Y USARLOS PARA MOSTRAR DATOS DEL DATAFRAME
#EL CALLBACK CUANDO ES USADO, ACTIVA AUTOMATICAMENTE LA FUNCION UPDATE_VALUE
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [{
                'x': data.index,
                'y': data[input_data],
                'type': 'line',
                'name': input_data #USANDO INPUT_DATA SE BUSCA EL PAIS EN EL DATAFRAME
            }],
            'layout': {
                'title': input_data
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)