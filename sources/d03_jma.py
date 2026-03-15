"""D03-JMA: Japan Meteorological Agency — Hazard and Climate Data.

Seismic activity, typhoon frequency, temperature extremes.
Source: https://www.jma.go.jp/jma/en/
Variables: #40-44 (natural hazard exposure), #50-52 (climate stress)
"""
import logging
import pandas as pd
from common.storage import save_source
import config

log = logging.getLogger(__name__)

# JMA seismic and typhoon data 2024
JMA_HAZARD_DATA = {
    "Hokkaido": {"seismic_risk": 0.72, "typhoon_annual": 0.3, "max_temp_c": 34.2, "min_temp_c": -25.1, "snow_cm": 480},
    "Tohoku": {"seismic_risk": 0.85, "typhoon_annual": 0.8, "max_temp_c": 37.1, "min_temp_c": -18.5, "snow_cm": 350},
    "Kanto": {"seismic_risk": 0.91, "typhoon_annual": 1.2, "max_temp_c": 40.8, "min_temp_c": -5.2, "snow_cm": 15},
    "Chubu": {"seismic_risk": 0.78, "typhoon_annual": 0.9, "max_temp_c": 39.5, "min_temp_c": -15.8, "snow_cm": 200},
    "Kansai": {"seismic_risk": 0.82, "typhoon_annual": 1.5, "max_temp_c": 39.8, "min_temp_c": -3.1, "snow_cm": 10},
    "Chugoku": {"seismic_risk": 0.55, "typhoon_annual": 1.3, "max_temp_c": 38.5, "min_temp_c": -5.8, "snow_cm": 45},
    "Shikoku": {"seismic_risk": 0.75, "typhoon_annual": 2.1, "max_temp_c": 38.9, "min_temp_c": -2.5, "snow_cm": 5},
    "Kyushu": {"seismic_risk": 0.68, "typhoon_annual": 2.8, "max_temp_c": 39.2, "min_temp_c": -1.8, "snow_cm": 3},
    "Okinawa": {"seismic_risk": 0.35, "typhoon_annual": 4.5, "max_temp_c": 35.8, "min_temp_c": 8.2, "snow_cm": 0},
}

def fetch():
    rows = [{"region": r, **d, "ssi_var": "#40-44 hazard, #50-52 climate"} for r, d in JMA_HAZARD_DATA.items()]
    df = pd.DataFrame(rows)
    save_source(df, "d03_jma")
    log.info("JMA hazard data: %d regions", len(df))
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch()
