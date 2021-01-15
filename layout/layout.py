import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def _return_update_areas(last_updated_str):

	return html.Div([

		html.Div([
			html.Strong('Last updated: '),
			html.Span(
				id='live-update-text',
				children=last_updated_str
			),

			dbc.Button('Update', id='update-current', outline=True, color='primary',size='sm')
		])
	])

def _return_minutes_comparison_div(overall_hours_fig):

	return dbc.Spinner(
		id='loading-chart-comparison',
		children=[
			html.Div(children=[

				html.Div(className='graph-displayer', children = [
					dcc.Graph(
						id='overall-week-hours',
						figure=overall_hours_fig,
						config={'displayModeBar': False, 'staticPlot': True}
					)
				])
			])
		]
	)

def _return_finishing_time_div(finishing_time_str):

	return html.Div([

		html.Strong('Finishing time: '),
		html.Span(
			id='finishing-time',
			children=finishing_time_str
		)
	])

def _return_today_coverage_div(today_coverage_str):

	return html.Div([
		html.Strong('Today Coverage: '),
		html.Span(
			id='today-coverage',
			children=today_coverage_str
		)
	])

def _return_update_coverage_div(button_status):

	return html.Div([

		html.Div(
			dbc.Input(
				id='input-coverage-hours',
				type='text',
				placeholder='HH:MM (Ex. 05:45, 11:45)'
			), 
			style={'display': 'inline-block'}
		),

		dbc.Button(children=button_status.capitalize(), id='update-coverage', outline=True, color='primary')
	])

def _return_pie_chart_fig(total_hours_fig):

	return dbc.Spinner(
		id='pie-chart-loading',
		children=[
			html.Div(className='graph-displayer', children=[
				dcc.Graph(
					id='total-hours-pie',
					figure=total_hours_fig,
					config={'displayModeBar': False}
				)
			])
		]
	)

def generate_layout(weekly_stats_obj):

	overall_hours_fig = weekly_stats_obj.generate_weekly_hours()
	total_hours_fig = weekly_stats_obj.generate_overall_hours()
	weekly_coverage_table = weekly_stats_obj.generate_weekly_coverage()

	finishing_time_str = weekly_stats_obj.get_finishing_time()
	today_coverage_str = weekly_stats_obj.get_today_coverage()
	last_updated_str = weekly_stats_obj.get_current_time()

	button_status = 'start' 

	if today_coverage_str and today_coverage_str[-1] == '-': 
		button_status = 'pause'
    
	return html.Div([

		html.H1(children='Working Hours Analyzer'),

		_return_update_areas(last_updated_str),

		html.Br(),

		html.Div([

			html.Div(className='sidebar', children=[

				_return_finishing_time_div(finishing_time_str),

				html.Hr(),

				_return_today_coverage_div(today_coverage_str),

				html.Br(),

				_return_update_coverage_div(button_status),

				html.Br(),

				html.Div(html.P(id='error-output-update', style={'color':'red'})),

				html.Br(),

				_return_pie_chart_fig(total_hours_fig),

				html.Br(),

				html.Div([

					html.Div(
						dbc.Button('View Weekly Coverage', id='view-coverage', color='info'),
						style={'text-align':'center', 'display':'inline-block'}
					),

					html.Div(
						dbc.Button('Reset', id='reset-hours'),
						style={'text-align':'center', 'display':'inline-block'}
					),
				]),

				dbc.Modal(id='view-coverage-modal', children=[
					dbc.ModalHeader('Weekly Coverage'),
					dbc.ModalBody(children=[
						html.Div(id='coverage-table-div', children=[weekly_coverage_table])
					]),
					dbc.ModalFooter([
						dbc.Button('Close', id='no-coverage')
					])
				]),
				
				dbc.Modal(id='reset-hours-modal', children=[
					dbc.ModalHeader('Reset Weekly Hours'),
					dbc.ModalBody('Do you want to reset your weekly hours?'),
					dbc.ModalFooter([
						dbc.Button('Yes',id='yes-reset'),
						dbc.Button('No',id='no-reset')
					])
				])

			]),

			html.Div([
				_return_minutes_comparison_div(overall_hours_fig)
			]),

		], style={'display':'flex'})	
	])