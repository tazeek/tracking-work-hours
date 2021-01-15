from layout.sidebar import generate_sidebar

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def _return_header_div(last_updated_str):

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

	return html.Div([
		dbc.Spinner(
			id='loading-chart-comparison',
			color="primary",
			fullscreen=True,
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
	])

def generate_layout(weekly_stats_obj):

	today_coverage_str = weekly_stats_obj.get_today_coverage()

	button_status = None

	if today_coverage_str and today_coverage_str[-1] == '-': 
		button_status = 'pause'
	else:
		button_status = 'start'

	sidebar_dict = {
		'button': button_status,
		'total_hours': weekly_stats_obj.generate_overall_hours(),
		'coverage_table': weekly_stats_obj.generate_weekly_coverage(),
		'finishing_time': weekly_stats_obj.get_finishing_time(),
		'today_coverage': today_coverage_str
	} 
    
	return html.Div([

		html.H1(children='Working Hours Analyzer'),

		_return_header_div(weekly_stats_obj.get_current_time()),

		html.Br(),

		html.Div([

			generate_sidebar(sidebar_dict),
			_return_minutes_comparison_div(weekly_stats_obj.generate_weekly_hours())

		], style={'display':'flex'})	
	])