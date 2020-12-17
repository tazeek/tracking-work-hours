from WeeklyTab import WeeklyTab

from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html

weekly_stats_obj = WeeklyTab()

def fetch_finishing_time_string():
    return f'Finishing time: {weekly_stats_obj.get_finishing_time()}'

def fetch_today_coverage_string():
    return f'Today\'s coverage: {weekly_stats_obj.get_today_coverage()}'

def fetch_last_updated_string():
    return f'Last updated: {weekly_stats_obj.get_current_time()}'

def initialize_app():

    overall_hours_fig = weekly_stats_obj.generate_weekly_hours()
    total_hours_fig = weekly_stats_obj.generate_overall_hours()
    weekly_coverage_table = weekly_stats_obj.generate_weekly_coverage()

    finishing_time_str = fetch_finishing_time_string()
    today_coverage_str = fetch_today_coverage_string()
    last_updated_str = fetch_last_updated_string()
    
    return html.Div([

        html.Div(id='hidden-div', style={'display':'none'}),

        html.H1(children='Time Tracking Hour Analyzer'),

        html.H4(
            id='finishing-time',
            children=finishing_time_str
        ),

        html.H4(
            id='today-coverage',
            children=today_coverage_str
        ),

        html.H4(
            id='live-update-text',
            children=last_updated_str
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
        fetch_last_updated_string(),
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