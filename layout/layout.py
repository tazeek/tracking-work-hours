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
}

def _return_update_areas(last_updated_str):

	return html.Div([

		html.Div([
			html.Strong('Last updated: '),
			html.Span(
				id='live-update-text',
				children=last_updated_str
			)
		]),

		html.Br(),

		dbc.Button('Update', id='update-current', outline=True, color='primary',size='sm')
	])

def _return_minutes_comparison_div(overall_hours_fig):

	return html.Div(children=[

		html.Div(className='graph-displayer', children = [
			dcc.Graph(
			id='overall-week-hours',
			figure=overall_hours_fig,
			config={'displayModeBar': False, 'staticPlot': True}
			)
		])
	])

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

		html.Div(
			[	
				_return_finishing_time_div(finishing_time_str),

				html.Hr(),

				_return_today_coverage_div(today_coverage_str),

				html.Br(),

				_return_update_coverage_div(button_status),

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

				html.Div(
					dbc.Button('Reset', id='reset-hours'),
					style={'text-align':'center'}
				),
				
				dbc.Modal(id='reset-hours-modal', children=[
					dbc.ModalHeader('Reset Weekly Hours'),
					dbc.ModalBody('Do you want to reset your weekly hours?'),
					dbc.ModalFooter([
						dbc.Button('Yes',id='yes-reset'),
						dbc.Button('No',id='no-reset')
					])
				])
			],
			style=SIDEBAR_STYLE
		),

		_return_minutes_comparison_div(overall_hours_fig)
	])