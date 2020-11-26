from Tracker import Tracker

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

tracker_obj = Tracker()
tracker_obj.update_time_calculations()

daily_max_minutes = tracker_obj.get_max_minutes_daily()
days_df = pd.DataFrame(tracker_obj.get_days_stats())
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

app.layout = html.Div([
    dcc.Graph(id='overall-week-hours',figure=weekly_hours_fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)