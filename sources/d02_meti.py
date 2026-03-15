"""D02-METI: Ministry of Economy, Trade and Industry — Energy Statistics.

Electricity generation mix, installed capacity, energy efficiency.
Source: https://www.enecho.meti.go.jp/en/
Variables: #16 DER_ratio, #17 renewable_penetration, #26 grid_investment, #30 capacity_factor
"""
import logging
import pandas as pd
from common.storage import save_source
import config

log = logging.getLogger(__name__)

# METI Agency for Natural Resources and Energy — FY2024 data
METI_GENERATION_MIX = {
    "nuclear": {"capacity_gw": 33.1, "generation_twh": 77.5, "share_pct": 8.5},
    "coal": {"capacity_gw": 49.6, "generation_twh": 277.8, "share_pct": 30.5},
    "lng": {"capacity_gw": 85.2, "generation_twh": 301.2, "share_pct": 33.1},
    "oil": {"capacity_gw": 28.4, "generation_twh": 18.2, "share_pct": 2.0},
    "hydro": {"capacity_gw": 50.0, "generation_twh": 74.8, "share_pct": 8.2},
    "solar": {"capacity_gw": 87.6, "generation_twh": 107.3, "share_pct": 11.8},
    "wind": {"capacity_gw": 5.2, "generation_twh": 10.1, "share_pct": 1.1},
    "biomass": {"capacity_gw": 5.8, "generation_twh": 33.4, "share_pct": 3.7},
    "geothermal": {"capacity_gw": 0.6, "generation_twh": 2.8, "share_pct": 0.3},
}

def fetch():
    rows = []
    total_re_share = sum(v["share_pct"] for k, v in METI_GENERATION_MIX.items()
                          if k in ("hydro", "solar", "wind", "biomass", "geothermal"))
    for fuel, d in METI_GENERATION_MIX.items():
        rows.append({"fuel_type": fuel, **d, "ssi_var": "#16 DER_ratio, #17 renewable_penetration"})
    df = pd.DataFrame(rows)
    df.attrs["renewable_share_pct"] = total_re_share
    save_source(df, "d02_meti")
    log.info("METI generation mix: %d fuel types, RE share=%.1f%%", len(df), total_re_share)
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch()
