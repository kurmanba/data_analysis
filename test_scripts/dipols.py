import sys

from pylab import mpl

if sys.platform == "darwin":
    mpl.use("macosx")

import numpy as np
import matplotlib.pyplot as plt

# Your experimental data (c1, c2 values)
exp_data = np.array([
        [1.09616, 0.114423],
        [1.03665, 0.0649933],
        [1.0329, 0.0640926],
        [1.06619, 0.083214],
        [1.02375, 0.0240804],
        [0.979454, 0.00715783],
        [0.942307, 2.70987e-16],
        [0.930934, 6.42636e-17],
        [1.05196, 0.0940654],
        [1.19517, 0.228734],
        [1.03661, 0.0742418],
        [0.950166, 0.00129494]
])


def compute_c1_c2(gamma):
    """Compute c1 and c2 given gamma"""
    if gamma <= 0:  # Physically invalid
        return None, None
    c1 = (3 * gamma) / (2 * (gamma + 1))
    c2 = (gamma - 2) / (2 * (gamma + 1))
    return c1, c2


def plot_valid_coefficients_with_data(exp_data):
    """Plots valid (c1, c2) pairs with a heatmap of gamma and overlays experimental data"""

    gamma_values = np.logspace(-2, 2, 500)  # Sweep gamma from 0.01 to 100
    c1_list, c2_list = [], []

    for gamma in gamma_values:
        c1, c2 = compute_c1_c2(gamma)
        if c1 is not None and c2 is not None:
            c1_list.append(c1)
            c2_list.append(c2)

    c1_array = np.array(c1_list)
    c2_array = np.array(c2_list)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(c1_array, c2_array, c=np.log10(gamma_values), cmap='coolwarm', edgecolor='k', alpha=0.8)

    # Overlay experimental data
    plt.scatter(exp_data[:, 0], exp_data[:, 1], color='black', marker='x', s=100, label="Experimental Data")

    # Labels and legend
    plt.colorbar(scatter, label=r'$\log_{10}(\gamma)$')
    plt.xlabel(r'$c_1$')
    plt.ylabel(r'$c_2$')
    plt.title("Valid Coefficient Region for $(c_1, c_2)$ with Experimental Data")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()


# Call the function to generate the plot with your data
# Given values
mu = 1.5e-26  # Dipole moment in C·m
delta_alpha = 2e-32  # Polarizability in C·m^2/V
k_B = 1.38e-23  # Boltzmann constant in J/K
T = 300  # Temperature in K

# Calculate the Kerr constant K_0
K_0 = (1 / 15) * ((mu / (k_B * T))**2 + (delta_alpha / (k_B * T)))
K_1 = np.sqrt(k_B*T*delta_alpha)

print(K_0, K_1)

plot_valid_coefficients_with_data(exp_data)
