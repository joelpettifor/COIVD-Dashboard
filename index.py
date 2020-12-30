import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app, server
from layouts import layout_overview, layout_local_trend, noPage

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

server = app.server

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/overview/':
        return layout_overview
    elif pathname == '/local-trend/':
        return layout_local_trend
    else:
        return noPage


if __name__ == '__main__':
    app.run_server(debug=False)
