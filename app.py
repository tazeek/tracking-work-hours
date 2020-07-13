import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Define your variables

color='lightblue'

my_dashboard_title='Working Hours Dashboard'
my_bar_heading='Daily hours calculation'

# Set up the charts


# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Hours analysis'

# Set up the layout
app.layout = html.Div(children=[
    html.H1(my_bar_heading)
    ]
)

if __name__ == '__main__':
    app.run_server()