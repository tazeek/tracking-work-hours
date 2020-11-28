import plotly.graph_objs as go
import pandas as pd

class WeeklyTab:

	def __init__(self, tracker_obj):

		self._tracker_obj = tracker_obj

	def generate_weekly_hours(self):

		daily_max_minutes = tracker_obj.get_max_minutes_daily()
		weekly_stats_df = pd.DataFrame(tracker_obj.get_days_stats())
		avg_minutes, avg_str_display = tracker_obj.find_average_time_to_cover()

		weekly_hours_fig = go.Figure(
		    go.Bar(
		        x=days_df['minutes_covered'],
		        y=days_df['day'],
		        orientation='h',
		        name="",
		        customdata=days_df['coverage'],
		        hovertemplate="Total: %{x}<br>Coverage: %{customdata}"
		    )
		)

		weekly_hours_fig.add_shape(
		    dict(
		        type="line",
		        x0=daily_max_minutes,
		        x1=daily_max_minutes,
		        y0=-0.5,
		        y1=4.5,
		        line=dict(
		            color="Red",
		            width=2,
		            dash="dot"
		        )
		    )
		)

		weekly_hours_fig.add_shape(
		    dict(
		        type="line",
		        x0=avg_minutes,
		        x1=avg_minutes,
		        y0=-0.5,
		        y1=4.5,
		        line=dict(
		            color="#FECB52",
		            width=2,
		            dash="dot"
		        )
		    )
		)

		weekly_hours_fig.update_layout(
		    title_text='Weekly hours calculation (Individual Days)',
		    xaxis_title='Minutes covered',
		    yaxis_title='Day',
		    yaxis=dict(autorange="reversed"),
		    width=1000,
		    height=600,
		    xaxis=dict(
		        range=[0,600],
		        tick0=0,
		        dtick=60
		    )
		)

		return weekly_hours_fig