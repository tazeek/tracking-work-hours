from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.callback import DashCallbackBlueprint

def register_callbacks(app, weekly_stats_obj):

	dcb = DashCallbackBlueprint() 

	@dcb.callback(
		[
			Output('live-update-text','children'),
			Output('total-hours-pie','figure'),
			Output('overall-week-hours','figure')
		],
		[
			Input('interval-component','n_intervals')
		]
	)
	def update_live_intervals(n):

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
		[Input('reset-hours','n_clicks')])
	def reset_hours(n_clicks):
	    
		if n_clicks is None:
			raise PreventUpdate

		weekly_stats_obj.reset_weekly_hours()

		return [
			weekly_stats_obj.get_current_time(),
			weekly_stats_obj.get_today_coverage(),
			weekly_stats_obj.generate_overall_hours(),
			weekly_stats_obj.generate_weekly_hours()
		]

	@dcb.callback(
		[Output('today-coverage','children'),
		Output('update-coverage','value'),
		Output('update-coverage','children')],
		[Input('update-coverage','n_clicks')],
		[State('update-coverage','value')]
	)
	def update_today_coverage(clicks, value):

		if clicks is None:
			raise PreventUpdate

		new_value = 'start' if value == 'stop' else 'stop'

		weekly_stats_obj.update_today_coverage()

		return [weekly_stats_obj.get_today_coverage(), new_value, new_value.capitalize()]

	dcb.register(app)