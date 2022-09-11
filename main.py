import i18n
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data
from src.data.source import DataSource

DATA_PATH = "./data/transactions.csv"
LOCALE = "nl"


def main() -> None:
    # Set locale
    i18n.set("locale", LOCALE)
    i18n.load_path.append("locale")

    # load data
    data = load_transaction_data(DATA_PATH, LOCALE)
    data = DataSource(data)

    # run app
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, data)
    app.run()


if __name__ == '__main__':
    main()

