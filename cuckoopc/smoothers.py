"""
smoothers.py
------------
Contains utility functions for spline fitting and loss evaluation.
"""

import numpy as np
from scipy.interpolate import UnivariateSpline

def eval_smoother(smooths, omega):
    return np.stack([s(omega) for s in smooths], axis=1)

def fit_smoother(omega, Y, s=2):
    idx = np.argsort(omega)
    omega_sorted = omega[idx]
    Y_sorted = Y[idx]
    smooths = []
    for j in range(Y.shape[1]):
        us = UnivariateSpline(omega_sorted, Y_sorted[:, j], s=s)
        smooths.append(us)
    return smooths

def loss_fn(omega, Y, rho=1, penalty_large=1e6):
    if np.any(np.diff(np.sort(omega)) <= 0):
        return penalty_large
    smooths = fit_smoother(omega, Y)
    Yhat = eval_smoother(smooths, omega)
    mse = np.mean(np.sum((Y - Yhat)**2, axis=1))
    penalty = rho * np.sum(np.abs(np.diff(np.sort(omega))))
    return mse + penalty

def pso_objective(X, Y=None, rho=1):
    return np.array([loss_fn(np.clip(omega, 0, 1), Y, rho) for omega in X])

def cuckoo_objective(X, Y=None, rho=1):
    return np.array([loss_fn(np.clip(omega, 0, 1), Y, rho) for omega in X])
