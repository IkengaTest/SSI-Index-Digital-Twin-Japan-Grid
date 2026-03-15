"""D06-ENTSOE: ENTSO-E Transparency Platform (via proxy for JP data).

Cross-border flow equivalent: inter-regional power transfers.
Variables: #32 interconnection_ratio, #33 cross_border_flow
Note: Japan uses OCCTO for inter-regional data; ENTSO-E provides comparison benchmarks.
"""
import logging
import pandas as pd
from common.storage import save_source
import config

log = logging.getLogger(__name__)

# Inter-regional interconnector capacity (OCCTO/METI 2024)
JP_INTERCONNECTORS = {
    "Hokkaido-Tohoku": {"capacity_mw": 900, "flow_avg_mw": 450, "utilization": 0.50},
    "Tohoku-Tokyo": {"capacity_mw": 5500, "flow_avg_mw": 2800, "utilization": 0.51},
    "Tokyo-Chubu": {"capacity_mw": 2100, "flow_avg_mw": 850, "utilization": 0.40},
    "Chubu-Kansai": {"capacity_mw": 3400, "flow_avg_mw": 1200, "utilization": 0.35},
    "Chubu-Hokuriku": {"capacity_mw": 1900, "flow_avg_mw": 600, "utilization": 0.32},
    "Kansai-Chugoku": {"capacity_mw": 4100, "flow_avg_mw": 1500, "utilization": 0.37},
    "Kansai-Shikoku": {"capacity_mw": 1400, "flow_avg_mw": 480, "utilization": 0.34},
    "Chugoku-Kyushu": {"capacity_mw": 2780, "flow_avg_mw": 1100, "utilization": 0.40},
}

def fetch():
    rows = [{"corridor": c, **d, "ssi_var": "#32 interconnection, #33 cross_border"} for c, d in JP_INTERCONNECTORS.items()]
    df = pd.DataFrame(rows)
    save_source(df, "d06_entsoe")
    log.info("JP interconnectors: %d corridors", len(df))
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch()
