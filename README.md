# :satellite: eo-notebook-apps

A collection of Python notebooks and applications related to Earth Observation (EO) sector.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Sentinel-2 notebooks

Python notebooks used to download/process/analyze Sentinel-2 imagery.

* [Download a single Sentinel-2 image (least cloudy acquisitions)](https://github.com/ivandorte/eo-notebooks-apps/blob/main/s2-notebooks/01a_download_single.ipynb)
* [Download all Sentinel-2 images for a year (maxx=5%)](https://github.com/ivandorte/eo-notebooks-apps/blob/main/s2-notebooks/01b_download_multi.ipynb)
* [Download all Sentinel-2 images for a year (maxx=5%) + cloud mask (CLM)](https://github.com/ivandorte/eo-notebooks-apps/blob/main/s2-notebooks/01c_download_multi_clm.ipynb)
* [Write Sentinel-2 images (Tiff) to netcdf](https://github.com/ivandorte/eo-notebooks-apps/blob/main/s2-notebooks/02a_tiff_to_netcdf.ipynb)
* [Write Sentinel-2 images (Tiff) to netcdf + cloud mask (CLM)](https://github.com/ivandorte/eo-notebooks-apps/blob/main/s2-notebooks/02b_tiff_to_netcdf_clm.ipynb)

Link: [s2-notebooks](https://github.com/ivandorte/eo-notebooks-apps/tree/main/s2-notebooks)

## Sentinel-2 explorer (DEMO)

A simple Panel dashboard exploring all available Sentinel-2 L1C data (2022, max cloud coverage <= 5%) for my small municipality. This dashboard was built to test the new features of the upcoming Panel release.

![img](https://github.com/ivandorte/eo-notebooks-apps/blob/main/s2-panel-app/images/dashboard.png)

### Data

Sentinel-2 L1C imagery acquired via [sentinelhub-py](https://sentinelhub-py.readthedocs.io) on 2023-05-02. Copyright: This dashboard contains modified Copernicus Sentinel data (2022)/Sentinel Hub.

### Band combinations & spectral indices

- [sentinelhub: Collection of custom scripts](https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/sentinel-2/)
- [Sentinel 2 Bands and Combinations](https://gisgeography.com/sentinel-2-bands-combinations/)
- [List of band combinations in Sentinel 2](https://giscrack.com/list-of-band-combinations-in-sentinel-2a/)

### ToDo

- [ ] Add an interactive plot that shows the spectral curve of the selected pixel.
- [ ] Add an option to compare the spectral curve of the selected pixel with known spectral profiles (e.g vegetation, soil, water...)

### Set up

To run this dashboard you will need to do the following steps:

1. Git clone this repository:

`git clone git@github.com:ivandorte/eo-notebooks-apps.git`

`cd eo-notebooks-apps/s2-panel-app`

2. Install the required Python packages:

`python -m pip install -r requirements.txt`

3. Run the app

`panel serve app.py --show`

The dashboard will be available in your web browser!!!

Link: [s2-panel-app](https://github.com/ivandorte/eo-notebooks-apps/tree/main/s2-panel-app)

---

### References

- [HoloViz](https://holoviz.org/)

- [Panel](https://pyviz-dev.github.io/panel/reference/index.html)

- [Discourse: Panel 1.0 RC](https://discourse.holoviz.org/t/panel-1-0-release-candidate/5268)

- [Markdown Badges](https://github.com/Ileriayo/markdown-badges)

### Authors

- Ivan D'Ortenzio

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/ivanziogeo)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ivan-d-ortenzio/)
