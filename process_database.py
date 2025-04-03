import os

import h5py
import pywt
from tqdm import tqdm

from analizer import *
from configuration import get_experiment_config
from scipy.signal import savgol_filter as sgf

if sys.platform == "darwin":
    mpl.use("macosx")


def wavelet_denoise(signal,
                    wavelet='coif2'
                    , level=10,
                    threshold_method='soft') -> np.ndarray:
    """
    Apply wavelet denoising to the signal.
    """
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745  # Robust noise estimate
    threshold = sigma * np.sqrt(2 * np.log(len(signal)))  # Universal threshold
    coeffs[1:] = [pywt.threshold(c, threshold, mode=threshold_method) for c in coeffs[1:]]

    return pywt.waverec(coeffs, wavelet)[:len(signal)]


def get_existing_groups(hdf_filename,
                        group_paths) -> list:
    """Check and return only existing groups in the HDF5 file."""

    with h5py.File(hdf_filename, 'r') as hdf:
        return [gp for gp in group_paths if gp in hdf]


def generate_group_paths(config,
                         pulse_selection=None,
                         conc_selection=None) -> list:
    """
    Generate sorted group paths based on pulse width, concentrations, and flows.
    """
    group_paths = []
    selected_pulses = pulse_selection if pulse_selection else config.pulse_width
    selected_concentrations = conc_selection if conc_selection else config.potentials.concentrations

    for conc in sorted(selected_concentrations):
        for flow in sorted(config.potentials.flows):
            for pulse in sorted(selected_pulses, reverse=True):
                group_paths.append(f"{conc}/{flow}/{pulse}")

    return group_paths


def interpret_dataset(data,
                      config,
                      group,
                      dataset):
    """
    Interprets the dataset and returns the processed data.
    """

    st, end, _, _, _ = (lambda b: (b.st, b.end, b.tr1, b.tr2, b.accept))(
            config.directories.boundaries.get(f'{group}/{dataset}', None))

    time, field, intensity = data[:config.setup.cut, :].T
    time *= config.setup.time_multiplier
    field *= config.setup.ch1_multiplier
    intensity *= config.setup.ch2_multiplier

    sample_rate = np.mean(np.diff(time))

    relaxation = intensity[end:] - np.min(intensity[end:])
    relaxation_time = time[end:] - time[end]

    rise = intensity[st:end] - np.min(intensity[st:end])
    rise_time = time[st:end] - time[st]

    dn_rise = bg_sub(rise, config)
    dn_fall = bg_sub(relaxation, config)

    s_rise = get_scale(dn_rise)
    s_fall = get_scale(dn_fall)

    d_rise, c1_rise, c2_rise, p = find_consts_double_rise(s_rise, rise_time, config)
    d_fall, c1_fall, delay, b = find_consts_fall(s_fall, relaxation_time, config)

    s_rise_fit = double_rise(rise_time, d_rise, c1_rise, c2_rise, p)
    s_rise_fit /= np.max(s_rise_fit)
    s_fall_fit = double_fall(relaxation_time, d_fall, c1_fall, delay, b, config)
    s_fall_fit /= np.max(s_fall_fit)

    time_rise_std = np.arange(0, config.fit.standard_time, sample_rate)
    time_fall_std = np.arange(0, config.fit.standard_time, sample_rate)

    dn_rise_std = np.zeros_like(time_rise_std)
    dn_fall_std = np.zeros_like(time_fall_std)

    if len(dn_rise) <= len(dn_rise_std):
        dn_rise_std[: len(dn_rise)] = dn_rise
        dn_rise_std[len(dn_rise):] = dn_rise[-1] if len(dn_rise) > 0 else 0
    else:
        dn_rise_std = dn_rise[: len(dn_rise_std)]
    if len(dn_fall) <= len(dn_fall_std):
        dn_fall_std[: len(dn_fall)] = dn_fall
        dn_fall_std[len(dn_fall):] = 0
    else:
        dn_fall_std[: len(dn_fall_std)] = dn_fall[: len(dn_fall_std)]

    reg_times, reg_values = regularization(time_fall_std, sgf(dn_fall_std,201,1), config)

    aspect_ratio = conver_p(1 / (6 * d_fall), config)
    dn_infinity = np.mean(dn_rise[:-1000])
    e_square = np.mean(field[end - 1000:end])**2

    keys = ["Rise", "Rise_scaled", "s_rise_fit", "Rise_time", 'Rise_time_std',
            "Fall", "Fall_scaled", "s_fall_fit", "Fall_time", 'Fall_time_std',
            "Rise_c1", "Rise_c2", "Rise_D", "Fall_c1", "Fall_D",
            'Sample_rate',
            'dn', 'time',
            'e_square', 'dn_infinity',
            'aspect_ratio',
            'reg_times', 'reg_values']

    # intensity[end + 100:] = sgf(intensity[end + 100:], window_length=551, polyorder=1)
    results = [dn_rise, get_scale(dn_rise_std), s_rise_fit, rise_time, time_rise_std,
               dn_fall, get_scale(dn_fall_std), s_fall_fit, relaxation_time, time_fall_std,
               c1_rise, c2_rise, d_rise, c1_fall, d_fall,
               sample_rate,
               bg_sub(intensity, config), time,
               e_square, dn_infinity,
               aspect_ratio,
               reg_times, reg_values]

    return dict(zip(keys, results))


def process_database(pulse_selection=None,
                     conc_selection=None) -> None:
    """
    Processes selected groups and stores computed results in a new HDF5 database.
    """

    config = get_experiment_config()
    raw_hdf_filename = os.path.join(config.base_dirs.database, "experiment_data_pulses.h5")
    processed_hdf_filename = os.path.join(config.base_dirs.database, "processed_experiment_data.h5")

    pulse_selection = ['100', '150', '200', '300']
    conc_selection = ["00156", "00312", "00625"]

    group_paths = generate_group_paths(config, pulse_selection, conc_selection)
    existing_groups = get_existing_groups(raw_hdf_filename, group_paths)

    if not existing_groups:
        print("❌ No matching groups found in the database.")
        return

    with h5py.File(raw_hdf_filename, 'r') as raw_hdf, h5py.File(processed_hdf_filename, 'w') as processed_hdf:
        pbar = tqdm(existing_groups, desc="Processing Groups", leave=True, dynamic_ncols=True)

        for group in pbar:
            pbar.set_description(f"Processing: {group}")  # Inline update without new lines
            processed_group = processed_hdf.create_group(group)

            for dataset in raw_hdf[group]:

                st, end, _, _, accept = (lambda b: (b.st, b.end, b.tr1, b.tr2, b.accept))(
                        config.directories.boundaries.get(f'{group}/{dataset}', None))
                if accept == 0:
                    continue

                results = interpret_dataset(np.array(raw_hdf[group][dataset][:]), config, group, dataset)

                dataset_group = processed_group.create_group(dataset)
                for key, value in results.items():
                    if isinstance(value, (int, float, np.generic)):
                        dataset_group.create_dataset(key, data=value)
                    else:
                        dataset_group.create_dataset(key, data=value, compression="gzip")

        pbar.close()
        print("✅ Processing & storage complete.")


if __name__ == '__main__':
    process_database()
    # plt.plot(rise_time, s_rise)
    # plt.plot(rise_time, s_rise_fit)
    # plt.plot(relaxation_time, s_relaxation)
    # plt.plot(relaxation_time, s_relaxation_fit)
    # index_ss = steady_state_index(dn_rise)

    # plt.plot(time_rise_std, dn_rise_std)
    # plt.plot( rise_time,dn_rise)
    # plt.title(f'{group}/{dataset} / {c1_rise}/ {c2_rise}/ {d_rise}')
    # plt.show()

    # plt.plot(time_fall_std, dn_fall_std)
    # plt.show()
    # plt.plot(tau, x)
    # plt.show()

    # plt.plot(time_rise_std, dn_rise_std)
    # plt.plot(rise_time, dn_rise)
    # plt.plot(time_fall_std, dn_fall_std)
    # plt.plot(relaxation_time, dn_relaxation)
