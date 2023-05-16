import holoviews as hv
import numpy as np
import panel as pn


def plot_s2_spindex_hist(event):
    """
    This function shows the Histogram of the computed Sentinel-2 spectral index
    in a FloatPanel on button click.
    Solution by @Hoxbro: https://discourse.holoviz.org/t/how-to-display-a-floatpanel-on-button-click/5346/3
    """

    # Get spectral index data from the cache
    spindex_cache = pn.state.cache["spindex"]

    spindex_name = spindex_cache["name"]
    spindex_array = spindex_cache["np_array"]

    # Remove the masked values
    spindex_array = spindex_array.compressed()

    # Calculates the histogram
    frequencies, edges = np.histogram(spindex_array, 20)

    # Plot the histogram
    spindex_hist = hv.Histogram((edges, frequencies)).opts(
        xlabel=spindex_name, title=f"Histogram of {spindex_name} values"
    )

    # Embed the histogram in a FloatPanel
    float_hist = pn.layout.FloatPanel(
        spindex_hist,
        contained=False,
        position="center",
        margin=20,
    )

    # Show the dialog
    pn.state.cache["placeholder"][:] = [float_hist]
