import sys

import h5py
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from pylab import mpl
# from tabulate import tabulate
from tabulate import tabulate
from configuration import get_experiment_config
from analizer import compute_induced_dipole, conver_p

if sys.platform == "darwin":
    mpl.use("macosx")

k_B = 1.38e-23  # Boltzmann constant (J/K)
T = 300  # Temperature (K)

epsilon_0 = 8.854e-12  # Permittivity of free space (F/m)
k_B = 1.38e-23  # Boltzmann constant (J/K)
T = 300  # Temperature in K
r = 10.5e-9  # Radius in meters (1 nm)
l = 150e-9  # Length in meters (150 nm)

def compute_c2(c1):
    """Compute c2 given c1 by solving for gamma."""
    gamma = sp.Symbol('gamma', real=True, positive=True)
    eq = sp.Eq(c1, (3 * gamma) / (2 * (gamma + 1)))
    gamma_solution = sp.solve(eq, gamma)
    if gamma_solution:
        gamma_value = float(gamma_solution[0])
        c2 = (gamma_value - 2) / (2 * (gamma_value + 1))
        return c2, gamma_value
    return None, None


def compute_delta_alpha_mu(c1, K):
    """Compute delta_alpha and mu given c1 and K."""
    c2, gamma_value = compute_c2(c1)
    if c2 is None:
        return None, None, None

    delta_alpha = (15 * k_B * T * K) / (gamma_value + 1)
    mu = k_B * T * np.sqrt(15 * K * gamma_value / (gamma_value + 1))
    mu_debye = mu /  3.33564e-30
    return delta_alpha, mu, mu_debye


def load_group_data(group):
    e_squared, dn_infinity = [], []
    rise_c1, rise_c2, rise_d, fall_c1, fall_d = [], [], [], [], []

    for filename in group:
        dataset = group[filename]
        if "e_square" in dataset:
            e_squared.append(np.array(dataset["e_square"]))
        if "dn_infinity" in dataset:
            dn_infinity.append(np.array(dataset["dn_infinity"]))
        if "Rise_c1" in dataset:
            rise_c1.append(np.array(dataset["Rise_c1"]))
        if "Rise_c2" in dataset:
            rise_c2.append(np.array(dataset["Rise_c2"]))
        if "Rise_D" in dataset:
            rise_d.append(np.array(dataset["Rise_D"]))
        if "Fall_c1" in dataset:
            fall_c1.append(np.array(dataset["Fall_c1"]))
        if "Fall_D" in dataset:
            fall_d.append(np.array(dataset["Fall_D"]))

    if not e_squared or not dn_infinity:
        return None, None, None, None, None, None, None, None, None

    e_squared = np.array(e_squared).flatten()
    dn_infinity = np.array(dn_infinity).flatten()
    rise_c1 = np.array(rise_c1).flatten()
    rise_c2 = np.array(rise_c2).flatten()
    rise_d = np.array(rise_d).flatten()
    fall_c1 = np.array(fall_c1).flatten()
    fall_d = np.array(fall_d).flatten()

    if e_squared.size == 0 or dn_infinity.size == 0:
        return None, None, None, None, None, None, None, None, None

    sort_idx = np.argsort(e_squared)
    return (e_squared[sort_idx], dn_infinity[sort_idx], rise_c1[sort_idx],
            rise_c2[sort_idx], rise_d[sort_idx], fall_c1[sort_idx], fall_d[sort_idx])


def plot_all_kerr_data(concentrations, pulses):
    config = get_experiment_config()

    processed_hdf_path = '/Users/alisher/IdeaProjects/TEB_REMAKE/databases/processed_experiment_data.h5'
    data = {conc: {} for conc in concentrations}

    with h5py.File(processed_hdf_path, 'r') as hdf_file:
        for conc in concentrations:
            for pulse in pulses:
                group_path = f"{conc}/0/{pulse}"
                if group_path not in hdf_file:
                    print(f"❌ {group_path} not found")
                    continue

                e_sq, dn_inf, rise_c1, rise_c2, rise_d, fall_c1, fall_d = load_group_data(hdf_file[group_path])
                data[conc][pulse] = (e_sq, dn_inf, rise_c1, rise_c2, rise_d, fall_c1, fall_d)

    added_to_legend = {pulse: False for pulse in pulses}
    table_data = []
    fig = go.Figure()
    print(concentrations)
    for conc in concentrations:

        for pulse, (e_sq, dn_inf, rise_c1, rise_c2, rise_d, fall_c1, fall_d) in data[conc].items():
            show_in_legend = not added_to_legend[pulse]
            added_to_legend[pulse] = True
            slope, intercept = np.polyfit(e_sq, dn_inf, 1)
            volume_fraction = lambda c: (c / 1.5) / (c / 1.5 + (100 - c) / 1.113)  # c in %
            vf = volume_fraction(float(conc) / 10000)
            delta_alpha, mu, mu_debye = compute_delta_alpha_mu(np.mean(rise_c1), (slope / 1e4) / (vf * 100))

            table_data.append(
                    [float(conc) / 10000,
                     vf * 100,
                     pulse,
                     intercept,
                     slope / 1e4,
                     (slope / 1e4) / (vf * 100),
                     np.mean(fall_d) * 1e3,
                     delta_alpha, mu_debye])

    headers = ["Concentration",
               "Volume_fraction",
               "Pulse",
               "intercept",
               "Kerr_unscaled",
               "Kerr_scaled",
               "Fall_D",
               "Delta_alpha",
               "mu"]

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    concentrations = ['00156', '00312', '00625']
    pulse_widths = ['100', '150', '200', '300']
    plot_all_kerr_data(concentrations, pulse_widths)
