import plotly.graph_objs as go

class TodayTab:

	def __init__(self, tracker_obj):

		self._tracker_obj = tracker_obj

	def generate_today_remaining_figure(self):

		tracker_obj = self._tracker_obj

		covered_today, balance_today = tracker_obj.find_time_covered_today()

		buffer_name = ''
		buffer_color = ''

		if balance_today > 0:
		    buffer_name = 'remaining'
		    buffer_color = 'rgba(237, 49, 49, 0.6)'
		else:
		    buffer_name = 'overtime'
		    buffer_color = 'rgba(49, 237, 86, 0.6)'
		    balance_today = abs(balance_today)

		today_stat_fig = go.Figure(go.Bar(
		    y=['Today'],
		    x=[covered_today],
		    name='covered',
		    orientation='h',
		    hovertemplate = "Total(minutes): %{x} </br>",
		    marker=dict(
		        color='rgba(246, 78, 139, 0.6)',
		    )
		))

		today_stat_fig.add_trace(go.Bar(
		    y=['Today'],
		    x=[balance_today],
		    name=buffer_name,
		    orientation='h',
		    hovertemplate = "Total(minutes): %{x} </br>",
		    marker=dict(
		        color=buffer_color,
		    )
		))

		today_stat_fig.update_layout(
		    barmode='stack',
		    autosize=False,
		    width=800,
		    height=300
		)

		today_stat_fig.update_yaxes(automargin=True)

		return today_stat_fig