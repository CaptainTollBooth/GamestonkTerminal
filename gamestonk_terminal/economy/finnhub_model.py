import logging

import pandas as pd
import requests

from gamestonk_terminal import config_terminal as cfg
from gamestonk_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_economy_calendar_events() -> pd.DataFrame:
    """Get economic calendar events

    Returns
    -------
    pd.DataFrame
        Get dataframe with economic calendar events
    """
    response = requests.get(
        f"https://finnhub.io/api/v1/calendar/economic?token={cfg.API_FINNHUB_KEY}"
    )
    if response.status_code == 200:
        d_data = response.json()
        if "economicCalendar" in d_data:
            return pd.DataFrame(d_data["economicCalendar"])

    return pd.DataFrame()
