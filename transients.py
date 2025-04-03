import os
import sys
from pathlib import Path

import h5py
import numpy as np
import plotly.graph_objects as go
from configuration import get_experiment_config
from scipy.signal import savgol_filter as sgf

from dataclasses import dataclass, field
import plotly.io as pio

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

def plot_dn_values(hdf_filename, conc_selection=None, pulse_selection=None):
    """
    Plot dn values from processed database for given concentrations and pulse widths, sorted by highest E values.
    """
    plot_config = PlotConfig()
    plot_config = PlotConfig(xaxis_title=r"$ \Huge{t \text{ [ms]}}$",
                             yaxis_title=r"$\Huge{\langle \Delta n (t) \rangle \times 10^{6} }$",
                             color_scale=px.colors.qualitative.Set2)

    output_path  = Path("/Users/alisher/IdeaProjects/TEB_REMAKE/figures") / "transients.png"

    if conc_selection is None:
        conc_selection = ["00156", "00312", "00625"]
    if pulse_selection is None:
        pulse_selection = ["100", "150", "200", "300"]

    fig = go.Figure()
    data_list = []
    color_scale = px.colors.qualitative.D3


    with h5py.File(hdf_filename, 'r') as processed_hdf:
        for conc in conc_selection:
            for pulse in pulse_selection:
                for flow in processed_hdf.get(conc, {}):
                    group_path = f"{conc}/{flow}/{pulse}"
                    if group_path not in processed_hdf:
                        continue

                    for dataset_name in processed_hdf[group_path]:
                        dataset = processed_hdf[group_path][dataset_name]
                        voltage = np.sqrt(np.array(dataset["e_square"]))
                        dn_values = dataset['dn'][:]*1e6
                        # dn_values/=np.max(dn_values)
                        dn_values = sgf(dn_values, 501, 1)
                        time_values = dataset['time'][:] - np.min(dataset['time'][:])
                        data_list.append((voltage, time_values, dn_values, group_path))

    data_list.sort(key=lambda x: x[0], reverse=True)

    for idx, (voltage, time_values, dn_values, group_path) in enumerate(data_list):
        color = color_scale[idx % len(color_scale)]
        fig.add_trace(go.Scatter(
                x=time_values,
                y=dn_values,
                mode='lines',
                name=rf'$\Huge{{E_{{{idx + 1}}}}}$',
                line=dict(color=color, width=4)
        ))

    fig.update_layout(**plot_config.get_layout(), **plot_config.get_axes_options())
    pio.write_image(fig, output_path, format='png', scale=3)
    print(f"✅ Plot saved to {output_path}")


hdf_filename = "/Users/alisher/IdeaProjects/TEB_REMAKE/databases/processed_experiment_data.h5"
# pulses = ["100", "150", "200", "300"]
pulses = ["100"]
for pulse in pulses:
    plot_dn_values(hdf_filename, conc_selection=["00312"], pulse_selection=[pulse])