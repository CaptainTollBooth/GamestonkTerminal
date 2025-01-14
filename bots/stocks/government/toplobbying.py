import pandas as pd
from matplotlib import pyplot as plt

import bots.config_discordbot as cfg
from bots.config_discordbot import logger
from bots.helpers import image_border
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.helper_funcs import plot_autoscale
from gamestonk_terminal.stocks.government import quiverquant_model


def toplobbying_command(num: int = 10, raw: bool = False):
    """Displays top lobbying firms [quiverquant.com]"""
    # Debug user input
    if cfg.DEBUG:
        logger.debug("gov-toplobbying %s %s", num, raw)

    # Retrieve Data
    df_lobbying = quiverquant_model.get_government_trading("corporate-lobbying")

    if df_lobbying.empty:
        raise Exception("No corporate lobbying found")

    df_lobbying["Amount"] = df_lobbying.Amount.astype(float).fillna(0) / 100_000

    lobbying_by_ticker = pd.DataFrame(
        df_lobbying.groupby("Ticker")["Amount"].agg("sum")
    ).sort_values(by="Amount", ascending=False)
    fig, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    lobbying_by_ticker.head(num).plot(kind="bar", ax=ax)
    ax.set_xlabel("Ticker")
    ax.set_ylabel("Total Amount ($100k)")
    ax.set_title(f"Corporate Lobbying Spent since {df_lobbying['Date'].min()}")
    fig.tight_layout()

    plt.savefig("ta_toplobbying.png")
    imagefile = "ta_toplobbying.png"

    imagefile = image_border(imagefile)
    return {
        "title": "Stocks: [quiverquant.com] Top Lobbying Firms",
        "imagefile": imagefile,
    }
