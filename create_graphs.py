import os
from pathlib import Path

import h5py
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from configuration import get_experiment_config
from plot_utilities import KerrPlotConfig

def plot_all_kerr_data(concs: list, pulses: list):
    config_exp = get_experiment_config()
    processed_hdf_filename = os.path.join(config_exp.base_dirs.database, "processed_experiment_data.h5")

    color_scale = px.colors.qualitative.D3
    fig = go.Figure()

    # Global color index to cycle through colors uniquely across (conc, pulse) pairs
    color_index = 0
    for conc in concs:
        for pulse in pulses:
            with h5py.File(processed_hdf_filename, 'r') as processed_hdf:
                group_path = f"{conc}/0/{pulse}"
                if group_path not in processed_hdf:
                    print(f"❌ Group {group_path} not found in the database.")
                    continue

                group = processed_hdf[group_path]
                e_squared_list = []
                dn_infinity_list = []

                for filename in group:
                    filename_group = group[filename]
                    if "e_square" in filename_group:
                        e_squared_list.append(np.array(filename_group["e_square"]))
                    if "dn_infinity" in filename_group:
                        dn_infinity_list.append(np.array(filename_group["dn_infinity"]) * 1e6)

                e_squared = np.array(e_squared_list)
                dn_infinity = np.array(dn_infinity_list)

                if e_squared.size == 0 or dn_infinity.size == 0:
                    print(f"❌ No valid data found for conc {conc} pulse {pulse}.")
                    continue

                sort_idx = np.argsort(e_squared)
                e_squared = e_squared[sort_idx]
                dn_infinity = dn_infinity[sort_idx]
                color = color_scale[color_index % len(color_scale)]
                color_index += 1

                fig.add_trace(go.Scatter(
                        x=e_squared,
                        y=dn_infinity,
                        mode='markers',
                        marker=dict(
                                size=10,
                                color=color,
                                opacity=0.7,
                                line=dict(width=1, color='black')
                        ),
                        name=f'Conc {conc}, {pulse} [ms]',
                        showlegend=True
                ))

                slope, intercept = np.polyfit(e_squared, dn_infinity, 1)
                poly_fit = np.poly1d((slope, intercept))
                x_fit = np.linspace(e_squared.min(), e_squared.max(), 100)
                y_fit = poly_fit(x_fit)
                fig.add_trace(go.Scatter(
                        x=x_fit,
                        y=y_fit,
                        mode='lines',
                        line=dict(
                                color=color,
                                width=3,
                                dash='dash'
                        ),
                        showlegend=False
                ))

    kerr_config = KerrPlotConfig()
    layout = kerr_config.get_layout()
    layout.update({
            "xaxis": {
                    **layout.get("xaxis", {}),
                    "title": r"$\Huge{E^2 \, [kV^2/cm^2]}$"
            },
            "yaxis": {
                    **layout.get("yaxis", {}),
                    "title": r"$\Huge{\langle \Delta n_{\infty} \rangle \times 10^{-6}}$"
            }
    })
    fig.update_layout(layout)

    # Update legend settings to ensure all entries are visible
    fig.update_layout(
            legend=dict(
                    traceorder="normal",
                    font=dict(size=20),
                    title=dict(text="Data Traces")
            ),
            hovermode="closest",
            template="plotly_white"
    )

    output_path = Path(config_exp.base_dirs.figures) / "kerr_all_pulses.png"
    pio.write_image(fig, output_path, format='png', scale=3)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    concentrations = ['00312', '00156', '00625']  # Concentrations to include
    pulse_widths = ['100', '150', '200', '300']
    plot_all_kerr_data(concentrations, pulse_widths)
