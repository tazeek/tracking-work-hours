from WeeklyTab import WeeklyTab
from Tracker import Tracker

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app():

    tracker_obj = Tracker()
    tracker_obj.update_time_calculations()

    weekly_stats_obj = WeeklyTab(tracker_obj)
    
    return html.Div([
        html.H1(children='Time Tracking Hour Analyzer', style={'textAlign': 'center'}),

        html.H4(
            children='Finishing time: ' + tracker_obj.get_finishing_time_today(), 
            style={'textAlign': 'center'}
        ),

        html.Div(children=[

            dcc.Graph(
                id='overall-week-hours', 
                style={'display': 'inline-block'}, 
                figure=weekly_stats_obj.generate_weekly_hours()
            ),

            dcc.Graph(
                id='time-analysis',
                style={'display': 'inline-block'},
                figure=weekly_stats_obj.generate_noon_comparisons()
            )
        ]),

        dcc.Graph(
            id='total-hours-pie',
            figure=weekly_stats_obj.generate_overall_hours(),
            style={'margin':'auto','width': "50%"}
        )
    ])

    return None

if __name__ == '__main__':

    app = dash.Dash()

    app.layout = initialize_app
    
    app.run_server(debug=True)