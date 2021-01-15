import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def _generate_reset_event_modal():

	return dbc.Modal(id='reset-hours-modal', children=[
		dbc.ModalHeader('Reset Weekly Hours'),
		dbc.ModalBody('Do you want to reset your weekly hours?'),
		dbc.ModalFooter([
			dbc.Button('Yes',id='yes-reset'),
			dbc.Button('No',id='no-reset')
		])
	])

def _generate_coverage_modal(weekly_coverage_table):

	return dbc.Modal(id='view-coverage-modal', children=[
		dbc.ModalHeader('Weekly Coverage'),
		dbc.ModalBody(children=[
			html.Div(id='coverage-table-div', children=[weekly_coverage_table])
		]),
		dbc.ModalFooter([
			dbc.Button('Close', id='no-coverage')
		])
	]),

def _generate_reset_view_buttons():

	return html.Div([

		html.Div(
			dbc.Button('View Weekly Coverage', id='view-coverage', color='info'),
			style={'text-align':'center', 'display':'inline-block'}
		),

		html.Div(
			dbc.Button('Reset', id='reset-hours'),
			style={'text-align':'center', 'display':'inline-block'}
		),
	])

def _return_pie_chart_fig(total_hours_fig):

	return dbc.Spinner(
		id='pie-chart-loading',
		color="primary",
		fullscreen=True,
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

def _return_today_coverage_div(today_coverage_str):

	return html.Div([
		html.Strong('Today Coverage: '),
		html.Span(
			id='today-coverage',
			children=today_coverage_str
		)
	])

def _return_finishing_time_div(finishing_time_str):

	return html.Div([

		html.Strong('Finishing time: '),
		html.Span(
			id='finishing-time',
			children=finishing_time_str
		)
	])

def generate_sidebar():

	return html.Div(className='sidebar', children=[

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

		_generate_coverage_modal(),
		_generate_reset_event_modal()
	])