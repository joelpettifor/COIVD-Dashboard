from requests import get
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table

def get_data(url):
    response = get(endpoint, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    return response.json()


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



layout_overview = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H5('Overview'),
            html.Div('''
                Overview Page
            ''')
        ])
    )
])

layout_local_trend = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H5('Overview'),
            html.Div('''
                Local Trend Page
            ''')
        ])
    )
])

noPage = html.Div([
    html.P(["404 Page not found"])
    ], className="no-page")

