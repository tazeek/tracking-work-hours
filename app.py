import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Define your variables

color='lightblue'

my_dashboard_title='Working Hours Dashboard'
my_bar_heading='Daily hours calculation'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)

alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]

beer_layout = go.Layout(
    barmode='group',
    title = my_dashboard_title
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Hours analysis'

# Set up the layout
app.layout = html.Div(children=[
    html.H1(my_bar_heading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    )
    ]
)

if __name__ == '__main__':
    app.run_server()