from requests import get
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from datetime import date, timedelta

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

last_month = date.today() - timedelta(30)   ###---  time frame needs checking
### -----  Last 30 days in dataframe needs to be done, date in datframe needs to changed to string -----#####
latestlocalauth_df = localauth_df[localauth_df.Date >= "2020-10-01"]


print(start_date)

print(localauth_df.head)
print(latestlocalauth_df.head)