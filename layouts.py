from requests import get
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from datetime import date, timedelta

px.defaults.template = "simple_white"

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
    localauth_data.append([day['date'], day['newCasesBySpecimenDate'], day['newDeathsByDeathDate']])

localauth_df = pd.DataFrame(data=localauth_data, columns=['Date', 'Daily Cases', 'Daily Deaths'])

last_month = date.today() - timedelta(30)  ###---  time frame needs checking
### -----  Last 30 days in dataframe needs to be done, date in datframe needs to changed to string -----#####
latestlocalauth_df = localauth_df[localauth_df.Date >= "2020-10-01"]

nav = dbc.Nav(
    [
        dbc.NavLink("Navbar", className='navbar-brand'),
        dbc.NavLink("A link", className='nav-link', active=True, href="#"),
        dbc.NavLink("Another link", href="#"),
        dbc.NavLink("Disabled", disabled=True, href="#"),
    ]
    , className='navbar navbar-expand-lg navbar-dark bg-primary',
)

layout_overview = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("Covid 19 Dashboard"), className='page-header', width=9),
                dbc.Button("Success", color="success"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavLink("Navbar", className='navbar-brand'),
                            dbc.NavLink("Overview", className='nav-link', active=True, href="#"),
                            dbc.NavLink("Local Trends", href="#"),
                            dbc.NavLink("Disabled", disabled=True, href="#"),
                        ]
                        , className='navbar navbar-expand-lg navbar-dark bg-primary',
                    )
                    , width=12)
            ]
        ),
        dbc.Row(
            dcc.Graph(
                id='Daily Case Graph',
                figure=px.line(latestlocalauth_df,
                               x='Date',
                               y='Daily Cases',
                               title = 'Daily Cases',
                               )
            )
        )
    ]
)

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
