from dataclasses import dataclass, field

import numpy as np
import plotly.express as px


@dataclass
class PlotConfig:
    plot_title: str = ""
    xaxis_title: str = ""
    yaxis_title: str = ""
    extra_yaxis_titles: dict = field(default_factory=dict)
    smoothing_sigma: int = 5
    colors: dict = field(default_factory=lambda: {"ch_1": "blue", "ch_2": "red"})
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    plot_options: dict = field(default_factory=lambda: {
            "font": {
                    "family": 'Latin Modern',  # Use EC-compatible font
                    "size": 60,
                    "color": 'black'
            },
            "plot_bgcolor": 'white',
            "xaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern"},  # EC Font
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            },
            "yaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern", "color": 'black'},
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            }
    })

    def get_layout(self):
        return {
                "plot_bgcolor": self.plot_options["plot_bgcolor"],
                "paper_bgcolor": "white",
                "font": self.plot_options["font"],
                "margin": dict(l=10, r=10, t=50, b=50),
                "width": 1280,
                "height": 720,
                "legend": {
                        "x": 0.85,
                        "y": 0.3,
                        "bgcolor": "white",
                        "bordercolor": "black",
                        "font": {
                                "size": 40,
                                "family": "Latin Modern",
                                "color": "black"
                        }
                }
        }

    def get_axes_options(self):
        axes = {
                "xaxis": {"title": self.xaxis_title, **self.plot_options["xaxis"]},
                "yaxis": {"title": self.yaxis_title, **self.plot_options["yaxis"]},
        }
        for key, title in self.extra_yaxis_titles.items():
            axes[key] = {"title": title, **self.plot_options["yaxis"]}
        return axes


@dataclass
class RegPlotConfig:
    plot_title: str = ""
    xaxis_title: str = ""
    yaxis_title: str = ""
    extra_yaxis_titles: dict = field(default_factory=dict)
    smoothing_sigma: int = 5
    colors: dict = field(default_factory=lambda: {"ch_1": "blue", "ch_2": "red"})
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    plot_options: dict = field(default_factory=lambda: {
            "font": {
                    "family": 'Latin Modern',  # Use EC-compatible font
                    "size": 60,
                    "color": 'black'
            },
            "plot_bgcolor": 'white',
            "xaxis": {
                    "range": [0, 60],
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern"},  # EC Font
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            },
            "yaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "showticklabels": True,
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern", "color": 'black'},
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            }
    })

    def get_layout(self):
        return {
                "plot_bgcolor": self.plot_options["plot_bgcolor"],
                "paper_bgcolor": "white",
                "font": self.plot_options["font"],
                "margin": dict(l=10, r=10, t=50, b=50),
                "width": 1280,
                "height": 720,
                "legend": {
                        "x": 0.85,
                        "y": 0.3,
                        "bgcolor": "white",
                        "bordercolor": "black",
                        "font": {
                                "size": 40,
                                "family": "Latin Modern",
                                "color": "black"
                        }
                }
        }

    def get_axes_options(self):
        axes = {
                "xaxis": {"title": self.xaxis_title, **self.plot_options["xaxis"]},
                "yaxis": {"title": self.yaxis_title, **self.plot_options["yaxis"]},
        }
        for key, title in self.extra_yaxis_titles.items():
            axes[key] = {"title": title, **self.plot_options["yaxis"]}
        return axes


@dataclass
class ScatterPlotConfig(PlotConfig):
    marker_size: int = 30  # Default marker size for scatter plots
    line_width: int = 5  # Default line width for connections between points (if desired)
    marker_color: str = "blue"  # Default marker color
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)  # Color scale for markers
    plot_bgcolor: str = 'white'  # Background color
    grid_color: str = 'lightgray'  # Color of the grid lines
    show_legend: bool = True  # Option to show or hide the legend
    show_hover: bool = True  # Option to show hover text

    plot_options: dict = field(default_factory=lambda: {
            "font": {
                    "family": 'Latin Modern',  # Use EC-compatible font
                    "size": 60,
                    "color": 'black'
            },
            "plot_bgcolor": 'white',  # Background color of the plot
            "paper_bgcolor": "white",  # Background color of the paper
            "xaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern"},  # EC Font
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            },
            "yaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern", "color": 'black'},
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            },
            "grid": {
                    "showgrid": True,
                    "gridcolor": 'lightgray',  # Grid lines color
                    "gridwidth": 0.5  # Grid line width
            },
            "legend": {
                    "x": 0.85,
                    "y": 0.3,
                    "bgcolor": "white",
                    "bordercolor": "black",
                    "font": {
                            "size": 40,
                            "family": "Latin Modern",
                            "color": "black"
                    }
            }
    })

    def get_layout(self):
        return {
                "plot_bgcolor": self.plot_options["plot_bgcolor"],
                "paper_bgcolor": self.plot_options["paper_bgcolor"],
                "font": self.plot_options["font"],
                "margin": dict(l=10, r=10, t=50, b=50),
                "width": 1280,
                "height": 720,
                "showlegend": self.show_legend,
                "xaxis": {
                        **self.plot_options["xaxis"],
                        "gridcolor": self.plot_options["grid"]["gridcolor"],
                        "showgrid": self.plot_options["grid"]["showgrid"]
                },
                "yaxis": {
                        **self.plot_options["yaxis"],
                        "gridcolor": self.plot_options["grid"]["gridcolor"],
                        "showgrid": self.plot_options["grid"]["showgrid"]
                },
                "legend": self.plot_options["legend"]
        }

    def get_axes_options(self):
        axes = {
                "xaxis": {"title": self.xaxis_title, **self.plot_options["xaxis"]},
                "yaxis": {"title": self.yaxis_title, **self.plot_options["yaxis"]},
        }
        for key, title in self.extra_yaxis_titles.items():
            axes[key] = {"title": title, **self.plot_options["yaxis"]}
        return axes

@ dataclass
class LogPlotConfig:
    plot_title: str = ""
    xaxis_title: str = ""
    yaxis_title: str = ""
    extra_yaxis_titles: dict = field(default_factory=dict)
    smoothing_sigma: int = 5
    colors: dict = field(default_factory=lambda: {"ch_1": "blue", "ch_2": "red"})
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    log_range: tuple = (-5, 0)
    num_ticks: int = 6
    num_minor_ticks: int = 4  # Number of minor ticks per decade

    plot_options: dict = field(default_factory=lambda: {
            "font": {
                    "family": 'Latin Modern',
                    "size": 60,
                    "color": 'black'
            },
            "plot_bgcolor": 'white',
            "xaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern"},
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            },
            "yaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern", "color": 'black'},
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            }
    })

    def get_layout(self) -> dict:
        """Returns a customized layout configuration for logarithmic plots."""
        return {"plot_bgcolor": self.plot_options["plot_bgcolor"],
                "paper_bgcolor": "white",
                "font": self.plot_options["font"],
                "margin": dict(l=10, r=10, t=50, b=50),
                "width": 1280,
                "height": 720,
                "legend": {
                        "x": 0.85,
                        "y": 0.3,
                        "bgcolor": "white",
                        "bordercolor": "black",
                        "font": {
                                "family": "Latin Modern",
                                "color": "black"
                        }
                }
                }

    def get_axes_options(self):
        """Returns axes options, ensuring a logarithmic y-axis with minor ticks."""
        log_ticks = np.logspace(self.log_range[0], self.log_range[1], num=self.num_ticks)
        log_labels = [f"10<sup>{int(np.log10(tick))}</sup>" for tick in log_ticks]

        minor_ticks = []
        for i in range(self.log_range[0], self.log_range[1]):
            minor_ticks.extend(np.logspace(i, i + 1, num=self.num_minor_ticks + 2)[1:-1])

        axes = {
                "xaxis": {"title": self.xaxis_title, **self.plot_options["xaxis"]},
                "yaxis": {
                        "type": "log",
                        "tickvals": log_ticks.tolist(),
                        "ticktext": log_labels,
                        "range": list(self.log_range),
                        "title": self.yaxis_title,
                        "minor": {
                                "tickvals": np.array(minor_ticks).tolist(),
                                "tickwidth": 1,
                                "tickcolor": "black",
                                "ticklen": 5,
                                "ticks": "inside"
                        },
                        **self.plot_options["yaxis"]
                }
        }
        for key, title in self.extra_yaxis_titles.items():
            axes[key] = {"title": title, **self.plot_options["yaxis"]}
        return axes


@dataclass
class PlotConfigBoth:
    plot_title: str = ""
    xaxis_title: str = ""
    yaxis_title: str = ""
    extra_yaxis_titles: dict = field(default_factory=dict)
    smoothing_sigma: int = 5
    colors: dict = field(default_factory=lambda: {"ch_1": "blue", "ch_2": "red"})
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    plot_options: dict = field(default_factory=lambda: {
            "font": {
                    "family": 'Latin Modern',  # Use EC-compatible font
                    "size": 60,
                    "color": 'black'
            },
            "plot_bgcolor": 'white',
            "xaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern"},  # EC Font
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            },
            "yaxis": {
                    "showline": True,
                    "linewidth": 3,
                    "linecolor": 'black',
                    "mirror": True,
                    "tickfont": {"size": 60, "family": "Latin Modern", "color": 'black'},
                    "ticks": "inside",
                    "tickwidth": 5,
                    "tickcolor": "black",
                    "ticklen": 10
            }
    })

    def get_layout(self):
        return {
                "plot_bgcolor": self.plot_options["plot_bgcolor"],
                "paper_bgcolor": "white",
                "font": self.plot_options["font"],
                "margin": dict(l=10, r=10, t=50, b=50),
                "width": 1280,
                "height": 720,
                "legend": {
                        "x": 0.85,
                        "y": 0.3,
                        "bgcolor": "white",
                        "bordercolor": "black",
                        "font": {
                                "size": 40,
                                "family": "Latin Modern",
                                "color": "black"
                        }
                }
        }

    def get_axes_options(self):
        axes = {
                "xaxis": {"title": self.xaxis_title, **self.plot_options["xaxis"]},
                "yaxis": {"title": self.yaxis_title, **self.plot_options["yaxis"]},
                "xaxis2": {  # Adding the inverted top x-axis
                        "overlaying": "x",
                        "side": "top",
                        "autorange": "reversed",
                        "showline": True,
                        "linewidth": 3,
                        "linecolor": 'black',
                        "mirror": True,
                        "tickfont": {"size": 60, "family": "Latin Modern"},
                        "ticks": "inside",
                        "tickwidth": 5,
                        "tickcolor": "black",
                        "ticklen": 10
                }
        }

        for key, title in self.extra_yaxis_titles.items():
            axes[key] = {"title": title, **self.plot_options["yaxis"]}

        return axes