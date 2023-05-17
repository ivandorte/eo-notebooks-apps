import holoviews as hv
import numpy as np
import panel as pn
from bokeh.models import WheelZoomTool
from bokeh.models.formatters import NumeralTickFormatter


def plot_s2_spindex_hist(event):
    """
    This function shows the Histogram of the computed Sentinel-2 spectral index
    in a FloatPanel on button click.
    Solution by @Hoxbro: https://discourse.holoviz.org/t/how-to-display-a-floatpanel-on-button-click/5346/3
    """

    def hook(plot, element):
        """
        Custom hook for disabling zoom on axis
        """

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

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
        xlabel=spindex_name,
        yformatter=NumeralTickFormatter(format="0a"),
        title=f"Histogram of {spindex_name} values",
        hooks=[hook],
        width=400,
        height=400,
    )

    # https://jspanel.de/#options
    config = {
        "resizeit": {"disable": "true"},
        "headerControls": "closeonly",
        "closeOnEscape": "true",
    }

    # Embed the histogram in a FloatPanel
    float_hist = pn.layout.FloatPanel(
        spindex_hist, contained=False, position="center", margin=20, config=config
    )

    # Show the dialog
    pn.state.cache["placeholder"][:] = [float_hist]
