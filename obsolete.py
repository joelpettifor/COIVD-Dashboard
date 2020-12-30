import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from requests import get
from requests import get
import pandas as pd


def get_data(url):
    response = get(endpoint, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    return response.json()

if __name__ == '__main__':
    endpoint = (
            'https://api.coronavirus.data.gov.uk/v1/data?'
            'filters=areaType=utla;areaCode=E08000021&'
            'structure={"date":"date","areaName":"areaName","newCasesBySpecimenDate":"newCasesBySpecimenDate",'
            '"newDeathsByDeathDate":"newDeathsByDeathDate"} '
        )

json_data = get_data(endpoint)

localauth_data = []

for day in json_data['data']:
    localauth_data.append([day['date'],day['newCasesBySpecimenDate'],day['newDeathsByDeathDate']])

localauth_df = pd.DataFrame(data=localauth_data, columns=['Date', 'Daily Cases', 'Daily Deaths'])

external_stylesheets = [dbc.themes.SANDSTONE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div([
    # Column: Title + Map
    html.Div([
        # Row: Title
        html.Div([
            html.H1("Uk Covid Dashboard", className="text-center")
        ], className="row"),
        # Row: Map
        html.Div([
            dcc.Graph(id="bigfoot-map")
        ], className="row")
    ], className="col-md-12")
], className="container-fluid")


if __name__ == '__main__':
    app.run_server(debug=True)
    endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=utla;areaCode=E08000021&'
        'structure={"date":"date","areaName":"areaName","newCasesBySpecimenDate":"newCasesBySpecimenDate",'
        '"newDeathsByDeathDate":"newDeathsByDeathDate"} '
    )