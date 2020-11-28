from Tracker import Tracker
from WeeklyTab import WeeklyTab

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

tracker_obj = Tracker()
tracker_obj.update_time_calculations()

weekly_stats_obj = WeeklyTab(tracker_obj)

app.layout = html.Div(children=[
    dcc.Graph(id='overall-week-hours',figure=weekly_stats_obj.generate_weekly_hours()),
    dcc.Graph(id='total-hours-pie',figure=weekly_stats_obj.generate_overall_hours()),
    dcc.Graph(id='time-analysis',figure=weekly_stats_obj.generate_noon_comparisons())
])

if __name__ == '__main__':
    app.run_server(debug=True)