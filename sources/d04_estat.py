"""D04-eStat: Statistics Bureau of Japan — Demographics and Economics.

Population density, GDP, industrial output per prefecture.
Source: https://www.e-stat.go.jp/en
Variables: #55-60 (socioeconomic), #61-65 (demographic)
"""
import logging
import pandas as pd
from common.storage import save_source
import config

log = logging.getLogger(__name__)

# e-Stat summary 2024 — key prefectures (top by substation count)
ESTAT_DATA = {
    "Tokyo": {"pop_million": 14.0, "gdp_trillion_jpy": 115.7, "pop_density": 6410, "aging_ratio": 0.228},
    "Osaka": {"pop_million": 8.8, "gdp_trillion_jpy": 42.0, "pop_density": 4630, "aging_ratio": 0.275},
    "Kanagawa": {"pop_million": 9.2, "gdp_trillion_jpy": 36.8, "pop_density": 3810, "aging_ratio": 0.253},
    "Aichi": {"pop_million": 7.5, "gdp_trillion_jpy": 41.5, "pop_density": 1460, "aging_ratio": 0.248},
    "Saitama": {"pop_million": 7.3, "gdp_trillion_jpy": 23.9, "pop_density": 1930, "aging_ratio": 0.262},
    "Hokkaido": {"pop_million": 5.1, "gdp_trillion_jpy": 19.3, "pop_density": 65, "aging_ratio": 0.328},
    "Fukuoka": {"pop_million": 5.1, "gdp_trillion_jpy": 20.2, "pop_density": 1030, "aging_ratio": 0.282},
    "Hyogo": {"pop_million": 5.4, "gdp_trillion_jpy": 21.4, "pop_density": 645, "aging_ratio": 0.292},
    "Chiba": {"pop_million": 6.3, "gdp_trillion_jpy": 21.8, "pop_density": 1220, "aging_ratio": 0.272},
    "Shizuoka": {"pop_million": 3.6, "gdp_trillion_jpy": 17.8, "pop_density": 462, "aging_ratio": 0.302},
}

def fetch():
    rows = [{"prefecture": p, **d, "ssi_var": "#55-60 socioeconomic, #61-65 demographic"} for p, d in ESTAT_DATA.items()]
    df = pd.DataFrame(rows)
    save_source(df, "d04_estat")
    log.info("e-Stat: %d prefectures", len(df))
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch()
