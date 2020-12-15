from Tracker import Tracker

import plotly.graph_objs as go
import pandas as pd

class WeeklyTab:

	def __init__(self):

		self._tracker_obj = Tracker()
		self._tracker_obj.update_time_calculations()

	def get_finishing_time(self):
		return self._tracker_obj.get_finishing_time_today()

	def get_current_time(self):
		return self._tracker_obj.get_current_time()

	def get_today_coverage(self):
		return self._tracker_obj.get_today_coverage()

	def perform_live_update(self):
		return self._tracker_obj.perform_live_update()

	def generate_weekly_hours(self):
		"""Generate bar chart for displaying the coverage of the week"""

		tracker_obj = self._tracker_obj

		weekly_stats_df = pd.DataFrame(tracker_obj.get_days_stats())

		weekly_hours_fig = go.Figure(
		    go.Bar(
		        x=weekly_stats_df['minutes_before_noon'],
		        y=weekly_stats_df['day'],
		        orientation='h',
		        name="Before noon (Total Minutes)",
		        customdata=weekly_stats_df['coverage'],
		        marker=dict(color='rgba(246, 78, 139, 0.6)'),
		        texttemplate="%{x}",
		        textposition="inside",
		        textfont_color='white',
		        hoverinfo='none'
		    )
		)

		weekly_hours_fig.add_trace(
			go.Bar(
				x=weekly_stats_df['minutes_after_noon'],
				y=weekly_stats_df['day'],
				orientation='h',
				name="After noon (Total Minutes)",
				customdata=weekly_stats_df['coverage'],
				marker=dict(color='rgba(58, 71, 80, 0.6)'),
				texttemplate="%{x}",
				textposition="inside",
				textfont_color='white',
				hoverinfo='none'
			)
		)

		weekly_hours_fig.update_layout(
		    title_text='Minutes covered (Day by day)',
		    title_x=0.5,
		    xaxis_title='Minutes covered',
		    yaxis=dict(autorange="reversed"),
		    width=750,
		    height=600,
		    xaxis=dict(
		        range=[0,600],
		        tick0=0,
		        dtick=60
		    ),
		    barmode='stack',
		    transition={'duration': 1000, 'easing': 'cubic-in-out'}
		)

		return weekly_hours_fig

	def generate_overall_hours(self):
		"""Generate pie chart showing the total covered and remaining hours"""

		tracker_obj = self._tracker_obj

		total_covered, total_remaining = tracker_obj.get_total_and_remaining()

		total_calculation_df = pd.DataFrame([
		    {
		        'category': 'covered', 
		        'amount': total_covered, 
		        'amount_hrs': tracker_obj.get_hours_minutes(total_covered)
		    },
		    {
		        'category': 'remaining', 
		        'amount': total_remaining,
		        'amount_hrs': tracker_obj.get_hours_minutes(total_remaining)
		    }
		])

		overall_hours_pie_fig = go.Figure(go.Pie(
		    name="",
		    values = total_calculation_df['amount'],
		    labels = total_calculation_df['category'],
		    customdata = total_calculation_df['amount_hrs'],
		    hovertemplate = "Category: %{label} <br>Total(minutes): %{value} </br>Total(hours): %{customdata}"

		))

		overall_hours_pie_fig.update_layout(
			width=400,
			height=600,
			transition={'duration': 1000, 'easing': 'cubic-in-out'}
		)

		return overall_hours_pie_fig