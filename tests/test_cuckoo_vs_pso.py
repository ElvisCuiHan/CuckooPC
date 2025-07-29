"""
test_cuckoo_vs_pso.py
---------------------
Basic test script for comparing Cuckoo Search and PSO on the Ackley function
and a simple synthetic dataset for principal curve estimation.
"""

import numpy as np
from cuckoopc.pso import estimate_principal_curve_pso
from cuckoopc.cuckoo import estimate_principal_curve_cuckoo

# Ackley function for optimizer testing
def ackley(x):
    x = np.array(x)
    d = len(x)
    term1 = -20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / d))
    term2 = -np.exp(np.sum(np.cos(2 * np.pi * x)) / d)
    return term1 + term2 + 20 + np.e

def test_ackley_optimizers():
    n_dim = 5
    Y_dummy = np.random.rand(50, 2)

    # PSO-based curve estimation
    curve_pso, omega_pso, cost_pso, _ = estimate_principal_curve_pso(Y_dummy, rho=1, max_iter=30, n_particles=15)
    print(f"[PSO] Final cost (dummy curve): {cost_pso:.4f}")

    # Cuckoo-based curve estimation
    curve_cuckoo, omega_cuckoo, cost_cuckoo, _ = estimate_principal_curve_cuckoo(Y_dummy, rho=1, max_iter=30, n_nests=15)
    print(f"[Cuckoo] Final cost (dummy curve): {cost_cuckoo:.4f}")

    # Basic Ackley function evaluation
    x0 = np.random.uniform(-5, 5, n_dim)
    print(f"Sample Ackley value at {x0[:3]}... = {ackley(x0):.4f}")

if __name__ == "__main__":
    test_ackley_optimizers()
