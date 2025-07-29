"""
pso.py
------
Contains the Particle Swarm Optimization (PSO) implementation for principal curve estimation.
"""

import numpy as np
from .smoothers import pso_objective, fit_smoother, eval_smoother

class SimplePSO:
    """A simplified PSO optimizer for principal curve estimation."""

    def __init__(self, n_particles=20, dimensions=100, w=0.7, c1=1.5, c2=1.5):
        self.n_particles = n_particles
        self.dimensions = dimensions
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def optimize(self, objective_func, bounds, iters=100):
        lower_bound, upper_bound = bounds
        positions = np.random.uniform(lower_bound, upper_bound, (self.n_particles, self.dimensions))
        velocities = np.random.uniform(-1, 1, (self.n_particles, self.dimensions))
        fitness = objective_func(positions)
        pbest_positions = positions.copy()
        pbest_fitness = fitness.copy()
        gbest_idx = np.argmin(fitness)
        gbest_position = positions[gbest_idx].copy()
        gbest_fitness = fitness[gbest_idx]

        for _ in range(iters):
            r1, r2 = np.random.random((2, self.n_particles, self.dimensions))
            velocities = (self.w * velocities +
                          self.c1 * r1 * (pbest_positions - positions) +
                          self.c2 * r2 * (gbest_position - positions))
            positions = np.clip(positions + velocities, lower_bound, upper_bound)
            fitness = objective_func(positions)
            better_mask = fitness < pbest_fitness
            pbest_positions[better_mask] = positions[better_mask]
            pbest_fitness[better_mask] = fitness[better_mask]
            current_best_idx = np.argmin(fitness)
            if fitness[current_best_idx] < gbest_fitness:
                gbest_position = positions[current_best_idx].copy()
                gbest_fitness = fitness[current_best_idx]

        return gbest_fitness, gbest_position


def estimate_principal_curve_pso(Y, rho=1, max_iter=60, n_particles=20, verbose=True):
    """Estimate principal curves using PSO."""
    n = len(Y)
    bounds = (np.zeros(n), np.ones(n))

    def scenario_objective(X):
        return pso_objective(X, Y=Y, rho=rho)

    pso = SimplePSO(n_particles=n_particles, dimensions=n)
    cost, omega_opt = pso.optimize(scenario_objective, bounds, iters=max_iter)
    omega_opt = np.sort(omega_opt)
    smooths_final = fit_smoother(omega_opt, Y)
    curve_est = eval_smoother(smooths_final, omega_opt)
    if verbose:
        print(f"PSO completed, final cost: {cost:.4f}")
    history = [cost] * max_iter
    return curve_est, omega_opt, cost, history
