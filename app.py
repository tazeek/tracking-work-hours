from WeeklyTab import WeeklyTab
from Tracker import Tracker

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

tracker_obj = Tracker()
tracker_obj.update_time_calculations()

weekly_stats_obj = WeeklyTab(tracker_obj)

def initialize_app():
    
    return html.Div([
        html.H1(children='Time Tracking Hour Analyzer', style={'textAlign': 'center'}),

        html.H4(
            id='live-update-text',
            children='Last updated: ' + tracker_obj.get_current_time(), 
            style={'textAlign': 'center'}
        ),

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
                id='total-hours-pie',
                style={'display': 'inline-block'},
                figure=weekly_stats_obj.generate_overall_hours()
            )
        ]),

        dcc.Graph(
            id='time-analysis',
            figure=weekly_stats_obj.generate_noon_comparisons()
        ),

        dcc.Interval(
            id='interval-component',
            interval = 5 * 60 * 1000 # 1000 = 1 second
        )
    ])

    return None

app = dash.Dash()
app.layout = initialize_app

@app.callback(
    [
        Output('live-update-text','children'),
        Output('total-hours-pie','figure'),
        Output('time-analysis','figure'),
        Output('overall-week-hours','figure')
    ],
    [
        Input('interval-component','n_intervals')
    ]
)
def update_live_intervals(n):

    return [
    'Last updated: ' + tracker_obj.get_current_time(),
    weekly_stats_obj.generate_overall_hours(),
    weekly_stats_obj.generate_noon_comparisons(),
    weekly_stats_obj.generate_weekly_hours()
    ]

if __name__ == '__main__':
    
    app.run_server(debug=True)