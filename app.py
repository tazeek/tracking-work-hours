from WeeklyTab import WeeklyTab
from TodayTab import TodayTab
from Tracker import Tracker

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

    tracker_obj = Tracker()
    tracker_obj.update_time_calculations()

    weekly_stats_obj = WeeklyTab(tracker_obj)
    today_stats_obj = TodayTab(tracker_obj)
    
    app.layout = html.Div([
        dcc.Tabs(id='tabs', value='week-tab', children=[
            dcc.Tab(label='Weekly Stats', value='overall'),
            dcc.Tab(label='Today Stats', value='today')
        ]),
        html.Div(id='data-graphs')
    ])

    return None

app = dash.Dash()
initialize_app(app)

@app.callback(
    Output('data-graphs','children'),
    [Input('tabs','value')]
)
def create_graphs_tabs(stat_name):
    print(stat_name)

if __name__ == '__main__':
    
    app.run_server(debug=True)