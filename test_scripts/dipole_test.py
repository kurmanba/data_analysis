import numpy as np
import sympy as sp

def compute_c1_c2(gamma):
    """Compute c1 and c2 given gamma"""
    if gamma <= 0:
        return None, None
    c1 = (3 * gamma) / (2 * (gamma + 1))
    c2 = (gamma - 2) / (2 * (gamma + 1))
    return c1, c2

def find_closest_coefficients(exp_data):
    """Find closest valid (c1, c2) pairs to experimental data"""

    gamma_values = np.logspace(-2, 2, 500)  # Sweep gamma from 0.01 to 100
    valid_c1, valid_c2 = [], []

    for gamma in gamma_values:
        c1, c2 = compute_c1_c2(gamma)
        if c1 is not None and c2 is not None:
            valid_c1.append(c1)
            valid_c2.append(c2)

    valid_c1 = np.array(valid_c1)
    valid_c2 = np.array(valid_c2)

    closest_points = []

    for c1_exp, c2_exp in exp_data:
        distances = np.sqrt((valid_c1 - c1_exp) ** 2 + (valid_c2 - c2_exp) ** 2)
        min_idx = np.argmin(distances)
        closest_points.append((c1_exp, c2_exp, valid_c1[min_idx], valid_c2[min_idx], distances[min_idx]))

    return closest_points

def compute_delta_alpha_mu(c1, c2, K_avg, k_B, T):
    """Compute delta_alpha and mu given c1, c2, and K_avg"""
    mu, delta_alpha, gamma = sp.symbols('mu delta_alpha gamma', real=True, positive=True)
    gamma_expr = mu**2 / (delta_alpha * k_B * T)

    eq1 = sp.Eq(c1, (3 * gamma) / (2 * (gamma + 1)))
    eq2 = sp.Eq(c2, (gamma - 2) / (2 * (gamma + 1)))

    gamma_solution = sp.solve([eq1, eq2], gamma)
    if not gamma_solution:
        raise ValueError("No valid solution for gamma.")
    gamma_value = gamma_solution[gamma]

    eq3 = sp.Eq(K_avg, (1/15) * ((mu**2 / (k_B * T)) + (delta_alpha / (k_B * T))))
    mu_expr = sp.sqrt(gamma_value * delta_alpha * k_B * T)
    eq3_substituted = eq3.subs(mu, mu_expr)

    delta_alpha_solution = sp.solve(eq3_substituted, delta_alpha)
    if not delta_alpha_solution:
        raise ValueError("No valid solution for delta_alpha.")

    delta_alpha_value = delta_alpha_solution[0]
    mu_value = mu_expr.subs(delta_alpha, delta_alpha_value)

    return float(delta_alpha_value), float(mu_value)

exp_headers = {'c1': 0, 'c2': 1, 'K_avg': 2}
exp_data = np.array([
        [1.09616, 0.114423, 1.28889e-11],
        [1.03665, 0.0649933, 1.39406e-11],
        [1.0329,  0.0640926, 1.43246e-11],
        [1.06619, 0.083214, 1.08861e-11],
        [1.02375, 0.0240804, 2.44078e-11],
        [0.979454, 0.00715783, 2.87981e-11],
        [0.942307, 2.70987e-16, 2.75802e-11],
        [0.930934, 6.42636e-17, 2.3812e-11],
        [1.05196, 0.0940654, 4.12309e-11],
        [1.19517, 0.228734, 4.1108e-11],
        [1.03661, 0.0742418, 3.92186e-11],
        [0.950166, 0.00129494, 4.12827e-11]
])

k_B = 1.38e-23  # Boltzmann constant in J/K
T = 300  # Temperature in K
closest_results = find_closest_coefficients(exp_data[:, :2])
print("Experimental c1, c2  ->  Closest Valid c1, c2  |  Delta Alpha (Cm²/V)  |  Mu (Cm)")
print("-" * 90)

for i, (c1_exp, c2_exp, c1_valid, c2_valid, distance) in enumerate(closest_results):
    K_avg = exp_data[i, 2]

    try:
        delta_alpha, mu = compute_delta_alpha_mu(c1_valid, c2_valid, K_avg, k_B, T)
        print(f"({c1_exp:.5f}, {c2_exp:.5f}) -> ({c1_valid:.5f}, {c2_valid:.5f}) | {delta_alpha:.5e} | {mu:.5e}")
    except ValueError:
        print(f"({c1_exp:.5f}, {c2_exp:.5f}) -> ({c1_valid:.5f}, {c2_valid:.5f}) | No valid solution")
