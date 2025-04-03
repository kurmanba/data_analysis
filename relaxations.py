import sys
from dataclasses import dataclass, field

import h5py
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pylab import mpl
# from tabulate import tabulate
import plotly.io as pio

if sys.platform == "darwin":
    mpl.use("macosx")


@dataclass
class Configuration:
    kerr_plot_width: int = 1500
    kerr_plot_height: int = 800
    kerr_plot_margin: dict = field(default_factory=lambda: dict(l=50, r=50, t=50, b=50))
    show_legend: bool = True

    xaxis_title: str = r'$ \Huge{E^2 \text{ [}V^2/cm^2\text{]} \times 10^{-3} } $'
    yaxis_title: str = r'$ \Huge{D_r \, [\mathrm{rad}^2/\mathrm{s}]} $'
    plot_border_color: str = 'black'
    plot_border_width: int = 5
    tick_style: dict = field(default_factory=lambda: {
            "inside": True,
            "width": 5,
            "color": "black",
            "length": 10
    })

    font_family: str = 'Computer Modern'
    font_size: int = 60
    font_color: str = 'black'

    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    marker_size: int = 15
    marker_symbol: str = 'circle'
    marker_border_width: int = 2
    marker_border_color: str = 'black'
    line_width: int = 5

    experiment_base_dirs: dict = field(default_factory=lambda: {
            'database': "/Users/alisher/IdeaProjects/TEB_REMAKE/databases",
            'figures': "/Users/alisher/IdeaProjects/TEB_REMAKE/figures"
    })

    def get_kerr_plot_layout(self):
        """Returns a complete Plotly layout configuration dictionary for Kerr plot."""
        base_layout = {
                "plot_bgcolor": 'white',
                "paper_bgcolor": 'white',
                "font": self._get_font_config(),
                "margin": self.kerr_plot_margin,
                "width": self.kerr_plot_width,
                "height": self.kerr_plot_height,
                "showlegend": self.show_legend,
                "legend": dict(
                        x=0.02,  # Position in the upper left
                        y=0.98,
                        font=dict(
                                size=24,
                                family=self.font_family,
                                color=self.font_color
                        ),
                        bgcolor='rgba(255,255,255,0.7)',
                        bordercolor='black',
                        borderwidth=1
                ),
                "xaxis": self._get_axis_config(self.xaxis_title),
                "yaxis": self._get_axis_config(self.yaxis_title)
        }
        base_layout["yaxis"].update({"range": [0, None]})
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
                "ticks": "inside" if self.tick_style["inside"] else "outside",
                "tickwidth": self.tick_style["width"],
                "tickcolor": self.tick_style["color"],
                "ticklen": self.tick_style["length"]
        }


def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def load_group_data(group):
    e_squared, dn_infinity = [], []
    rise_c1, rise_c2, rise_d, fall_c1, fall_d = [], [], [], [], []

    for filename in group:
        dataset = group[filename]
        if "e_square" in dataset:
            e_squared.append(np.array(dataset["e_square"]))
        if "dn_infinity" in dataset:
            dn_infinity.append(np.array(dataset["dn_infinity"]))
        if "Rise_c1" in dataset:
            rise_c1.append(np.array(dataset["Rise_c1"]))
        if "Rise_c2" in dataset:
            rise_c2.append(np.array(dataset["Rise_c2"]))
        if "Rise_D" in dataset:
            rise_d.append(np.array(dataset["Rise_D"]))
        if "Fall_c1" in dataset:
            fall_c1.append(np.array(dataset["Fall_c1"]))
        if "Fall_D" in dataset:
            fall_d.append(np.array(dataset["Fall_D"]))

    if not e_squared or not dn_infinity:
        return None, None, None, None, None, None, None, None, None

    e_squared = np.array(e_squared).flatten()
    dn_infinity = np.array(dn_infinity).flatten()
    rise_c1 = np.array(rise_c1).flatten()
    rise_c2 = np.array(rise_c2).flatten()
    rise_d = np.array(rise_d).flatten()
    fall_c1 = np.array(fall_c1).flatten()
    fall_d = np.array(fall_d).flatten()

    if e_squared.size == 0 or dn_infinity.size == 0:
        return None, None, None, None, None, None, None, None, None

    sort_idx = np.argsort(e_squared)
    return (e_squared[sort_idx], dn_infinity[sort_idx], rise_c1[sort_idx],
            rise_c2[sort_idx], rise_d[sort_idx], fall_c1[sort_idx], fall_d[sort_idx])


def plot_all_kerr_data(concentrations, pulses):
    config = Configuration()
    processed_hdf_path = '/Users/alisher/IdeaProjects/TEB_REMAKE/databases/processed_experiment_data.h5'
    output_path ='/Users/alisher/IdeaProjects/TEB_REMAKE/figures/Rise.png'

    color_scale = config.color_scale
    ellipse_colors = {conc: color_scale[i % len(color_scale)] for i, conc in enumerate(concentrations)}
    pulse_colors = {pulse: color_scale[i % len(color_scale)] for i, pulse in enumerate(pulses)}
    concentration_values = {'00156': 0.0156, '00312': 0.0312, '00625': 0.0625}

    min_size, max_size = 5, 15
    marker_sizes = {
            conc: min_size + (max_size - min_size) * (value - min(concentration_values.values())) /
                  (max(concentration_values.values()) - min(concentration_values.values()))
            for conc, value in concentration_values.items()
    }
    marker_border = {
            '00156': 1,
            '00312': 1,
            '00625': 5
    }

    data = {conc: {} for conc in concentrations}

    with h5py.File(processed_hdf_path, 'r') as hdf_file:
        for conc in concentrations:
            for pulse in pulses:
                group_path = f"{conc}/0/{pulse}"
                if group_path not in hdf_file:
                    print(f"❌ {group_path} not found")
                    continue

                e_sq, dn_inf, rise_c1, rise_c2, rise_d, fall_c1, fall_d = load_group_data(hdf_file[group_path])
                data[conc][pulse] = (e_sq, dn_inf, rise_c1, rise_c2, rise_d, fall_c1, fall_d)

    added_to_legend = {pulse: False for pulse in pulses}
    table_data = []
    fig = go.Figure()
    print(concentrations)
    for conc in concentrations:

        plt.figure(figsize=(8, 6))
        for pulse, (e_sq, dn_inf, rise_c1, rise_c2, rise_d, fall_c1, fall_d) in data[conc].items():
            color = pulse_colors[pulse]
            show_in_legend = not added_to_legend[pulse]
            added_to_legend[pulse] = True

            e_sq_scaled, dn_inf_scaled = e_sq * 1e-3, dn_inf * 1e6
            table_data.append([conc, pulse, rise_c1[0], rise_c2[0], rise_d[0], fall_c1[0], fall_d[0]])

            fig.add_trace(go.Scatter(
                    x=np.sqrt(e_sq), y=rise_d*1e3, mode='markers',
                    marker=dict(size=config.marker_size, color=color, opacity=0.7,
                                line=dict(width=marker_border[conc], color=config.marker_border_color)),
                    name=fr'$\Huge{pulse}\,[\mathrm{{ms}}]$',  # Only show pulse width in legend
                    legendgroup=pulse,  # Group by pulse width
                    showlegend=show_in_legend
            ))

            # plt.scatter(np.sqrt(e_sq), fall_d, label=f"{conc}-{pulse}" if show_in_legend else "", alpha=0.7)
            # plt.scatter(np.sqrt(e_sq), rise_d, label=f"{conc}-{pulse}" if show_in_legend else "", alpha=0.7)

    kerr_config = config.get_kerr_plot_layout()
    fig.update_layout(kerr_config)
    pio.write_image(fig, output_path, format='png', scale=3)
    print(f"✅ Plot saved to {output_path}")

    headers = ["Concentration", "Pulse", "Rise_c1", "Rise_c2", "Rise_D", "Fall_c1", "Fall_D"]
    print(table_data)
    # print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    concentrations = ['00312', '00156', '00625']
    pulse_widths = ['100', '150', '200', '300']
    plot_all_kerr_data(concentrations, pulse_widths)
