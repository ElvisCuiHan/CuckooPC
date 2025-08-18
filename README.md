<p align="center">
  <img src="figures/cuckoopc.png" alt="CuckooPC Simulation Demo" width="500"/>
</p>

# <span style="color:#4A90E2;">CuckooPC-Simulation</span>

<span style="color:#4A90E2; font-weight:bold;">CuckooPC-Simulation</span> is a Python project for 
<span style="color:#E67E22; font-weight:bold;">principal curve estimation</span> 
that combines both classical and metaheuristic algorithms. It features:

- <span style="color:#27AE60; font-weight:bold;">Hastie & Stuetzle algorithm</span> – A classical principal curve fitting approach.
- <span style="color:#F39C12; font-weight:bold;">Particle Swarm Optimization (PSO)</span> – A population-based optimization heuristic.
- <span style="color:#9B59B6; font-weight:bold;">Cuckoo Search (CS)</span> – A Lévy flight-based metaheuristic algorithm.

This repository provides a **flexible framework** for:
- <span style="color:#2C3E50;">Nonlinear curve fitting and smoothing</span>.
- <span style="color:#2C3E50;">Quantitative analysis and comparison of algorithms</span>.
- <span style="color:#2C3E50;">Visualization and benchmarking</span> on complex curve shapes 
(e.g., <span style="color:#E74C3C;">Spiral</span>, <span style="color:#3498DB;">Heart</span>, 
<span style="color:#8E44AD;">Butterfly</span>, <span style="color:#27AE60;">Pedal</span>, 
<span style="color:#F1C40F;">Elvis</span>).

---

## <span style="color:#16A085;">Key Features</span>
- **Multiple Algorithms**: Compare classical and modern metaheuristic approaches.
- **Performance Metrics**: Evaluate algorithms using:
  - <span style="color:#E67E22;">L2 distance</span> to the true curve.
  - <span style="color:#3498DB;">Data fitting quality</span>.
  - <span style="color:#8E44AD;">Hausdorff distance</span>.
  - <span style="color:#27AE60;">Length preservation</span>.
  - <span style="color:#F39C12;">Computation time</span>.
- **Visualization Utilities**: Generate performance bar charts and LaTeX tables for reporting.

---

## <span style="color:#2980B9;">Repository Structure</span>
```
CuckooPC-Simulation/
│
├── cuckoopc/           # Core modules
│   ├── pso.py          # PSO-based principal curve estimation
│   ├── cuckoo.py       # Cuckoo Search-based principal curve estimation
│   ├── smoothers.py    # Spline fitting and loss functions
│   └── comparison.py   # Visualization and performance evaluation
│
├── notebooks/          # Jupyter notebooks for experiments
└── tests/              # Unit tests and validation scripts
```

---

## <span style="color:#8E44AD;">Installation</span>
```bash
git clone https://github.com/your-username/CuckooPC-Simulation.git
cd CuckooPC-Simulation
pip install -r requirements.txt
```

---

## <span style="color:#C0392B;">Quick Example</span>
```python
import numpy as np
from cuckoopc.pso import estimate_principal_curve_pso
from cuckoopc.cuckoo import estimate_principal_curve_cuckoo

# Example data
Y = np.random.rand(100, 2)

# Estimate curve using Cuckoo Search
curve_cs, omega_cs, cost_cs, history_cs = estimate_principal_curve_cuckoo(Y)

# Estimate curve using PSO
curve_pso, omega_pso, cost_pso, history_pso = estimate_principal_curve_pso(Y)
```
