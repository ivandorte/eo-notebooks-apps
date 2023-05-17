import holoviews as hv
import panel as pn
import xarray as xr
from modules.constants import S2_BAND_COMB, S2_SPINDICES
from modules.image_plots import (
    plot_s2_band_comb,
    plot_s2_spindex,
    plot_true_color_image,
)
from modules.image_statistics import plot_s2_spindex_hist

# Load floatpanel extension
pn.extension("floatpanel")

# Disable webgl: https://github.com/holoviz/panel/issues/4855
hv.renderer("bokeh").webgl = False


def create_s2_dashboard():
    """
    This function creates the main dashboard
    """

    # Read the data
    s2_data = xr.open_dataarray("data/s2_data.nc", decode_coords="all")
    s2_data = s2_data.astype("int16")

    # Time variable
    time_var = list(s2_data.indexes["time"])
    time_date = [t.date() for t in time_var]

    # Time Select
    time_opts = dict(zip(time_date, time_var))
    time_select = pn.widgets.Select(name="Time", options=time_opts)

    # Sentinel-2 Band Combinations Select
    s2_band_comb_select = pn.widgets.Select(
        name="Sentinel-2 Band combinations", options=S2_BAND_COMB
    )

    # Sentinel-2 spectral indices ToogleGroup
    tg_title = pn.widgets.StaticText(name="", value="Sentinel-2 spectral indices")
    s2_spindices_tg = pn.widgets.ToggleGroup(
        name="Sentinel-2 indices",
        widget_type="button",
        behavior="radio",
        options=S2_SPINDICES,
    )

    # A StaticText showing the selected band combination
    band_comb_text = pn.widgets.StaticText(
        name="Band Combination", value=", ".join(S2_BAND_COMB["True Color"])
    )

    # Save the StaticText to the cache
    pn.state.cache["band_text"] = band_comb_text

    # Create a placeholder for the FloatPanel
    placeholder = pn.Column(height=0, width=0)

    # Save the placeholder to the cache so that it can be used in the histogram function
    pn.state.cache["placeholder"] = placeholder

    # Histogram button
    show_hist_bt = pn.widgets.Button(name="Show Histogram")
    show_hist_bt.on_click(plot_s2_spindex_hist)

    # Mask clouds Switch
    clm_title = pn.widgets.StaticText(name="", value="Mask clouds?")
    clm_switch = pn.widgets.Switch(name="Switch")

    # Bind image plots
    s2_true_color_bind = pn.bind(
        plot_true_color_image,
        in_data=s2_data,
        time=time_select,
        mask_clouds=clm_switch,
    )

    s2_band_comb_bind = pn.bind(
        plot_s2_band_comb,
        in_data=s2_data,
        time=time_select,
        band_comb=s2_band_comb_select,
        mask_clouds=clm_switch,
    )

    s2_spindex_bind = pn.bind(
        plot_s2_spindex,
        in_data=s2_data,
        time=time_select,
        s2_spindex=s2_spindices_tg,
        mask_clouds=clm_switch,
    )

    # Use the Swipe tool to compare the spectral index with the true color image
    spindex_truecolor_swipe = pn.Swipe(s2_true_color_bind, s2_spindex_bind)

    # Create the main layout
    main_layout = pn.Row(
        pn.Column(s2_band_comb_bind, band_comb_text),
        pn.Column(placeholder, spindex_truecolor_swipe, show_hist_bt),
    )

    # Create the dashboard and turn into a deployable application
    s2_dash = pn.template.FastListTemplate(
        site="",
        title="EO DEMO: Sentinel-2 explorer",
        theme="default",
        main=[main_layout],
        sidebar=[
            time_select,
            s2_band_comb_select,
            tg_title,
            s2_spindices_tg,
            clm_title,
            clm_switch,
        ],
    )

    return s2_dash


if __name__.startswith("bokeh"):
    # Create the dashboard and turn into a deployable application
    s2_dash = create_s2_dashboard()
    s2_dash.servable()
