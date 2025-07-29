"""
cuckoo.py
---------
Contains the Cuckoo Search (CS) implementation for principal curve estimation.
"""

import numpy as np
from .smoothers import cuckoo_objective, fit_smoother, eval_smoother

class SimpleCuckoo:
    """A simplified Cuckoo Search optimizer."""

    def __init__(self, n_nests=20, dimensions=100, pa=0.25, alpha=0.01):
        self.n_nests = n_nests
        self.dimensions = dimensions
        self.pa = pa
        self.alpha = alpha

    def _levy_flight(self, beta=1.5):
        sigma = (np.math.gamma(1 + beta) * np.sin(np.pi * beta / 2) /
                 (np.math.gamma((1 + beta) / 2) * beta * 2**((beta - 1)/2)))**(1/beta)
        u = np.random.normal(0, sigma, self.dimensions)
        v = np.random.normal(0, 1, self.dimensions)
        step = u / (np.abs(v)**(1/beta))
        return step

    def optimize(self, objective_func, bounds, iters=100):
        lower_bound, upper_bound = bounds
        nests = np.random.uniform(lower_bound, upper_bound, (self.n_nests, self.dimensions))
        fitness = objective_func(nests)
        best_idx = np.argmin(fitness)
        best_nest = nests[best_idx].copy()
        best_score = fitness[best_idx]

        for _ in range(iters):
            new_nests = np.zeros_like(nests)
            for i in range(self.n_nests):
                step = self._levy_flight()
                new_pos = nests[i] + self.alpha * step * (nests[i] - best_nest)
                new_nests[i] = np.clip(new_pos, lower_bound, upper_bound)
            new_fitness = objective_func(new_nests)
            improved = new_fitness < fitness
            nests[improved] = new_nests[improved]
            fitness[improved] = new_fitness[improved]
            n_abandon = int(self.pa * self.n_nests)
            if n_abandon > 0:
                random_nests = np.random.uniform(lower_bound, upper_bound, (n_abandon, self.dimensions))
                worst_indices = np.argsort(-fitness)[:n_abandon]
                nests[worst_indices] = random_nests
                fitness[worst_indices] = objective_func(nests[worst_indices])
            current_best_idx = np.argmin(fitness)
            if fitness[current_best_idx] < best_score:
                best_score = fitness[current_best_idx]
                best_nest = nests[current_best_idx].copy()

        return best_score, best_nest


def estimate_principal_curve_cuckoo(Y, rho=1, max_iter=60, n_nests=20, verbose=True):
    """Estimate principal curves using Cuckoo Search."""
    n = len(Y)
    bounds = (np.zeros(n), np.ones(n))

    def scenario_objective(X):
        return cuckoo_objective(X, Y=Y, rho=rho)

    cuckoo = SimpleCuckoo(n_nests=n_nests, dimensions=n)
    cost, omega_opt = cuckoo.optimize(scenario_objective, bounds, iters=max_iter)
    omega_opt = np.sort(omega_opt)
    smooths_final = fit_smoother(omega_opt, Y)
    curve_est = eval_smoother(smooths_final, omega_opt)
    if verbose:
        print(f"Cuckoo Search completed, final cost: {cost:.4f}")
    history = [cost] * max_iter
    return curve_est, omega_opt, cost, history
