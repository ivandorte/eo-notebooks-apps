# Sentinel-2 Band Combinations
S2_BAND_COMB = {
    "True Color": ["B04", "B03", "B02"],
    "False Color (Vegetation)": ["B08", "B04", "B03"],
    "False Color (Urban)": ["B12", "B11", "B04"],
    "Short-Wave Infrared": ["B12", "B08", "B04"],
    "Agriculture": ["B11", "B08", "B02"],
    "Geology": ["B12", "B11", "B02"],
    "Healthy Vegetation": ["B08", "B11", "B02"],
    "Snow and Clouds": ["B02", "B11", "B12"],
}

# Sentinel-2 spectral indices
S2_SPINDICES = {
    "NDVI": {
        "name": "NDVI",
        "fullname": "Normalized Difference Vegetation Index",
        "b0": "B08",
        "b1": "B04",
        "cmap": "RdYlGn",
    },
    "NDBI": {
        "name": "NDBI",
        "fullname": "Normalized Difference Built-up Index",
        "b0": "B11",
        "b1": "B08",
        "cmap": "Greys",
    },
    "NDMI": {
        "name": "NDMI",
        "fullname": "Normalized Difference Moisture Index",
        "b0": "B8A",
        "b1": "B11",
        "cmap": "RdYlBu",
    },
    "NDWI": {
        "name": "NDWI",
        "fullname": "Normalized Difference Water Index",
        "b0": "B03",
        "b1": "B08",
        "cmap": "Blues",
    },
}
