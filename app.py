from tab.WeeklyTab import WeeklyTab

from controller.controller import register_callbacks
from layout.layout import generate_layout

import dash
import dash_bootstrap_components as dbc

weekly_stats_obj = WeeklyTab()

def serve_layout():

	return generate_layout(weekly_stats_obj)

app = dash.Dash(
	__name__,
	title='Work Hours Analytics',
	external_stylesheets=[dbc.themes.MINTY]
)

app.layout = serve_layout
register_callbacks(app,weekly_stats_obj)

if __name__ == '__main__':
    
    app.run_server(debug=True)