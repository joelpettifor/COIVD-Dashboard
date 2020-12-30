import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import server
from app import app
from layouts import layout_overview, layout_local_trend
import callbacks

app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Uk Covid Data Dashboard</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
        <div>Uk Covid Data Dashboard</div>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/uk-covid-dashboard' or pathname == '/uk-covid-dashboard/overview/':
        return layout_overview
    elif pathname == '/uk-covid-dashboard/local-trend/':
        return layout_local_trend
    else:
        return noPage

if __name__ == '__main__':
    app.run_server(debug=True)