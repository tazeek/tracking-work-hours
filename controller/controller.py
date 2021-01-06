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
	def update_live_intervals(n_clicks):
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
			Output('overall-week-hours','figure')],
		[
			Input('reset-hours','submit_n_clicks')
		]
	)
	def reset_hours(submit_n_clicks):
		'''Reset everything to 0 when the reset-hours button is clicked

			Input:
				button event of id: reset-hours

			Output:
				live-update-text: Update the time of new event
				today-coverage: Remove today's coverage
				total-hours-pie: Update the pie chart of hours
				overall-week-hours: Update the bar chart of noon times
		'''
	    
		if not submit_n_clicks:
			raise PreventUpdate

		weekly_stats_obj.reset_weekly_hours()

		return [
			weekly_stats_obj.get_current_time(),
			weekly_stats_obj.get_today_coverage(),
			weekly_stats_obj.generate_overall_hours(),
			weekly_stats_obj.generate_weekly_hours()
		]

	@dcb.callback(
		[
			Output('today-coverage','children'),
			Output('update-coverage','value'),
			Output('update-coverage','children'),
			Output('coverage-table', 'data'),
			Output('input-coverage-hours','value'),
			Output('error-output-update','children')
		],

		[
			Input('update-coverage-dialog','submit_n_clicks')
		],
		[
			State('input-coverage-hours','value'),
			State('update-coverage','value')
		]
	)
	def update_today_coverage(submit_n_clicks, input_value, button_value):

		if not submit_n_clicks:
			raise PreventUpdate

		valid_input = validate_coverage(input_value)

		if not valid_input:
			return [
				no_update, no_update, no_update, no_update,
				None, 
				f'Invalid input: {input_value}'
			]

		new_value = 'continue' if button_value == 'pause' else 'pause'

		weekly_stats_obj.update_today_coverage(input_value)

		return [
			weekly_stats_obj.get_today_coverage(), 
			new_value, 
			new_value.capitalize(),
			weekly_stats_obj.get_records_for_datatable(), 
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