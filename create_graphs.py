import os
from pathlib import Path

import h5py
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from configuration import get_experiment_config


def plot_kerr_data(pulse, conc):
    # Get configuration
    config = get_experiment_config()

    # Define the file path
    processed_hdf_filename = os.path.join(config.base_dirs.database, "processed_experiment_data.h5")

    # Open the processed HDF5 file
    with h5py.File(processed_hdf_filename, 'r') as processed_hdf:
        # Generate the correct group path: conc/flow/pulsewidth
        group_path = f"{conc}/0/{pulse}"

        if group_path not in processed_hdf:
            print(f"❌ Group {group_path} not found in the database.")
            return

        # Access the group corresponding to conc/flow/pulsewidth
        group = processed_hdf[group_path]
        print(f"Group keys at {group_path}: {group.keys()}")  # Debugging line to inspect keys

        e_squared = []
        dn_infinity = []

        # Iterate over the datasets in the group (which represent filenames)
        for filename in group:
            filename_group = group[filename]
            print(f"Checking file: {filename}, keys: {filename_group.keys()}")  # Debugging line to inspect keys

            # Check if the necessary keys exist in the current dataset (file group)
            if "e_square" in filename_group:
                e_squared.append(np.array(filename_group["e_square"]))
                print(filename_group["e_square"])
            if "dn_infinity" in filename_group:
                dn_infinity.append(np.array(filename_group["dn_infinity"])*1e6)

        # Convert lists to numpy arrays
        e_squared.append(0)
        dn_infinity.append(0)
        e_squared = np.array(e_squared)
        dn_infinity = np.array(dn_infinity)
        print(e_squared, dn_infinity)
        # Ensure data is not empty
        if e_squared.size == 0 or dn_infinity.size == 0:
            print("❌ No valid data found for e_square and dn_infinity.")
            return

        # Plotting the results
        fig = go.Figure()

        fig.add_trace(go.Scatter(
                x=e_squared,
                y=dn_infinity,
                mode='markers',
                marker=dict(
                        size=10,
                        color='blue',
                        opacity=0.7,
                        line=dict(width=1, color='black')
                ),
                name=f'{conc} {pulse}'
        ))

        # Update layout
        fig.update_layout(
                title=f"Kerr Effect: \(E^2\) vs \( \Delta n_\infty \)",
                xaxis_title=r"$E^2 \, [kV^2/cm^2]$",
                yaxis_title=r"$\Delta n_\infty \times 10^{-6}$",
                hovermode="closest",
                template="plotly_white"
        )

        # Save or display the plot
        pio.write_image(fig, Path(config.base_dirs.figures) / f"{conc}_{pulse}_kerr.png", format='png', scale=3)

def plot_c1_c2_data(pulse, conc):
    # Get configuration
    config = get_experiment_config()

    # Define the file path
    processed_hdf_filename = os.path.join(config.base_dirs.database, "processed_experiment_data.h5")

    # Open the processed HDF5 file
    with h5py.File(processed_hdf_filename, 'r') as processed_hdf:
        # Generate the correct group path: conc/flow/pulsewidth
        group_path = f"{conc}/0/{pulse}"

        if group_path not in processed_hdf:
            print(f"❌ Group {group_path} not found in the database.")
            return

        # Access the group corresponding to conc/flow/pulsewidth
        group = processed_hdf[group_path]
        print(f"Group keys at {group_path}: {group.keys()}")  # Debugging line to inspect keys

        e_squared = []
        dn_infinity = []

        # Iterate over the datasets in the group (which represent filenames)
        for filename in group:
            filename_group = group[filename]
            print(f"Checking file: {filename}, keys: {filename_group.keys()}")  # Debugging line to inspect keys

            # Check if the necessary keys exist in the current dataset (file group)
            if "e_square" in filename_group:
                e_squared.append(np.array(filename_group["Rise_c1"]))
                print(filename_group["e_square"])
            if "dn_infinity" in filename_group:
                dn_infinity.append(np.array(filename_group["Rise_c2"]))

        # Convert lists to numpy arrays
        e_squared.append(0)
        dn_infinity.append(0)
        e_squared = np.array(e_squared)
        dn_infinity = np.array(dn_infinity)
        print(e_squared, dn_infinity)
        # Ensure data is not empty
        if e_squared.size == 0 or dn_infinity.size == 0:
            print("❌ No valid data found for e_square and dn_infinity.")
            return

        # Plotting the results
        fig = go.Figure()

        fig.add_trace(go.Scatter(
                x=e_squared,
                y=dn_infinity,
                mode='markers',
                marker=dict(
                        size=10,
                        color='blue',
                        opacity=0.7,
                        line=dict(width=1, color='black')
                ),
                name=f'{conc} {pulse}'
        ))

        # Update layout
        fig.update_layout(
                title=f"Kerr Effect: \(E^2\) vs \( \Delta n_\infty \)",
                xaxis_title=r"$E^2 \, [kV^2/cm^2]$",
                yaxis_title=r"$\Delta n_\infty \times 10^{-6}$",
                hovermode="closest",
                template="plotly_white"
        )

        # Save or display the plot
        pio.write_image(fig, Path(config.base_dirs.figures) / f"{conc}_{pulse}_c1_c2.png", format='png', scale=3)

# Example usage
for pulse in ['100', '150', '200', '300']:
    plot_kerr_data(pulse, "00312")
    plot_c1_c2_data(pulse, "00312")
