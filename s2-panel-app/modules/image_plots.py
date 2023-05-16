import holoviews as hv
import numpy as np
import panel as pn
from bokeh.models import CustomJSHover, HoverTool, WheelZoomTool
from modules.image_processing import s2_contrast_stretch, s2_image_to_uint8

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

    # Check whether to apply a mask to the image
    if mask_clouds:
        # Assign a value of 255 to the pixels representing clouds
        out_data = out_data.where(out_data.mask == 0, 255)

    # Image bands to be plotted
    b0 = out_data.sel(band="B04").data
    b1 = out_data.sel(band="B03").data
    b2 = out_data.sel(band="B02").data

    # Create masked arrays
    b0_mask = np.ma.masked_where(b0 == 255, b0)
    b1_mask = np.ma.masked_where(b1 == 255, b1)
    b2_mask = np.ma.masked_where(b2 == 255, b2)

    # Plot the RGB image
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

    # Check whether to apply a mask to the image
    if mask_clouds:
        # Assign a value of 255 to the pixels representing clouds
        out_data = out_data.where(out_data.mask == 0, 255)

    # Image bands to be plotted
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

    # Check whether to apply a mask to the image
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
