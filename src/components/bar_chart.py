import i18n
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids
from ..data.source import DataSource
from ..data.loader import DataSchema


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value")
        ]
    )
    # Note that this function is explicitly used anywhere. There's a bit of Python magic going on in the decorator,
    # which is perhaps not ideal. Useful for a fun application though :)
    def update_bar_chart(years: list[str], months: list[str], categories: list[str]) -> html.Div:
        # similar to above comment, python magic with @nations
        filtered_source = source.filter(years, months, categories)

        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.BAR_CHART)

        fig = px.bar(
            filtered_source.create_pivot_table(),
            x=DataSchema.CATEGORY,
            y=DataSchema.AMOUNT,
            color=DataSchema.CATEGORY,
            labels={
                "category": i18n.t("general.category"),
                "amount": i18n.t("general.amount")
            }
        )
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)

