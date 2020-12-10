from WeeklyTab import WeeklyTab

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

weekly_stats_obj = WeeklyTab(tracker_obj)

def initialize_app():
    
    return html.Div([
        html.H1(children='Time Tracking Hour Analyzer', style={'textAlign': 'center'}),

        html.H4(
            id='live-update-text',
            children='Last updated: ' + weekly_stats_obj.get_current_time(), 
            style={'textAlign': 'center'}
        ),

        html.H4(
            id='finishing-time',
            children='Finishing time: ' + weekly_stats_obj.get_finishing_time_today(), 
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

        dcc.Interval(
            id='interval-component',
            interval = 2 * 60 * 1000 # 1000 = 1 second
        )
    ])

    return None

app = dash.Dash()
app.layout = initialize_app

@app.callback(
    [
        Output('live-update-text','children'),
        Output('finishing-time','children'),
        Output('total-hours-pie','figure'),
        Output('overall-week-hours','figure')
    ],
    [
        Input('interval-component','n_intervals')
    ]
)
def update_live_intervals(n):

    tracker_obj.perform_live_update()

    return [
    'Last updated: ' + weekly_stats_obj.get_current_time(),
    'Finishing time: ' + weekly_stats_obj.get_finishing_time_today(),
    weekly_stats_obj.generate_overall_hours(),
    weekly_stats_obj.generate_weekly_hours()
    ]

if __name__ == '__main__':
    
    app.run_server(debug=True)