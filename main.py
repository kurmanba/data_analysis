import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

from analizer import *
from configuration import get_experiment_config

if sys.platform == "darwin":
    mpl.use("macosx")


def read_oscilloscope_csv(file_path: str) -> np.ndarray:
    """
    Reads an oscilloscope CSV file.
    Skips the header and returns the data as a numpy array.
    """

    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("TIME,CH1,CH2"):
            header_index = i
            break
    else:
        raise ValueError("Could not find the data header in the file.")
    df = pd.read_csv(file_path, skiprows=header_index, usecols=[0, 1, 2], encoding='latin1')
    df = df.iloc[:, :3]
    # df.columns = ['TIME', 'CH1', 'CH2']

    return df.apply(pd.to_numeric, errors='coerce').to_numpy()


# def process_directory_math(directory):
#     """
#     Reads all CSV files in the given directory, extracts data, and plots:
#     1. CH1 vs. Time (Subplot 1)
#     2. CH2 vs. Time (Subplot 2, smoothed using Savitzky–Golay)
#     """
#     config = get_experiment_config()
#     kerr = []
#     kerr.append((0, 0))
#     fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
#     axes[0].set_title("CH1 vs Time")
#     axes[1].set_title("CH2 vs Time (Smoothed)")
#
#     for filename in os.listdir(directory):
#         if filename.startswith('.') and not filename.endswith('.csv'):
#             continue
#         file_path = os.path.join(directory, filename)
#         if os.path.isdir(file_path):
#             continue
#         print(file_path)
#
#         cut = 18000
#         data = read_oscilloscope_csv(file_path)
#         time = data[:cut, 0] * config.setup.time_multiplier
#         ch1 = np.nan_to_num(data[:cut, 1])
#         ch2 = data[:cut, 2] * config.setup.ch2_multiplier
#
#         ch1 -= np.min(ch1)
#         ch2 = sgf(ch2, 501, 1)
#         ch2 -= np.min(ch2)
#
#         axes[0].plot(ch1, label=f"{filename}")
#         axes[1].plot(ch2, label=f"{filename}")
#
#         dn = bg_sub(ch1, config)
#         kerr.append(((np.mean(ch1[5000:7500])) ** 2, np.mean(dn[5000:7500])))
#
#     axes[1].set_xlabel("Time (s)")
#     axes[0].set_ylabel("CH1 Signal")
#     axes[1].set_ylabel("CH2 Signal")
#
#     for ax in axes:
#         ax.legend()
#         ax.grid(True)
#
#     plt.suptitle(f"Signals vs Time ({directory})")
#     plt.show()
#
#     kerr_x, kerr_y = zip(*kerr)  # Unpacking tuple list into separate x and y lists
#     plt.scatter(kerr_x, kerr_y, marker='o', color='b', label="Kerr Effect")
#     plt.xlabel("Normalized CH1 squared (a.u.)")
#     plt.ylabel("Mean Background Subtracted CH1 (a.u.)")
#     plt.title("Kerr Effect Analysis")
#     plt.legend()
#     plt.grid(True)
#     plt.show()

def select_maximally_spaced_points(points, k):
    """
    Given a list of points (each is a tuple: (kerr_x, kerr_y, filename, color)),
    select k points that maximize the minimal distance between them using a greedy algorithm.
    """
    if len(points) <= k:
        return points

    selected = [points[0]]
    selected_indices = [0]

    while len(selected) < k:
        best_candidate = None
        best_candidate_index = None
        best_distance = -1

        for i, point in enumerate(points):
            if i in selected_indices:
                continue

            dists = [np.sqrt((point[0] - sel[0]) ** 2 + (point[1] - sel[1]) ** 2) for sel in selected]
            min_dist = min(dists)
            if min_dist > best_distance:
                best_distance = min_dist
                best_candidate = point
                best_candidate_index = i

        selected.append(best_candidate)
        selected_indices.append(best_candidate_index)

def modified_function(t, f):
    df_dt = np.gradient(f, t)  # Compute numerical derivative
    integral = np.cumsum(np.abs(df_dt) * np.gradient(t))  # Integrate |df/dt|
    return integral

def process_directory_math(directory):
    """
    Reads all CSV files in the given directory, extracts data, and plots:
      1. CH1 vs. Time (Subplot 1)
      2. CH2 vs. Time (Subplot 2, smoothed using Savitzky–Golay)
      3. Kerr Effect Analysis (Subplot 3) with slope in title
    Colors are consistent across all subplots.
    Only the Kerr subplot displays a legend.
    Out of all curves, only 6 are selected based on maximizing the mean distance between points.
    """

    config = get_experiment_config()
    file_list = []
    for filename in os.listdir(directory):
        if filename.startswith('.') and not filename.endswith('.csv'):
            continue
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            continue
        file_list.append(filename)

    if not file_list:
        print("No CSV files found in the directory.")
        return

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].set_title("CH1 vs Time")
    axes[1].set_title("CH2 vs Time (Smoothed)")

    colors = plt.cm.tab10(np.linspace(0, 1, len(file_list)))

    kerr = []

    for idx, filename in enumerate(file_list):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")
        cut = 18800
        data = read_oscilloscope_csv(file_path)
        time = data[:cut, 0]
        ch1 = np.nan_to_num(data[:cut, 1])* config.setup.ch1_multiplier
        ch2 = data[:cut, 2] * config.setup.ch2_multiplier

        ch2 = sgf(ch2, 551, 1)
        st, end = 0, 9588
        # ch2[st:end] = modified_function(time[st:end]- time[st], ch2[st:end] )
        # ch2 = sgf(ch2, 1051, 2)
        ch2 -= np.min(ch2)
        # ch2 /= np.max(ch2)

        color = colors[idx]
        axes[0].plot(ch1, color=color)
        axes[1].plot(ch2, color=color)

        dn = bg_sub(ch2, config)
        kerr_x = (np.mean(ch1[2900:2910]) ) ** 2
        kerr_y = np.mean(dn[2900:2910])
        kerr.append((kerr_x, kerr_y, filename, color))

    axes[0].set_ylabel("CH1 Signal")
    axes[1].set_ylabel("CH2 Signal")
    axes[1].set_xlabel("Time (s)")
    axes[0].grid(True)
    axes[1].grid(True)

    selected_kerr = kerr
    kerr_x_vals = [x for (x, y, _, _) in selected_kerr]
    kerr_y_vals = [y for (x, y, _, _) in selected_kerr]

    kerr_x_vals.insert(0, 0)
    kerr_y_vals.insert(0, 0)

    kerr_x_array = np.array(kerr_x_vals)
    kerr_y_array = np.array(kerr_y_vals)
    slope = np.sum(kerr_x_array * kerr_y_array) / np.sum(kerr_x_array ** 2)

    for (x, y, label, color) in selected_kerr:
        axes[2].scatter(x, y, color=color, label=label)

    fit_x = np.linspace(min(kerr_x_vals), max(kerr_x_vals), 100)
    fit_y = slope * fit_x
    axes[2].plot(fit_x, fit_y, 'r--', label=f"Slope: {slope*1e7:.3f}")

    axes[2].set_xlabel("Normalized CH1 squared (a.u.)")
    axes[2].set_ylabel("Mean Background Subtracted CH1 (a.u.)")
    axes[2].grid(True)
    axes[2].legend(fontsize=10)

    axes[2].set_title(f"Kerr Effect Analysis (Slope = {slope*1e7:.3f})")
    plt.suptitle(f"Signals and Kerr Effect ({directory})")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


if __name__ == '__main__':
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/raw_data_averages/EG_00625_standard')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/40')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/50')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/60')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/70')

    process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00625_300')
    process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00625_200')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00625_150')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00625_100')

    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00078_300")
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00078_200")
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00078_150")
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00078_100")

    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/examples")
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/Experimtents/Damage_experiment/EG_00078_damage_concentration')
    # process_directory_math('/Users/alisher/`IdeaProjects/TEB_REMAKE/Experimtents/Damage_experiment/EG_00156_damage_concentration')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/Experimtents/Damage_experiment/EG_00312_damage_concentration')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/Experimtents/Damage_experiment/EG_00625_damage_concentration')
    #
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00156_300")
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00156_200")
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00156_150")
    # process_directory_math("/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00156_100")
    #
    # # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/sd/examples/New Folder With Items')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00312_100')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00312_150')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00312_200')
    # process_directory_math('/Users/alisher/IdeaProjects/TEB_REMAKE/exp_pulses/00312_300')
