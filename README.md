# :satellite: EO DEMO: Sentinel-2 explorer

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Description

A simple Panel dashboard exploring all available Sentinel-2 L1C data (2022, max cloud coverage <= 5%) for my small municipality. This dashboard was built to test the new features of the upcoming Panel release.

![img](https://raw.githubusercontent.com/ivandorte/eo-scripts-apps/eo-panel-app/main/images/dashboard.png)

## Data

Sentinel-2 L1C imagery acquired via [sentinelhub-py](https://sentinelhub-py.readthedocs.io) on 2023-05-02.
Copyright: This dashboard contains modified Copernicus Sentinel data (2022)/Sentinel Hub.

## Band combinations & spectral indices

- [sentinelhub: Collection of custom scripts](https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/sentinel-2/)
- [Sentinel 2 Bands and Combinations](https://gisgeography.com/sentinel-2-bands-combinations/)
- [List of band combinations in Sentinel 2](https://giscrack.com/list-of-band-combinations-in-sentinel-2a/)

## Set up
To run this dashboard you will need to do the following steps:

1. Git clone this repository:

`git clone https://github.com/ivandorte/eo-scripts-apps.git`

`cd eo-notebooks-apps/eo-panel-app`

2. Install the required Python packages:

`python -m pip install -r requirements.txt`

3. Run the app

`panel serve app.py --show`

The dashboard will be available in your web browser!!!

## Problems/Questions

- Images axes unlinked when a selector is applied.
- (Swipe) After/before images unlinked when a selector is applied.
- (Swipe) Image Tooltip partially or totally covered when hovering near the slider.
- (FloatPanel) How to show a FloatPanel in the same data app on button click?
- (ToggleGroup) How to show a tootip when hovering over buttons?

## References

- [HoloViz](https://holoviz.org/)

- [Panel](https://pyviz-dev.github.io/panel/reference/index.html)

- [Discourse: Panel 1.0 RC](https://discourse.holoviz.org/t/panel-1-0-release-candidate/5268)

- [Markdown Badges](https://github.com/Ileriayo/markdown-badges)

## Authors

- Ivan D'Ortenzio

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/ivanziogeo)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ivan-d-ortenzio/)