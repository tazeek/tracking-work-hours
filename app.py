from WeeklyTab import WeeklyTab
from Tracker import Tracker

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):
    
    app.layout = html.Div([
        html.H1(children='Time Tracking Hour Analyzer'),
        html.H4(children='Finishing time: ' + tracker_obj.get_finishing_time_today()),
        dcc.Tabs(id='tabs', value='overall', children=[
            dcc.Tab(label='Weekly Stats', value='overall')
        ]),
        html.Div(id='data-graphs')
    ])

    return None

def load_stats_objects():

    tracker_obj = Tracker()
    tracker_obj.update_time_calculations()

    return WeeklyTab(tracker_obj), tracker_obj

weekly_stats_obj, tracker_obj = load_stats_objects()

app = dash.Dash()
initialize_app(app)

@app.callback(
    Output('data-graphs','children'),
    [Input('tabs','value')]
)
def create_graphs_tabs(stat_name):

    return [
        dcc.Graph(id='overall-week-hours',figure=weekly_stats_obj.generate_weekly_hours()),
        dcc.Graph(id='total-hours-pie',figure=weekly_stats_obj.generate_overall_hours()),
        dcc.Graph(id='time-analysis',figure=weekly_stats_obj.generate_noon_comparisons())
    ]


if __name__ == '__main__':
    
    app.run_server(debug=True)