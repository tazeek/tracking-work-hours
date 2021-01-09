from dash import no_update
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.callback import DashCallbackBlueprint

from src.utility_helper import validate_coverage

def register_callbacks(app, weekly_stats_obj):

	dcb = DashCallbackBlueprint() 

	@dcb.callback(
		[
			Output('live-update-text','children'),
			Output('total-hours-pie','figure'),
			Output('overall-week-hours','figure')
		],
		[
			Input('update-current','n_clicks')
		]
	)
	def update_graphs(n_clicks):
		''' Update the hours whenever the live update button is clicked

			Input:
				button event of id: update-current

			Output:
				live-update-text: Update the time of new event
				total-hours-pie: Update the pie chart of hours
				overall-week-hours: Update the bar chart of noon times
		'''

		weekly_stats_obj.perform_live_update()

		return [
			weekly_stats_obj.get_current_time(),
			weekly_stats_obj.generate_overall_hours(),
			weekly_stats_obj.generate_weekly_hours()
		]

	@dcb.callback(
		[
			Output('live-update-text','children'),
			Output('today-coverage','children'),
			Output('total-hours-pie','figure'),
			Output('overall-week-hours','figure'),
			Output('coverage-table', 'data'),
			Output('update-coverage','children')
		],
		[
			Input('yes-reset','n_clicks')
		]
	)
	def reset_hours(n_clicks):
		'''Reset everything to 0 when the reset-hours button is clicked

			Input:
				button event of id: reset-hours

			Output:
				live-update-text: Update the time of new event
				today-coverage: Remove today's coverage
				total-hours-pie: Update the pie chart of hours
				overall-week-hours: Update the bar chart of noon times
				coverage-table: Update the coverage table
				update-coverage (value): Change value of button to 'start'
				update-coverage (value): change text of button to 'start'
		'''

		if not n_clicks:
			raise PreventUpdate

		weekly_stats_obj.reset_weekly_hours()

		return [
			weekly_stats_obj.get_current_time(),
			weekly_stats_obj.get_today_coverage(),
			weekly_stats_obj.generate_overall_hours(),
			weekly_stats_obj.generate_weekly_hours(),
			weekly_stats_obj.get_records_for_datatable(),
			'start'.capitalize()
		]

	@dcb.callback(
		[
			Output('reset-hours-modal', 'is_open')
		],
		[
			Input('reset-hours','n_clicks'),
			Input('yes-reset','n_clicks'),
			Input('no-reset','n_clicks')
		],
		[
			State('reset-hours-modal', 'is_open')
		]
	)
	def toggle_reset_hours_modal(reset_button_click, confirm_yes, confirm_no, modal_is_open):
		if reset_button_click or confirm_yes or confirm_no:
			return not modal_is_open

		return modal_is_open

	@dcb.callback(
		[
			Output('live-update-text','children'),
			Output('total-hours-pie','figure'),
			Output('today-coverage','children'),
			Output('update-coverage','children'),
			Output('coverage-table', 'data'),
			Output('input-coverage-hours','value'),
			Output('error-output-update','children')
		],

		[
			Input('update-coverage','n_clicks')
		],
		[
			State('input-coverage-hours','value'),
			State('update-coverage','children')
		]
	)
	def update_today_coverage(n_clicks, input_value, button_value):
		'''Update today's coverage, based on the input and event type

			Input:
				Click event of update-coverage-dialog

			State:
				input-coverage-hours: Take the value of text field input-coverage-hours
				update-coverage: Take the state of coverage to (either pause or continue)

			Output:
				today-coverage: Update the current day coverage
				update-coverage (children): Update the button text
				coverage-table: Update the coverage table
				input-coverage-hours: Update the text box field
				error-output-update: Show error message for invalid input

		'''

		if not n_clicks:
			raise PreventUpdate

		valid_input = validate_coverage(input_value)

		if not valid_input:
			return [
				no_update, no_update, no_update, no_update, no_update,
				'', 
				f'Invalid input: {input_value}'
			]

		new_value = 'start' if button_value.lower() == 'pause' else 'pause'

		weekly_stats_obj.update_today_coverage(input_value)

		return [
			weekly_stats_obj.get_current_time(),
			weekly_stats_obj.generate_overall_hours(),
			weekly_stats_obj.get_today_coverage(),
			new_value.capitalize(),
			weekly_stats_obj.get_records_for_datatable(), 
			'',
			None
		]

	@dcb.callback(
		Output('coverage-table', 'data'),
		[
			Input('coverage-table', 'data_timestamp')
		],
		State('coverage-table','data')
	)
	def update_table(time_stamp, coverage_data):

		if time_stamp is None:
			raise PreventUpdate

		weekly_stats_obj.update_overall_coverage_table(coverage_data)

		return weekly_stats_obj.get_dataframe_for_datatable()



	dcb.register(app)