import os

import h5py
import pandas as pd
from tqdm import tqdm

from configuration import get_experiment_config


def read_oscilloscope_csv(file_path):
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

    return df.apply(pd.to_numeric, errors='coerce').to_numpy()


def collect_csv_files(directory, recursive=False):
    """
    Collects all CSV file paths in the given directory.
    """
    csv_files = []
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return csv_files

    if recursive:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith('.csv'):
                    csv_files.append(os.path.join(root, filename))
    else:
        for filename in os.listdir(directory):
            if filename.lower().endswith('.csv'):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    csv_files.append(file_path)
    return csv_files


def create_hdf_database():
    config = get_experiment_config()
    hdf_filename = os.path.join(config.base_dirs.database, "experiment_data_pulses.h5")
    raw_data_base = config.base_dirs.raw_folder

    with h5py.File(hdf_filename, 'w') as hdf:

        pbar = tqdm(config.potentials.concentrations,
                    desc="Concentrations",
                    leave=True,
                    dynamic_ncols=True)

        for conc in pbar:
            pbar.set_description(f"Processing: {conc:>10}")  # Keeps the description inline
            conc_group = hdf.create_group(conc)

            for flow in config.potentials.flows:
                flow_group = conc_group.create_group(str(flow))
                for pulse in config.potentials.pulse_width:
                    pulse_group = flow_group.create_group(str(pulse))
                    dir_path = os.path.join(raw_data_base, conc, str(flow), str(pulse))
                    csv_files = collect_csv_files(dir_path, recursive=False)

                    if not csv_files:
                        tqdm.write(f"⚠️ No CSV files found in {dir_path}")
                    for csv_file in csv_files:
                        try:
                            data = read_oscilloscope_csv(csv_file)
                        except Exception as e:
                            tqdm.write(f"❌ Skipping {csv_file} due to error: {e}")
                            continue

                        dset_name = os.path.splitext(os.path.basename(csv_file))[0]
                        pulse_group.create_dataset(dset_name, data=data)

        pbar.close()

    print("✅ HDF5 database creation complete.")


if __name__ == '__main__':
    create_hdf_database()
