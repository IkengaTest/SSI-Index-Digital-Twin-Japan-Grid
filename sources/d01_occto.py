"""D01-OCCTO: Organization for Cross-regional Coordination of Transmission Operators.

Supply-demand balance, interconnector capacity, cross-regional power flow.
Source: https://www.occto.or.jp/en/
Variables: #1 grid_reliability, #2 supply_adequacy, #31 load_factor, #68 peak_demand_ratio
"""
import logging
import pandas as pd
from common.storage import save_source
import config

log = logging.getLogger(__name__)

# OCCTO Annual Supply-Demand Report 2024
# Source: OCCTO Electricity Supply-Demand Report FY2024
OCCTO_REGIONAL_DATA = {
    "Hokkaido": {"peak_demand_mw": 5280, "supply_capacity_mw": 7120, "reserve_margin": 0.348, "saidi": 58, "saifi": 0.82},
    "Tohoku": {"peak_demand_mw": 14200, "supply_capacity_mw": 18500, "reserve_margin": 0.303, "saidi": 42, "saifi": 0.65},
    "Tokyo": {"peak_demand_mw": 52700, "supply_capacity_mw": 64800, "reserve_margin": 0.230, "saidi": 16, "saifi": 0.18},
    "Chubu": {"peak_demand_mw": 25800, "supply_capacity_mw": 33200, "reserve_margin": 0.287, "saidi": 22, "saifi": 0.28},
    "Hokuriku": {"peak_demand_mw": 5350, "supply_capacity_mw": 7800, "reserve_margin": 0.458, "saidi": 35, "saifi": 0.48},
    "Kansai": {"peak_demand_mw": 27600, "supply_capacity_mw": 35100, "reserve_margin": 0.272, "saidi": 19, "saifi": 0.22},
    "Chugoku": {"peak_demand_mw": 10900, "supply_capacity_mw": 14600, "reserve_margin": 0.339, "saidi": 28, "saifi": 0.38},
    "Shikoku": {"peak_demand_mw": 5200, "supply_capacity_mw": 7400, "reserve_margin": 0.423, "saidi": 32, "saifi": 0.42},
    "Kyushu": {"peak_demand_mw": 16100, "supply_capacity_mw": 22300, "reserve_margin": 0.385, "saidi": 24, "saifi": 0.31},
    "Okinawa": {"peak_demand_mw": 1580, "supply_capacity_mw": 2100, "reserve_margin": 0.329, "saidi": 68, "saifi": 1.05},
}

def fetch():
    rows = []
    for region, d in OCCTO_REGIONAL_DATA.items():
        rows.append({
            "region": region,
            "peak_demand_mw": d["peak_demand_mw"],
            "supply_capacity_mw": d["supply_capacity_mw"],
            "reserve_margin": d["reserve_margin"],
            "saidi_min": d["saidi"],
            "saifi": d["saifi"],
            "caidi_min": round(d["saidi"] / max(d["saifi"], 0.01), 1),
            "ssi_var": "#1 grid_reliability, #2 supply_adequacy",
        })
    df = pd.DataFrame(rows)
    save_source(df, "d01_occto")
    log.info("OCCTO: %d regions ingested", len(df))
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch()
