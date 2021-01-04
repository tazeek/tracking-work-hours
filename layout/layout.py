import dash_core_components as dcc
import dash_html_components as html

def generate_layout(weekly_stats_obj):

	overall_hours_fig = weekly_stats_obj.generate_weekly_hours()
	total_hours_fig = weekly_stats_obj.generate_overall_hours()
	weekly_coverage_table = weekly_stats_obj.generate_weekly_coverage()

	finishing_time_str = weekly_stats_obj.get_finishing_time()
	today_coverage_str = weekly_stats_obj.get_today_coverage()
	last_updated_str = weekly_stats_obj.get_current_time()

	button_status = 'start' if today_coverage_str[-1] != '-' else 'stop'
    
	return html.Div([

		html.Div(children=[
			html.H1(children='Time Tracking Hour Analyzer', style={'display': 'inline-block'}),

		])

		html.H1(children='Time Tracking Hour Analyzer'),

		html.H4(
			id='finishing-time',
			children=finishing_time_str
		),


		html.H4(
			id='today-coverage',
			children=today_coverage_str
		),

		html.Div(children=[

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

		html.Div(children=[
			html.P(id='error-output-update', style={'color':'red'})
		]),

		html.H4(
			id='live-update-text',
			children=last_updated_str
		),


		dcc.ConfirmDialogProvider(
			children=html.Button(
				'Reset Hours',
			),
			id='reset-hours',
			message='Do you want to reset your overall hours?'
		),

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
		html.Div(id='coverage-table-div', children=[weekly_coverage_table]),

		dcc.Interval(
			id='interval-component',
			interval = 2 * 60 * 1000 # 1000 = 1 second
			)
	])