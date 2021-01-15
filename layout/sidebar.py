import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def generate_sidebar():

	return html.Div(className='sidebar', children=[

	])

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

			])