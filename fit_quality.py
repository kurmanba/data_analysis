from dataclasses import dataclass, field
from pathlib import Path

import h5py
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

@dataclass
class PlotConfig:
    plot_title: str = ""
    xaxis_title: str = ""
    yaxis_title: str = ""
    extra_yaxis_titles: dict = field(default_factory=dict)
    x_range: tuple = None
    y_range: tuple = None
    smoothing_sigma: int = 5
    colors: dict = field(default_factory=lambda: {"ch_1": "blue", "ch_2": "red"})
    color_scale: list = field(default_factory=lambda: px.colors.qualitative.D3)
    line_width: int = 2
    marker_size: int = 1
    marker_opacity: float = 0.3
    marker_line_width: float = 0.5
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
                "xaxis": {"title": self.xaxis_title, "range": self.x_range, **self.plot_options["xaxis"]},
                "yaxis": {"title": self.yaxis_title, "range": self.y_range, **self.plot_options["yaxis"]},
        }
        for key, title in self.extra_yaxis_titles.items():
            axes[key] = {"title": title, **self.plot_options["yaxis"]}
        return axes

def plot_dn_values(hdf_filename, conc_selection=None, pulse_selection=None):
    plot_config = PlotConfig(
            xaxis_title=r"$ \Huge{t \text{ [ms]}}$",
            yaxis_title=r"$\Huge{\langle \Delta n (t) \rangle \times 10^{6} }$",
            x_range=(0, 50),
            y_range=(0.5, 1),
            line_width=3,
            marker_size=5,
            marker_opacity=0.7,
            marker_line_width=0.1
    )

    output_path = Path("/Users/alisher/IdeaProjects/TEB_REMAKE/figures") / "fit_quality.png"

    if conc_selection is None:
        conc_selection = ["00156", "00312", "00625"]
    if pulse_selection is None:
        pulse_selection = ["100", "150", "200", "300"]

    fig = go.Figure()
    data_list = []

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
                        dn_values = dataset['Rise'][:]
                        dn_values /= np.max(dn_values)
                        s_fit = dataset['s_rise_fit'][:]
                        time_values = dataset['Rise_time'][:]
                        data_list.append((voltage, time_values, dn_values, s_fit, group_path))

    data_list.sort(key=lambda x: x[0], reverse=True)

    for idx, (voltage, time_values, dn_values, s_fit, group_path) in enumerate(data_list):
        color = plot_config.color_scale[idx % len(plot_config.color_scale)]
        fig.add_trace(go.Scatter(
                x=time_values,
                y=s_fit,
                mode='lines',
                name=rf'$\Huge{{E_{{{idx + 1}}}}}$',
                line=dict(color=color, width=plot_config.line_width)
        ))
        fig.add_trace(go.Scatter(
                x=time_values, y=dn_values, mode='markers',
                marker=dict(size=plot_config.marker_size, color=color, opacity=plot_config.marker_opacity,
                            line=dict(width=plot_config.marker_line_width, color=color)),
                showlegend=False
        ))

    fig.update_layout(**plot_config.get_layout(), **plot_config.get_axes_options())
    pio.write_image(fig, output_path, format='png', scale=3)
    print(f"✅ Plot saved to {output_path}")

hdf_filename = "/Users/alisher/IdeaProjects/TEB_REMAKE/databases/processed_experiment_data.h5"
pulses = ["100"]
for pulse in pulses:
    plot_dn_values(hdf_filename, conc_selection=["00625"], pulse_selection=[pulse])