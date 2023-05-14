import holoviews as hv
import numpy as np
import panel as pn
import xarray as xr
from bokeh.models import CustomJSHover, HoverTool, WheelZoomTool
from skimage import exposure

pn.extension()

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

# This function hide the tooltip when the pixel value is NaN
HIDE_NAN_HOVTOOL = CustomJSHover(
    code="""
    var value;
    var tooltips = document.getElementsByClassName("bk-tooltip");
    if (isNaN(value)) {
        tooltips[0].hidden=true;
    } else {
        tooltips[0].hidden=false;
    }
        return value;
    """
)


def s2_image_to_uint8(in_data):
    """
    A function that converts image DN to Reflectance (0, 1) and
    then rescale to uint8 (0-255).
    https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l1c/
    """

    # Convert to reflectance and uint8 (range: 0-255)
    quant_value = 1e4
    out_data = (in_data / quant_value * 255).astype("uint8")
    out_data = out_data.clip(0, 255)

    return out_data


def s2_contrast_stretch(in_data):
    """
    Image enhancement: Contrast stretching.
    """

    p2, p98 = np.percentile(in_data, (2.5, 97.5))
    out_data = exposure.rescale_intensity(in_data, in_range=(p2, p98))

    return out_data


def plot_true_color_image(in_data, time, mask_clouds):
    """
    A function that plots the True Color band combination.
    """

    def hook(plot, element):
        """
        Custom hook for disabling x/y tick lines/labels
        """
        plot.state.xaxis.major_tick_line_color = None
        plot.state.xaxis.minor_tick_line_color = None
        plot.state.xaxis.major_label_text_font_size = "0pt"
        plot.state.yaxis.major_tick_line_color = None
        plot.state.yaxis.minor_tick_line_color = None
        plot.state.yaxis.major_label_text_font_size = "0pt"

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

    # Get the selected image and band combination
    out_data = in_data.sel(band=["B04", "B03", "B02"], time=time)

    # Convert the image to uint8
    out_data.data = s2_image_to_uint8(out_data.data)

    # Contrast stretching
    out_data.data = s2_contrast_stretch(out_data.data)

    if mask_clouds:
        # Assign a value of 255 to the pixels representing clouds
        out_data = out_data.where(out_data.mask == 0, 255)

    b0 = out_data.sel(band="B04").data
    b1 = out_data.sel(band="B03").data
    b2 = out_data.sel(band="B02").data

    # Create masked arrays
    b0_mask = np.ma.masked_where(b0 == 255, b0)
    b1_mask = np.ma.masked_where(b1 == 255, b1)
    b2_mask = np.ma.masked_where(b2 == 255, b2)

    # Plot the image
    plot_data = dict(
        x=out_data["x"],
        y=out_data["y"],
        r=b0_mask,
        g=b1_mask,
        b=b2_mask,
    )

    the_plot = hv.RGB(
        data=plot_data,
        kdims=["x", "y"],
        vdims=list("rgb"),
    ).opts(
        xlabel="",
        ylabel="",
        hooks=[hook],
        frame_width=500,
        frame_height=500,
    )

    return the_plot


def get_band_comb_text(band_comb):
    """
    A function that return a StaticText showing
    the selected band combination.
    """

    band_comb_text = pn.widgets.StaticText(
        name="Band Combination", value=", ".join(band_comb)
    )

    return band_comb_text


def plot_s2_band_comb(in_data, time, band_comb, mask_clouds):
    """
    A function that plots the selected band combination.
    """

    def hook(plot, element):
        """
        Custom hook for disabling x/y tick lines/labels
        """
        plot.state.xaxis.major_tick_line_color = None
        plot.state.xaxis.minor_tick_line_color = None
        plot.state.xaxis.major_label_text_font_size = "0pt"
        plot.state.yaxis.major_tick_line_color = None
        plot.state.yaxis.minor_tick_line_color = None
        plot.state.yaxis.major_label_text_font_size = "0pt"

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

    # Get the selected image and band combination
    out_data = in_data.sel(band=band_comb, time=time)

    # Convert the image to uint8
    out_data.data = s2_image_to_uint8(out_data.data)

    # Contrast stretching
    out_data.data = s2_contrast_stretch(out_data.data)

    if mask_clouds:
        # Assign a value of 255 to the pixels representing clouds
        out_data = out_data.where(out_data.mask == 0, 255)

    b0 = out_data.sel(band=band_comb[0]).data
    b1 = out_data.sel(band=band_comb[1]).data
    b2 = out_data.sel(band=band_comb[2]).data

    # Create masked arrays
    b0_mask = np.ma.masked_where(b0 == 255, b0)
    b1_mask = np.ma.masked_where(b1 == 255, b1)
    b2_mask = np.ma.masked_where(b2 == 255, b2)

    # Plot the image
    plot_data = dict(
        x=out_data["x"],
        y=out_data["y"],
        r=b0_mask,
        g=b1_mask,
        b=b2_mask,
    )

    the_plot = hv.RGB(
        data=plot_data,
        kdims=["x", "y"],
        vdims=list("rgb"),
    ).opts(
        xlabel="",
        ylabel="",
        hooks=[hook],
        frame_width=500,
        frame_height=500,
    )

    return the_plot


def assign_spindex_to_cache(s2_spindex_name, spindex):
    """
    This function assign the spectral index array to the panel state cache
    so that it can be used for the histogram floatpanel widget.
    """
    pn.state.cache["spindex"] = {"name": s2_spindex_name, "np_array": spindex}


def plot_s2_spindex(in_data, time, s2_spindex, mask_clouds):
    """
    A function that plots the selected Sentinel-2 spectral index.
    """

    def hook(plot, element):
        """
        Custom hook for disabling x/y tick lines/labels
        """
        plot.state.xaxis.major_tick_line_color = None
        plot.state.xaxis.minor_tick_line_color = None
        plot.state.xaxis.major_label_text_font_size = "0pt"
        plot.state.yaxis.major_tick_line_color = None
        plot.state.yaxis.minor_tick_line_color = None
        plot.state.yaxis.major_label_text_font_size = "0pt"

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

    # Get the selected image
    out_data = in_data.sel(time=time)

    # Get the name of the selected spectral index
    s2_spindex_name = s2_spindex["name"]

    # Define a custom Hover tool for the image
    spindex_hover = HoverTool(
        tooltips=[(f"{s2_spindex_name}", "@image")],
        formatters={"@image": HIDE_NAN_HOVTOOL},
    )

    # Calculate the selected spectral index
    b0 = out_data.sel(band=s2_spindex["b0"]).data
    b1 = out_data.sel(band=s2_spindex["b1"]).data
    plot_data = (b0 - b1) / (b0 + b1)

    if mask_clouds:
        # Assign a value of 255 to the pixels representing clouds
        plot_data[out_data.mask == 1] = 255

    # Create a masked array
    plot_data_mask = np.ma.masked_where(plot_data == 255, plot_data)

    # Assign this array to the pn.cache
    assign_spindex_to_cache(s2_spindex_name, plot_data_mask)

    # Plot the computed spectral index
    the_plot = hv.Image((out_data["x"], out_data["y"], plot_data_mask)).opts(
        xlabel="",
        ylabel="",
        cmap=s2_spindex["cmap"],
        hooks=[hook],
        tools=[spindex_hover],
        frame_width=500,
        frame_height=500,
    )

    # Get the True Color Image
    true_color = plot_true_color_image(in_data, time, mask_clouds)

    return pn.Swipe(true_color, the_plot)


def plot_s2_spindex_hist(event):
    """
    TODO: Show the Histogram of the Sentinel-2 spectral index
    in a FloatPanel on button click.
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
        title=f"Histogram of {spindex_name} values"
    )

    # Embed the histogram in a FloatPanel
    float_hist = pn.layout.FloatPanel(
        spindex_hist,
        name="",
        position="center",
        width=400,
        height=400,
        margin=20,
    )

    # How to show this dialog on button click?
    return pn.Column(float_hist).servable()


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

    # Histogram button
    show_hist_bt = pn.widgets.Button(name="Show Histogram")
    show_hist_bt.on_click(plot_s2_spindex_hist)

    # Mask clouds Switch
    swt_title = pn.widgets.StaticText(name="", value="Mask clouds?")
    clm_switch = pn.widgets.Switch(name="Switch")

    # Bind plots to the selectors
    s2_band_comb_text_bind = pn.bind(
        get_band_comb_text,
        band_comb=s2_band_comb_select,
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

    main_layout = pn.Row(
        pn.Column(s2_band_comb_bind, s2_band_comb_text_bind),
        pn.Column(s2_spindex_bind, show_hist_bt),
    )

    # Turn into a deployable application
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
            swt_title,
            clm_switch,
        ],
    )

    return s2_dash


if __name__.startswith("bokeh"):
    # Create the dashboard and turn into a deployable application
    s2_dash = create_s2_dashboard()
    s2_dash.servable()
