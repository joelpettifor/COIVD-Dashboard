from requests import get
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from datetime import date, timedelta
from dash.dependencies import Input,Output, State

px.defaults.template = "simple_white"

def get_data(url):
    response = get(endpoint, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    return response.json()


endpoint = (
    'https://api.coronavirus.data.gov.uk/v1/data?'
    'filters=areaType=nation;areaName=england&'
    'structure='
    '   {'
    '       "date":"date",'
    '       "areaName":"areaName",'
    '       "newCasesBySpecimenDate":"newCasesBySpecimenDate",'
    '       "newDeathsByDeathDate":"newDeathsByDeathDate",'
    '       "newCasesBySpecimenDateRollingRate":"newCasesBySpecimenDateRollingRate",'
    '       "newDeathsByDeathDateRollingRate":"newDeathsByDeathDateRollingRate"'
    '   }'
)

def get_data2(url):
    response2 = get(endpoint2, timeout=10)

    if response2.status_code >= 400:
        raise RuntimeError(f'Request failed: {response2.text}')

    return response2.json()


endpoint2 = (
    'https://api.coronavirus.data.gov.uk/v1/data?'
    'filters=areaType=utla;areaCode=E08000021&'
    'structure={"date":"date","areaName":"areaName","newCasesBySpecimenDate":"newCasesBySpecimenDate",'
    '"newDeathsByDeathDate":"newDeathsByDeathDate","newCasesBySpecimenDateRollingRate":"newCasesBySpecimenDateRollingRate", '
    '"newDeathsByDeathDateRollingRate":"newDeathsByDeathDateRollingRate"}'
)

json_data = get_data(endpoint)
json_data2 = get_data2(endpoint2)

overview_data = []

for day in json_data['data']:
    overview_data.append([day['date'], day['newCasesBySpecimenDate'], day['newDeathsByDeathDate'], day['newCasesBySpecimenDateRollingRate'], day['newDeathsByDeathDateRollingRate']])

overview_df = pd.DataFrame(data=overview_data, columns=['Date', 'Daily Cases', 'Daily Deaths', 'Rolling Case Rate', 'Rolling Death Rate'])

localauth_data = []

for day in json_data2['data']:
    localauth_data.append([day['date'], day['newCasesBySpecimenDate'], day['newDeathsByDeathDate'], day['newCasesBySpecimenDateRollingRate'], day['newDeathsByDeathDateRollingRate']])

localauth_df = pd.DataFrame(data=localauth_data, columns=['Date', 'Daily Cases', 'Daily Deaths', 'Rolling Case Rate', 'Rolling Death Rate'])

last_month = date.today() - timedelta(30)  ###---  time frame needs checking
### -----  Last 30 days in dataframe needs to be done, date in datframe needs to changed to string -----#####
latestoverview_df = overview_df[overview_df.Date >= "2020-03-01"]
latestlocalauth_df = localauth_df[localauth_df.Date >= "2020-03-01"]

comparison_df = pd.merge(latestoverview_df, latestlocalauth_df, on='Date')

overview_cases_fig = px.line(latestoverview_df, x ='Date', y='Daily Cases', title='Daily Cases')
overview_deaths_fig = px.line(latestoverview_df, x ='Date', y='Daily Deaths', title='Daily Deaths')

local_case_rate_comp_fig = px.line(comparison_df, x='Date', y=['Rolling Case Rate_x','Rolling Case Rate_y'], title='Case Rate Comparison')
local_death_rate_comp_fig = px.line(comparison_df, x='Date', y=['Rolling Death Rate_x','Rolling Death Rate_y'], title='Case Death Comparison')
local_cases_fig = px.line(latestlocalauth_df,x='Date',y='Daily Cases',title = 'Daily Cases in Newcastle',)

layout_overview = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1('UK Covid-19 Dashboard'), className='page-header', width=10)
            ]
        ),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink('Overview', active = True, href='/overview/')),
                dbc.NavItem(dbc.NavLink('Local Trends', href='/local-trend/')),
                dbc.NavItem(dbc.NavLink('Other', href='#')),
            ],
            brand="Overview",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        dbc.Row(
            [
            dbc.Col(
                dcc.Graph(
                    id='Daily Case Graph',
                    figure=overview_cases_fig
                )
            ),
            dbc.Col(
                dcc.Graph(
                    id='Daily Death Graph',
                    figure=overview_deaths_fig
                )
            )
        ]
        )
    ]
)

layout_local_trend = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("UK Covid-19 Dashboard"), className='page-header', width=10),
            ]
        ),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink('Overview', href='/overview/')),
                dbc.NavItem(dbc.NavLink('Local Trends', active=True, href='/local-trend/')),
                dbc.NavItem(dbc.NavLink('Other', href='#')),
            ],
            brand="Local Trends",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        dbc.Row(
            [
            dbc.Col(
                dcc.Graph(
                    id='Daily Case Graph',
                    figure=local_case_rate_comp_fig
                )
            )
        ]
        ),
        dbc.Row(
            [
            dbc.Col(
                dcc.Graph(
                    id='Daily Death Graph',
                    figure=local_death_rate_comp_fig
                )
            , width='12')
        ]
        )
    ]
)


noPage = html.Div([
    html.P(["404 Page not found"])
], className="no-page")
