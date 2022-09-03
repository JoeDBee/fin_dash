from dash import Dash, html
from src.components import dropdown, bar_chart


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className='app-dev',
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                children=[
                    dropdown.render(app)
                ]
            ),
            bar_chart.render(app)
        ],
    )
