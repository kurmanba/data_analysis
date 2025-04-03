import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

k_B = 1.38e-23  # Boltzmann constant (J/K)
T = 300  # Temperature (K)
DEBYE_CONVERSION = 3.33564e-30  # Conversion factor to Debye

exp_data = np.array([[1.09616e+00, 1.28889e-15],
       [1.03665e+00, 1.39406e-15],
       [1.03290e+00, 1.43246e-15],
       [1.06619e+00, 1.08861e-15],
       [1.02375e+00, 2.44078e-15],
       [9.79454e-01, 2.87981e-15],
       [9.42307e-01, 2.75802e-15],
       [9.30934e-01, 2.38120e-15],
       [1.05196e+00, 4.12309e-15],
       [1.19517e+00, 4.11080e-15],
       [1.03661e+00, 3.92186e-15],
       [9.50166e-01, 4.12827e-15]])

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
    mu_debye = mu / DEBYE_CONVERSION
    return delta_alpha, mu, mu_debye

delta_alpha_values = []
mu_values = []
mu_debye_values = []
print("Computed values of μ and Δα:")
for c1, K in exp_data:
    delta_alpha, mu, mu_debye = compute_delta_alpha_mu(c1, K)
    if delta_alpha is not None and mu is not None:
        delta_alpha_values.append(delta_alpha)
        mu_values.append(mu)
        mu_debye_values.append(mu_debye)
        print(f"c1: {c1:.5f}, K: {K:.5e} -> Δα: {delta_alpha:.5e}, μ: {mu:.5e} C·m ({mu_debye:.5f} Debye)")
    else:
        delta_alpha_values.append(np.nan)
        mu_values.append(np.nan)
        mu_debye_values.append(np.nan)

delta_alpha_values = np.array(delta_alpha_values)
mu_values = np.array(mu_values)
mu_debye_values = np.array(mu_debye_values)

gamma_values = np.linspace(1.5, 2.5, 100)
Delta_alpha = (15 * k_B * T * exp_data[:, 1].mean()) / (gamma_values + 1)
dDelta_alpha_dgamma = - (15 * k_B * T * exp_data[:, 1].mean()) / (gamma_values + 1)**2
dmu_dgamma = (k_B * T * np.sqrt(15 * exp_data[:, 1].mean())) / (2 * np.sqrt(gamma_values) * (gamma_values + 1)**(3/2))

# Plot
# plt.figure(figsize=(8, 6))
# plt.plot(gamma_values, dDelta_alpha_dgamma, label=r'$\frac{d\Delta\alpha}{d\gamma}$', color='b')
# plt.plot(gamma_values, dmu_dgamma, label=r'$\frac{d\mu}{d\gamma}$', color='r', linestyle='dashed')
# plt.xlabel(r'$\gamma$')
# plt.ylabel('Sensitivity')
# plt.title('Sensitivities of $\Delta\alpha$ and $\mu$ with respect to $\gamma$ (near $\gamma=2$)')
# plt.axhline(0, color='black', linewidth=0.5, linestyle='dotted')
# plt.legend()
# plt.grid(True)
# plt.show()
