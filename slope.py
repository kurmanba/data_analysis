from dataclasses import dataclass, field
from pathlib import Path

import h5py
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


@dataclass
class Configuration:
    kerr_plot_width: int = 1500
    kerr_plot_height: int = 800
    kerr_plot_margin: dict = field(default_factory=lambda: dict(l=50, r=50, t=50, b=50))
    show_legend: bool = True

    # Axis configuration
    xaxis_title: str = r'$\Huge{K_{0} \, [\frac{\Delta n}{E^2} \times 10^6 ]}$'
    yaxis_title: str = r'$\Huge{\text{\Delta n (E = 0)} \, [\Delta n \times 10^6]}$'
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
    marker_size: int = 30
    marker_symbol: str = 'circle'
    marker_border_width: int = 2
    marker_border_color: str = 'black'
    line_width: int = 5

    # Experiment related paths
    experiment_base_dirs: dict = field(default_factory=lambda: {
            'database': "/path/to/database",
            'figures': "/path/to/figures"
    })

    def get_kerr_plot_layout(self):
        layout = {
                "plot_bgcolor": 'white',
                "paper_bgcolor": 'white',
                "font": self._get_font_config(),
                "margin": self.kerr_plot_margin,
                "width": self.kerr_plot_width,
                "height": self.kerr_plot_height,
                "showlegend": self.show_legend,
                "legend": dict(
                        x=0.02, y=0.18,
                        font=dict(size=24, family=self.font_family, color=self.font_color),
                        bgcolor='rgba(255,255,255,0.7)',
                        bordercolor='black',
                        borderwidth=1
                ),
                "xaxis": self._get_axis_config(self.xaxis_title),
                "yaxis": self._get_axis_config(self.yaxis_title)
        }
        return layout

    def _get_font_config(self):
        return {'family': self.font_family, 'size': self.font_size, 'color': self.font_color}

    def _get_axis_config(self, title):
        return {
                'title': title,
                'showline': True,
                'linewidth': self.plot_border_width,
                'linecolor': self.plot_border_color,
                'mirror': True,
                'tickfont': {'size': self.font_size, 'family': self.font_family, 'color': self.font_color},
                "ticks": "inside" if self.tick_style["inside"] else "outside",
                "tickwidth": self.tick_style["width"],
                "tickcolor": self.tick_style["color"],
                "ticklen": self.tick_style["length"]
        }


def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def generate_ellipse(center, a, b, angle_deg, num_points=100):
    t = np.linspace(0, 2*np.pi, num_points)
    angle = np.deg2rad(angle_deg)
    x = center[0] + a * np.cos(t) * np.cos(angle) - b * np.sin(t) * np.sin(angle)
    y = center[1] + a * np.cos(t) * np.sin(angle) + b * np.sin(t) * np.cos(angle)
    return x, y


def load_group_data(group):
    e_squared, dn_infinity = [], []
    for filename in group:
        dataset = group[filename]
        if "e_square" in dataset:
            e_squared.append(np.array(dataset["e_square"]))
        if "dn_infinity" in dataset:
            dn_infinity.append(np.array(dataset["dn_infinity"]) * 1e6)
    if not e_squared or not dn_infinity:
        return None, None
    e_squared = np.array(e_squared).flatten()
    dn_infinity = np.array(dn_infinity).flatten()
    if e_squared.size == 0 or dn_infinity.size == 0:
        return None, None
    sort_idx = np.argsort(e_squared)
    return e_squared[sort_idx], dn_infinity[sort_idx]


def plot_slope_intercept_scatter(config: Configuration, concentrations, pulses):
    processed_hdf_path = Path("/Users/alisher/IdeaProjects/TEB_REMAKE/databases") / "processed_experiment_data.h5"
    output_path = Path("/Users/alisher/IdeaProjects/TEB_REMAKE/figures") / "slope_intercept_scatter.png"

    color_scale = config.color_scale
    ellipse_colors = {conc: color_scale[i % len(color_scale)] for i, conc in enumerate(concentrations)}
    pulse_colors = {pulse: color_scale[i % len(color_scale)] for i, pulse in enumerate(pulses)}

    slope_intercept = {conc: {} for conc in concentrations}
    ellipse_points = {conc: [] for conc in concentrations}

    with h5py.File(processed_hdf_path, 'r') as hdf_file:
        for conc in concentrations:
            for pulse in pulses:
                group_path = f"{conc}/0/{pulse}"
                if group_path not in hdf_file:
                    continue
                e_sq, dn_inf = load_group_data(hdf_file[group_path])
                if e_sq is None or dn_inf is None:
                    continue
                slope, intercept = np.polyfit(e_sq, dn_inf, 1)
                slope_intercept[conc][pulse] = (slope, intercept)
                ellipse_points[conc].append([slope, intercept])

    fig = go.Figure()
    added_to_legend = {pulse: False for pulse in pulses}

    for conc in concentrations:
        for pulse in pulses:
            if pulse not in slope_intercept[conc]:
                continue
            slope, intercept = slope_intercept[conc][pulse]
            color = pulse_colors[pulse]
            show_legend = not added_to_legend[pulse]
            added_to_legend[pulse] = True
            fig.add_trace(go.Scatter(
                    x=[slope], y=[intercept],
                    mode='markers',
                    marker=dict(
                            size=config.marker_size,
                            color=color,
                            symbol=config.marker_symbol,
                            line=dict(width=config.marker_border_width, color=config.marker_border_color)
                    ),
                    name=fr'$\Huge{pulse}\,[\mathrm{{ms}}]$',
                    legendgroup=pulse,
                    showlegend=show_legend
            ))

    # Generate ellipses based on covariance
    for conc in concentrations:
        if len(ellipse_points[conc]) < 2:
            continue  # Not enough points to compute covariance
        points = np.array(ellipse_points[conc])
        center = np.mean(points, axis=0)
        cov = np.cov(points, rowvar=False)
        lambda_, v = np.linalg.eig(cov)
        scale = 2  # Adjust this to change ellipse size
        a, b = np.sqrt(lambda_) * scale
        angle = np.degrees(np.arctan2(v[1, 0], v[0, 0]))
        x_ellipse, y_ellipse = generate_ellipse(center, a, b, angle)
        fill_color = hex_to_rgba(ellipse_colors[conc], alpha=0.1)
        fig.add_trace(go.Scatter(
                x=x_ellipse, y=y_ellipse,
                fill='toself',
                fillcolor=fill_color,
                line=dict(color=ellipse_colors[conc], width=1),
                showlegend=False,
                hoverinfo='skip'
        ))

    annotations = [
            {"x": 0.025, "y": -3, "text": r"$\Huge{0.0156\%}$", "showarrow": True, "ax": 0, "ay": 0},
            {"x": 0.035, "y": -10, "text": r"$\Huge{0.0312\%}$", "showarrow": True, "ax": 0, "ay": 0},
            {"x": 0.055, "y": -6, "text": r"$\Huge{0.0625\%}$", "showarrow": True, "ax": 0, "ay": 0}
    ]

    for annotation in annotations:
        fig.add_annotation(
                x=annotation["x"],
                y=annotation["y"],
                text=annotation["text"],
                showarrow=annotation["showarrow"],
                arrowhead=4,
                arrowsize=2,
                ax=annotation["ax"],
                ay=annotation["ay"],
                font=dict(size=20, color='black'),
                bgcolor="white",
                borderpad=4
        )
    layout = config.get_kerr_plot_layout()
    fig.update_layout(layout)
    pio.write_image(fig, output_path, format='png', scale=3)
    print(f"✅ Plot saved to {output_path}")


if __name__ == "__main__":
    config = Configuration()
    concentrations = ['00312', '00156', '00625']
    pulses = ['100', '150', '200', '300']
    plot_slope_intercept_scatter(config, concentrations, pulses)