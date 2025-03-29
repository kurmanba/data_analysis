import math
import sys

import numpy as np
from pylab import mpl
from scipy.ndimage import gaussian_filter1d as gf
from scipy.optimize import curve_fit, fsolve, nnls
from scipy.signal import savgol_filter as sgf

if sys.platform == "darwin":
    mpl.use("macosx")


def i2delta_n(i_values: np.ndarray, config) -> np.ndarray:
    """
    Convert the intensity signal to birefringence.
    """
    d = config.optics.d
    lambda_ = config.optics.lambda_
    i_ref = config.optics.I_ref

    return (lambda_ / (np.pi * d)) * np.arcsin(np.sqrt(i_values / i_ref))


def double_rise(t: np.ndarray, d: float, c1: float, c2: float, p: float) -> np.ndarray:
    """
    Model for double rise.
    """
    return p * (1 - c1 * np.exp(-2 * d * t) + c2 * np.exp(-6 * d * t))


def double_fall(t: np.ndarray, d: float, c: float, t_0: float, b: float, config) -> np.ndarray:
    """
    Model for exponential fall with delay and baseline.
    """
    step = 0.5 * (1 + np.tanh(config.fit.exp_smoothing_factor * (t - t_0)))
    return c * (1 - step) + ((c - b) * np.exp(-6 * d * (t - t_0)) + b) * step


def compute_weights(s: np.ndarray, t: np.ndarray, config) -> np.ndarray:
    """
    Compute weights based on the absolute slope.
    """
    slope = np.abs(np.gradient(s, t))
    slope = np.where(slope < config.fit.gradient_threshold * np.max(slope), 0, slope)
    return 1 + config.fit.gradient_award * (slope / (np.max(slope) + 1e-5))


def find_consts_double_rise(s: np.ndarray, t: np.ndarray, config) -> tuple:
    """
    Curve fit for double rise.
    """
    weights = compute_weights(s, t, config)
    try:
        popt_rise, _ = curve_fit(double_rise,
                                 t,
                                 gf(s, 1),
                                 sigma=1 / weights,
                                 absolute_sigma=True,
                                 p0=[0.01, 1, 0.1, np.mean(s[::-500])],
                                 bounds=(0, np.inf))
    except ValueError:
        print("Value error occurred during double rise fitting.")
        popt_rise = (0, 0, 0, 0)
    return popt_rise


def find_consts_fall(s: np.ndarray, t: np.ndarray, config) -> tuple:
    """
    Curve fit for exponential fall.
    """
    try:
        weights = compute_weights(sgf(s, config.fit.sgf_window, 1), t, config)
    except np.linalg.LinAlgError:
        weights = compute_weights(gf(s, 2), t, config)

    s_shift = np.min(s[s > 0]) * 0.1 if np.any(s > 0) else 1e-6
    log_s = np.log(s + s_shift)
    try:
        slope, intercept = np.polyfit(t, log_s, 1, w=weights)
        t_0_guess = max(0, -intercept / slope)
        d_guess = abs(slope) / 6
    except (RuntimeError, np.linalg.LinAlgError) as e:
        print(e)
        t_0_guess = np.median(t)
        d_guess = config.fit.d_fall_guess

    c_guess = np.nan_to_num(np.mean(s[:100]), nan=1.0, posinf=1.0, neginf=1.0)
    b_guess = np.nan_to_num(np.mean(s[-100:]) - np.mean(s[:100]), nan=0.1)
    try:
        popt_fall, _ = curve_fit(
                lambda t, d, c, t_0, b: double_fall(t, d, c, t_0, b, config),
                t,
                s,
                sigma=1 / weights,
                absolute_sigma=True,
                p0=[d_guess, c_guess, t_0_guess, b_guess],
                bounds=([0, 0, 0, -np.inf], [np.inf, np.inf, np.inf, np.inf]),
        )
    except ValueError:
        print("Value error occurred during fall fitting: FIT FAILED TO CONVERGE!")
        popt_fall = (0, 0, 0, 0)
    return popt_fall


def bg_sub(signal: np.ndarray, config) -> np.ndarray:
    """
    Standard background subtraction.
    """
    dn = signal.copy()
    dn = i2delta_n(dn, config)
    dn -= np.min(dn)
    return dn


def regularization(t, y, config):
    """
    Applies regularization to the curve.
    Returns:
        dict: Dictionary with "Reg_times" and "Reg_values" keys.
    """
    t = t[t > 0]
    y = y[: len(t)]

    t_resampled = np.linspace(t.min(), t.max(), config.reg.n_tau)
    y_resampled = np.interp(t_resampled, t, y)

    t_min_safe = max(t_resampled.min(), 1e-8)
    t_max_safe = max(t_resampled.max(), 1e-8)
    tau_grid = np.logspace(np.log10(t_min_safe / 10), np.log10(t_max_safe * 0.8), config.reg.n_tau)

    A = np.vstack([np.exp(-t_resampled[:, None] / tau_grid[None, :]),
                   np.sqrt(config.reg.lambda_reg) * np.eye(config.reg.n_tau)])

    b = np.concatenate([y_resampled, np.zeros(config.reg.n_tau)])
    x, _ = nnls(A, b)

    return tau_grid, x


def get_scale(s: np.ndarray) -> np.ndarray:
    """Scale array values between 0 and 1, avoiding division errors."""
    s_copy = s.copy()
    min_val = np.min(s_copy)
    max_val = np.max(s_copy)

    if max_val - min_val == 0:
        return np.zeros_like(s_copy)
    s_copy -= min_val
    return s_copy / (max_val - min_val)


def conver_p(tau, config):
    """
    Converts tau to an aspect ratio.
    """
    eta = config.material.eta  # Viscosity from material config
    k_B = config.electric.k_b  # Boltzmann constant from electric config
    T = config.electric.T  # Temperature from electric config
    A = (math.pi * eta * config.material.diameter ** 3) / (3 * k_B * T)

    def F(p):
        if p <= 0:
            return float('inf')
        q = -0.662 + 0.917 / p - 0.050 / (p ** 2)
        return A * p ** 3 / (math.log(p) + q) - tau

    p_initial = 5.0
    p_solution, = fsolve(F, p_initial)

    return p_solution


def package(data) -> dict:
    """
    Packages data into a dictionary.
    """
    keys = ["Rise", "Rise_scaled", "Rise_time", "Fall", "Fall_scaled", "Fall_time", "Rise_c1", "Rise_c2",
            "Rise_D", "Fall_c1", "Fall_D", 'Sample_rate', 'dn', 'aspect_ratio']
    return dict(zip(keys, data))


def steady_state_index(dn_rise,
                            threshold_factor=0.01,
                            window_size=10,
                            percentage=0.95):
    """
    Determines the steady-state index in the rise of the pulse response.
    """
    if len(dn_rise) == 0:
        return 0  # Return 0 if input is empty

    # Compute the derivative
    derivative = np.abs(np.diff(dn_rise))
    threshold = threshold_factor * np.max(derivative)

    # Method 1: Using a threshold on the derivative
    steady_indices = np.where(derivative < threshold)[0]
    if len(steady_indices) > 0:
        return steady_indices[0]

    # Method 2: Using a moving average smoothing
    smoothed_rise = np.convolve(dn_rise, np.ones(window_size) / window_size, mode='valid')
    smoothed_derivative = np.abs(np.diff(smoothed_rise))
    steady_indices = np.where(smoothed_derivative < threshold)[0]
    if len(steady_indices) > 0:
        return steady_indices[0]

    steady_value = dn_rise[-1]
    steady_indices = np.where(dn_rise >= percentage * steady_value)[0]
    if len(steady_indices) > 0:
        return steady_indices[0]

    return len(dn_rise) - 1


if __name__ == "__main__":
    pass
