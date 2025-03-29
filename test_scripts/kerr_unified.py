from dataclasses import dataclass, field

import plotly.express as px


@dataclass
class Configuration:
    # Experiment Configuration
    experiment_base_dirs: dict

    # Kerr Plot Configuration
    kerr_plot_config: 'KerrPlotConfig'

    # Data Paths
    processed_hdf_path: str
    output_path: str


@dataclass
class KerrPlotConfig:
    # Main plot configuration
    width: int = 1500
    height: int = 800
    margin: dict = field(default_factory=lambda: dict(l=50, r=50, t=50, b=50))
    show_legend: bool = False

    # Axis configuration
    xaxis_title: str = r'$ \Huge{E^2 \text{ [kV/cm]}} \times 10^3$'
    yaxis_title: str = r'$ \Huge{\Delta n} \times 10^6$'
    plot_border_color: str = 'black'
    plot_border_width: int = 5
    tick_style: dict = field(default_factory=lambda: {
            "inside": True,
            "width": 5,
            "color": "black",
            "length": 10
    })

    # Font configuration
    font_family: str = 'Computer Modern'
    font_size: int = 60
    font_color: str = 'black'

    # Marker/line styling
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    marker_size: int = 25
    marker_symbol: str = 'square'
    marker_border_width: int = 5
    marker_border_color: str = 'black'
    line_width: int = 5

    def get_layout(self):
        """Returns a complete Plotly layout configuration dictionary"""
        base_layout = {
                "plot_bgcolor": 'white',
                "paper_bgcolor": 'white',
                "font": self._get_font_config(),
                "margin": self.margin,
                "width": self.width,
                "height": self.height,
                "showlegend": self.show_legend,
                "legend": self._get_legend_config(),
                "xaxis": self._get_axis_config(self.xaxis_title),
                "yaxis": self._get_axis_config(self.yaxis_title)
        }
        return base_layout

    def _get_font_config(self):
        return {
                'family': self.font_family,
                'size': self.font_size,
                'color': self.font_color
        }

    def _get_axis_config(self, title):
        return {
                'title': title,
                'showline': True,
                'linewidth': self.plot_border_width,
                'linecolor': self.plot_border_color,
                'mirror': True,
                'tickfont': {
                        'size': self.font_size,
                        'family': self.font_family,
                        'color': self.font_color
                },
                "ticks": self.tick_style["inside"] and "inside" or "outside",
                "tickwidth": self.tick_style["width"],
                "tickcolor": self.tick_style["color"],
                "ticklen": self.tick_style["length"]
        }

    def _get_legend_config(self):
        return {
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
