"""sources — Data-source plug-ins for SSI Japan Digital-Twin.

Each module in this package should use the @register_source(tier)
decorator from config to register itself for automatic execution.
"""
from sources import d01_occto, d02_meti, d03_jma, d04_estat, d05_osm, d06_entsoe, d07_copernicus
