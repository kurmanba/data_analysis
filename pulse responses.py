import os
import sys

import h5py
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

from configuration import get_experiment_config

if sys.platform == "darwin":
    mpl.use("macosx")


def plot_dn_values(conc_selection=None, pulse_selection=None):
    """
    Plot dn values from processed database for given concentrations and pulse widths.

    Args:
        conc_selection (list): List of concentration strings to plot (e.g., ["00156", "00312"])
        pulse_selection (list): List of pulse width strings to plot (e.g., ["100", "200"])
    """
    config = get_experiment_config()
    processed_hdf_filename = os.path.join(config.base_dirs.database, "processed_experiment_data.h5")

    # Default selections if none provided
    if conc_selection is None:
        conc_selection = ["00156", "00312", "00625"]
    if pulse_selection is None:
        pulse_selection = ["100", "150", "200", "300"]

    # Generate all possible group paths
    group_paths = []
    for conc in conc_selection:
        for flow in sorted(config.potentials.flows):
            for pulse in pulse_selection:
                group_paths.append(f"{conc}/{flow}/{pulse}")

    plt.figure()

    with h5py.File(processed_hdf_filename, 'r') as processed_hdf:
        for group_path in group_paths:
            # Check if group exists in the file
            if group_path not in processed_hdf:
                continue

            conc, flow, pulse = group_path.split('/')

            # Iterate through datasets in the group
            for dataset_name in processed_hdf[group_path]:

                dataset = processed_hdf[group_path][dataset_name]
                st, end, _, _, accept = (lambda b: (b.st, b.end, b.tr1, b.tr2, b.accept))(
                        config.directories.boundaries.get(f'{group_path}/{dataset_name}', None))
                print(st, end)
                if 'dn' not in dataset or 'time' not in dataset:
                    continue

                # dn_values = dataset['dn'][:]
                # time_values = dataset['time'][:]

                # dn_values = dataset['s_rise_fit'][:]

                dn_values = dataset['Fall'][:]
                dn_values /= np.max(dataset['Fall'][:])
                dn_scatter = dataset['s_fall_fit'][:]
                time_values = dataset['Fall_time'][:]

                dn_values = dataset['Rise'][:]
                dn_values /= np.max(dataset['Rise'][:])
                dn_scatter = dataset['s_rise_fit'][:]
                time_values = dataset['Rise_time'][:]

                # dn_values = dataset['dn'][:]
                # dn_values = dataset['reg_values'][:]
                # time_values = dataset['reg_times'][:]
                # dn_values /= np.sum(dn_values)

                # dn_values[time_values > 150] = 0

                label = f"{group_path}"
                plt.plot(time_values, dn_scatter, label=label)
                plt.scatter(time_values, dn_values, label=label, s=5)

                # plt.plot( dn_values, label=label)
                # plt.plot( dn_scatter, label=label)
                # plt.vlines([st, end], ymin=0, ymax=1e-5, colors='r', linestyles='dashed')

    plt.xlabel('Time (s)')
    plt.ylabel('dn (a.u.)')
    plt.title('dn Values for Selected Concentrations and Pulse Widths')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# conc_selection = ["00156", "00312", "00625"]
pulses = ["100", "150", "200", "300"]
# pulses = ["200"]
# process_database()
for pulse in pulses:
    plot_dn_values(conc_selection=["00625"], pulse_selection=[pulse])
