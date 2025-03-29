import os
from pathlib import Path

import h5py
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from configuration import get_experiment_config
from plot_utilities import KerrPlotConfig


def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def generate_ellipse(center, a, b, angle_deg, num_points=100):
    t = np.linspace(0, 2 * np.pi, num_points)
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


def plot_all_kerr_data(concentrations, pulses):
    config_exp = get_experiment_config()
    processed_hdf_path = Path(config_exp.base_dirs.database) / "processed_experiment_data.h5"

    color_scale = px.colors.qualitative.D3
    ellipse_colors = {conc: color_scale[i % len(color_scale)] for i, conc in enumerate(concentrations)}
    pulse_colors = {pulse: color_scale[i % len(color_scale)] for i, pulse in enumerate(pulses)}

    data = {conc: {} for conc in concentrations}
    ellipse_points = {conc: [] for conc in concentrations}

    with h5py.File(processed_hdf_path, 'r') as hdf_file:
        for conc in concentrations:
            for pulse in pulses:
                group_path = f"{conc}/0/{pulse}"
                if group_path not in hdf_file:
                    print(f"❌ {group_path} not found")
                    continue

                e_sq, dn_inf = load_group_data(hdf_file[group_path])
                if e_sq is None or dn_inf is None:
                    continue

                data[conc][pulse] = (e_sq, dn_inf)
                ellipse_points[conc].append(np.column_stack((e_sq, dn_inf)))

    fig = go.Figure()

    for conc in concentrations:
        for pulse, (e_sq, dn_inf) in data[conc].items():
            color = pulse_colors[pulse]

            fig.add_trace(go.Scatter(
                    x=e_sq, y=dn_inf, mode='markers',
                    marker=dict(size=10, color=color, opacity=0.7, line=dict(width=1, color='black')),
                    name=f'{conc} - {pulse} ms'
            ))

            slope, intercept = np.polyfit(e_sq, dn_inf, 1)
            x_fit = np.linspace(e_sq.min(), e_sq.max(), 100)
            fig.add_trace(go.Scatter(
                    x=x_fit, y=slope*x_fit + intercept, mode='lines',
                    line=dict(color=color, width=3, dash='dash'), showlegend=False
            ))

    ellipse_params = {
            '00312': {'a': 1.6, 'b': 200, 'angle': 92.3},
            '00156': {'a': 1.6, 'b': 200, 'angle': 91.2},
            '00625': {'a': 1.6, 'b': 200, 'angle': 92.8}
    }

    for conc in concentrations:
        if not ellipse_points[conc]:
            continue

        points = np.concatenate(ellipse_points[conc])
        center = np.mean(points, axis=0)
        params = ellipse_params.get(conc, {'a': 0.5, 'b': 0.25, 'angle': 0})
        x, y = generate_ellipse(center, params['a'], params['b'], params['angle'])

        fill_color = hex_to_rgba(ellipse_colors[conc], alpha=0.1)
        fig.add_trace(go.Scatter(
                x=x, y=y, fill='toself', fillcolor=fill_color,
                line=dict(color=ellipse_colors[conc], width=0.1),
                showlegend=False, hoverinfo='skip'
        ))

    kerr_config = KerrPlotConfig().get_layout()
    kerr_config["xaxis"]["title"] = r"$\Huge{E^2 \,[kV^2/cm^2]}$"
    kerr_config["yaxis"]["title"] = r"$\Huge{\langle \Delta n_{\infty} \rangle \times 10^{-6}}$"
    fig.update_layout(kerr_config)

    # Save figure
    output_path = Path(config_exp.base_dirs.figures) / "kerr_all_pulses_with_ellipses.png"
    pio.write_image(fig, output_path, format='png', scale=3)
    print(f"✅ Plot saved to {output_path}")


if __name__ == "__main__":
    concentrations = ['00312', '00156', '00625']
    pulse_widths = ['100', '150', '200', '300']
    plot_all_kerr_data(concentrations, pulse_widths)