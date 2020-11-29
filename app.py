from WeeklyTab import WeeklyTab
from TodayTab import TodayTab
from Tracker import Tracker

import dash
import dash_core_components as dcc
import dash_html_components as html

def initialize_app(app):

	tracker_obj = Tracker()
	tracker_obj.update_time_calculations()

	weekly_stats_obj = WeeklyTab(tracker_obj)
	today_stats_obj = TodayTab(tracker_obj)
	
	app.layout = html.Div([
    	dcc.Tabs([
    		dcc.Tab(label='Weekly Stats', children=[
    			dcc.Graph(id='overall-week-hours',figure=weekly_stats_obj.generate_weekly_hours()),
    			dcc.Graph(id='total-hours-pie',figure=weekly_stats_obj.generate_overall_hours()),
    			dcc.Graph(id='time-analysis',figure=weekly_stats_obj.generate_noon_comparisons())
    		]),
    		dcc.Tab(label='Today Stats', children=[
    			dcc.Graph(id='today-remaining-hours',figure=today_stats_obj.generate_today_remaining_figure())
    		])
    	])
    ])

if __name__ == '__main__':

    app = dash.Dash()
    initialize_app(app)
    
    app.run_server(debug=True)