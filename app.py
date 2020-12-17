from WeeklyTab import WeeklyTab

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

weekly_stats_obj = WeeklyTab()

def initialize_app():

    finishing_time = weekly_stats_obj.get_finishing_time()
    today_coverage = weekly_stats_obj.get_today_coverage()
    last_updated = weekly_stats_obj.get_current_time()
    overall_hours_fig = weekly_stats_obj.generate_weekly_hours()
    total_hours_fig = weekly_stats_obj.generate_overall_hours()
    weekly_coverage_table = weekly_stats_obj.generate_weekly_coverage()
    
    return html.Div([

        html.Div(id='hidden-div', style={'display':'none'}),

        html.H1(children='Time Tracking Hour Analyzer'),

        html.H4(
            id='finishing-time',
            children='Finishing time: ' + finishing_time
        ),

        html.H4(
            id='today-coverage',
            children="Today's coverage: " + today_coverage
        ),

        html.H4(
            id='live-update-text',
            children='Last updated: ' + last_updated
        ),

        html.Button('Reset Hours', id='reset-hours'),

        html.Div(children=[

            html.Div(className='graph-displayer', children = [
                dcc.Graph(
                    id='overall-week-hours',
                    figure=overall_hours_fig,
                    config={'displayModeBar': False}
                )
            ]),

            html.Div(className='graph-displayer', children = [
                dcc.Graph(
                    id='total-hours-pie',
                    figure=total_hours_fig,
                    config={'displayModeBar': False}
                )
            ])
        ]),

        html.H4(children='Weekly coverage'),
        weekly_coverage_table,

        dcc.Interval(
            id='interval-component',
            interval = 2 * 60 * 1000 # 1000 = 1 second
        )
    ])

    return None

app = dash.Dash(__name__)
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

    weekly_stats_obj.perform_live_update()

    return [
    'Last updated: ' + weekly_stats_obj.get_current_time(),
    'Finishing time: ' + weekly_stats_obj.get_finishing_time(),
    weekly_stats_obj.generate_overall_hours(),
    weekly_stats_obj.generate_weekly_hours()
    ]

@app.callback(Output('hidden-div','children'),[Input('reset-hours','n_clicks')])
def reset_hours(n_clicks):
    
    if n_clicks is None:
        return None

    return weekly_stats_obj.reset_weekly_hours()

if __name__ == '__main__':
    
    app.run_server(debug=True)