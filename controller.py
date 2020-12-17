from dash.dependencies import Output, Input

def register_callbacks(app, weekly_stats_obj):

	@app.callback(
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

	@app.callback(Output('hidden-div','children'),[Input('reset-hours','n_clicks')])
	def reset_hours(n_clicks):
	    
	    if n_clicks is None:
	        return None

	    return weekly_stats_obj.reset_weekly_hours()