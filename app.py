import dash
import dash_core_components as dcc
import dash_html_components as html

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

app.layout = html.Div(
    style = {'backgroundColor': colors['background']},
    children = [
        html.H1(
            children="Hello Dash",
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(
            children="Dash: A web application framework for Python",
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(
            id='Graph1',
            figure={
                'data': [
                    {'x': [1,2,3], 'y': [4,1,1], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'}
                ],
                'layout':{
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {'color': colors['text']}
                }
            }
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)