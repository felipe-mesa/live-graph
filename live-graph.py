import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient

#CONEXION CON PLC
address = 'colocar direccion IP'
client = ModbusTcpClient(address)

#ESTRUCTURA DE LOS EJES DEL GRAFICO
#Se definen los ejes como 2 vectores de largo a definir
X = deque(maxlen=20)
Y = deque(maxlen=20)
#Se define que en cada actualización se agregara 1 elemento a los ejes
X.append(1)
Y.append(1)

app = dash.Dash(__name__)
server = app.server

#Definir layout basico
app.layout = html.Div(
    [
        html.H1(children='Monitoreo de datos de PLC en tiempor real'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000,   #Tiempo de actualización en milisegundos
            n_intervals = 0
        ),
    ]
)

#Definir wrapper, el cual gatillará la función para actualizar los datos del grafico
@app.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):

    #DEFINIR LOS DATOS QUE SE VAN A GRAFICAR
    now = datetime.now()
    registers = client.read_holding_registers(0,1).registers
    registro = int(registers[0])
    X.append(now)
    Y.append(registro)

    #Darle formato a los datos para incorporarlos en el grafico
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers' 
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)