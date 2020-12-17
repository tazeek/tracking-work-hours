from WeeklyTab import WeeklyTab

from dash.dependencies import Input, Output
from controller import register_callbacks

import dash
import dash_core_components as dcc
import dash_html_components as html

weekly_stats_obj = WeeklyTab()

def initialize_app():

    overall_hours_fig = weekly_stats_obj.generate_weekly_hours()
    total_hours_fig = weekly_stats_obj.generate_overall_hours()
    weekly_coverage_table = weekly_stats_obj.generate_weekly_coverage()

    finishing_time_str = weekly_stats_obj.get_finishing_time()
    today_coverage_str = weekly_stats_obj.get_today_coverage()
    last_updated_str = weekly_stats_obj.get_current_time()
    
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
                    config={'displayModeBar': False, 'staticPlot': True}
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
register_callbacks(app,weekly_stats_obj)

if __name__ == '__main__':
    
    app.run_server(debug=True)