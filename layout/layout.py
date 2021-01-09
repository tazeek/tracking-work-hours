import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "display": "inline-block"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

def generate_layout(weekly_stats_obj):

	overall_hours_fig = weekly_stats_obj.generate_weekly_hours()
	total_hours_fig = weekly_stats_obj.generate_overall_hours()
	weekly_coverage_table = weekly_stats_obj.generate_weekly_coverage()

	finishing_time_str = weekly_stats_obj.get_finishing_time()
	today_coverage_str = weekly_stats_obj.get_today_coverage()
	last_updated_str = weekly_stats_obj.get_current_time()

	button_status = 'continue' if today_coverage_str[-1] != '-' else 'pause'
    
	return html.Div([

		html.H1(children='Time Tracking Hour Analyzer'),

		html.Div([
			html.Div(
				id='live-update-text',
				children=last_updated_str
			),

			html.Br(),

			dbc.Button('Update', id='update-current', outline=True, color='primary',size='sm')
		]),

		html.Br(),

		html.Div(
			[
				html.Div(
					id='finishing-time',
					children=finishing_time_str
				),

				html.Hr(),

				html.Div(
					id='today-coverage',
					children=today_coverage_str
				),

				html.Br(),

				html.Div([

					html.Div(
						dcc.Input(
							id='input-coverage-hours',
							type='text',
							placeholder='HH:MM (Ex. 05:45, 11:45)'
						), 
						style={'display': 'inline-block'}
					),

					html.Div(
						dcc.ConfirmDialogProvider(
							children=html.Button(
								children=button_status.capitalize(),
								value=button_status,
								id='update-coverage'
							),
							id='update-coverage-dialog',
							message='Do you want to continue to update today\'s coverage?'
						),
						style={'display': 'inline-block'}
					)
				]),

				html.Br(),

				html.Div(children=[
					html.P(id='error-output-update', style={'color':'red'})
				]),

				html.Br(),

				html.Div(className='graph-displayer', children = [
					dcc.Graph(
					id='total-hours-pie',
					figure=total_hours_fig,
					config={'displayModeBar': False}
					)
				]),

				html.Br(),

				html.Div(id='coverage-table-div', children=[weekly_coverage_table]),

				html.Br(),

				dcc.ConfirmDialogProvider(
					children=html.Button(
						'Reset Hours',
					),
					id='reset-hours',
					message='Do you want to reset your overall hours?'
				)
			],
			style=SIDEBAR_STYLE
		),

		html.Div(children=[

			html.Div(className='graph-displayer', children = [
				dcc.Graph(
				id='overall-week-hours',
				figure=overall_hours_fig,
				config={'displayModeBar': False, 'staticPlot': True}
				)
			])
		],
		style=CONTENT_STYLE
		)
	])