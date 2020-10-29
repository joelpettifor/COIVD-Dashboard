import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime

app = dash.Dash(__name__,
external_stylesheets=[dbc.themes.SANDSTONE])


server = app.server

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col(html.H1(children='COVID-19 Dashboard'),width={'size':6, 'offset':3}),
        dbc.Col(html.Div(children='''A dashboard of Covid Cases in the UK'''), width=4)
    ]),

    dbc.Row([
        html.Div(children='''
            symbol to graph:
        '''),
        dcc.Input(id='input', value='tsla', type='text')
    ]),
    dbc.Row([

    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output-graph'), width=6),

        dbc.Col(dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x':['Jan','Feb','Mar','Apr','May'], 'y': [4,1,2,5,8], 'type': 'line', 'name': 'Cases'},
                    {'x':['Jan','Feb','Mar','Apr','May'], 'y': [2,4,5,1,5], 'type': 'line', 'name': 'Deaths'},
                ]

            }
        ), width=6)
    ])
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
    )
def update_graph(input_data):

    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)

    return dcc.Graph(
        id='example graph',
        figure={
            'data':[
                {'x':df.index, 'y': df.Close, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
