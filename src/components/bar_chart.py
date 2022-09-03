import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


from . import ids

MEDAL_DATA = px.data.medals_long()


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.NATION_DROPDOWN, "value")
    )
    # Note that this function is explicitly used anywhere. There's a bit of Python magic going on in the decorator,
    # which is perhaps not ideal. Useful for a fun application though :)
    def update_bar_chart(nations: list[str]) -> html.Div:
        filtered_data = MEDAL_DATA.query("nation in @nations") # similar to above comment, python magic with @nations

        if not filtered_data.shape[0]:
            return html.Div("No data selected :(")
        fig = px.bar(filtered_data, x="medal", y="count", color="nation", text="nation")
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)

