import plotly.graph_objs as go
import pandas as pd

class WeeklyTab:

	def __init__(self, tracker_obj):

		self._tracker_obj = tracker_obj

	def generate_weekly_hours(self):

		tracker_obj = self._tracker_obj

		daily_max_minutes = tracker_obj.get_max_minutes_daily()
		weekly_stats_df = pd.DataFrame(tracker_obj.get_days_stats())
		avg_minutes, avg_str_display = tracker_obj.find_average_time_to_cover()

		weekly_hours_fig = go.Figure(
		    go.Bar(
		        x=weekly_stats_df['minutes_covered'],
		        y=weekly_stats_df['day'],
		        orientation='h',
		        name="",
		        customdata=weekly_stats_df['coverage'],
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

	def generate_overall_hours(self):

		tracker_obj = self._tracker_obj

		total_covered = tracker_obj.get_total_time_covered()
		remaining_weekly = tracker_obj.get_remaining_weekly()

		total_calculation_df = pd.DataFrame([
		    {
		        'category': 'covered', 
		        'amount': total_covered, 
		        'amount_hrs': tracker_obj.get_hours_minutes(total_covered)
		    },
		    {
		        'category': 'remaining', 
		        'amount': remaining_weekly,
		        'amount_hrs': tracker_obj.get_hours_minutes(remaining_weekly)
		    }
		])

		overall_hours_pie_fig = go.Figure(go.Pie(
		    name="",
		    values = total_calculation_df['amount'],
		    labels = total_calculation_df['category'],
		    customdata = total_calculation_df['amount_hrs'],
		    hovertemplate = "Category: %{label} <br>Total(minutes): %{value} </br>Total(hours): %{customdata}"

		))

		overall_hours_pie_fig.update_layout(title_text='Overall weekly hours calculation: Remaining vs Covered')

		return overall_hours_pie_fig

	def generate_noon_comparisons(self):

		tracker_obj = self._tracker_obj

		time_analysis_dict = {
		    'before_noon': tracker_obj.get_before_noon_minutes(),
		    'after_noon': tracker_obj.get_after_noon_minutes()
		}

		time_analysis_df = pd.DataFrame(time_analysis_dict.items(), columns=['category', 'minutes'])

		time_analysis_fig = go.Figure(go.Bar(
		    name = "",
		    x=time_analysis_df['category'],
		    y=time_analysis_df['minutes'],
		    hovertemplate = "Total(minutes): %{y}"
		    
		))

		# Hours should be 50-50 coverage
		time_analysis_fig.add_shape(
		    dict(
		        type="line",
		        x0=-0.5,
		        x1=1.5,
		        y0=1200, # Half of 40 hours is 20 hours (1200 minutes)
		        y1=1200,
		        line=dict(
		            color="#FECB52",
		            width=2,
		            dash="dot"
		        ),
		))

		return time_analysis_fig 
