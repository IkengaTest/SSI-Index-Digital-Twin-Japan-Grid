"""D05-OSM: OpenStreetMap — Substation Geolocation and Grid Topology.

OSM Overpass API for power=substation nodes in Japan.
Source: https://overpass-api.de/
Variables: #7 substation_density, #8 grid_connectivity, #9 spatial_clustering
"""
import logging
import pandas as pd
from data_loader import fetch_json
from common.storage import save_source
import config

log = logging.getLogger(__name__)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
QUERY = '[out:json][timeout:180];area["ISO3166-1"="JP"]->.a;(node["power"="substation"](area.a);way["power"="substation"](area.a););out center;'

def fetch():
    """Fetch substations from OSM Overpass API."""
    try:
        data = fetch_json(OVERPASS_URL, params={"data": QUERY}, use_cache=True)
        elements = data.get("elements", [])
        rows = []
        for e in elements:
            lat = e.get("lat") or e.get("center", {}).get("lat")
            lon = e.get("lon") or e.get("center", {}).get("lon")
            if lat and lon:
                rows.append({
                    "osm_id": e.get("id"),
                    "lat": lat, "lon": lon,
                    "name": e.get("tags", {}).get("name", ""),
                    "voltage": e.get("tags", {}).get("voltage", ""),
                    "operator": e.get("tags", {}).get("operator", ""),
                })
        df = pd.DataFrame(rows)
        save_source(df, "d05_osm")
        log.info("OSM Japan: %d substations", len(df))
        return df
    except Exception as exc:
        log.error("OSM fetch failed: %s", exc)
        return pd.DataFrame()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch()
