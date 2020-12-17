from WeeklyTab import WeeklyTab

from controller import register_callbacks
from layout import generate_layout

import dash

weekly_stats_obj = WeeklyTab()

app = dash.Dash(__name__)
app.layout = generate_layout(weekly_stats_obj)
register_callbacks(app,weekly_stats_obj)

if __name__ == '__main__':
    
    app.run_server(debug=True)