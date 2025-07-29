# CuckooPC-Simulation

This repository implements **Principal Curve Estimation** using:
1. The classical **Hastie & Stuetzle algorithm**.
2. A **Particle Swarm Optimization (PSO)** approach.
3. A **Cuckoo Search (CS)** metaheuristic algorithm.

The project provides simulation experiments on various curve shapes 
(Spiral, Heart, Butterfly, Pedal, Elvis) and compares the performance 
of PSO and Cuckoo algorithms in terms of:

- **L2 Distance to the true curve**
- **Data fitting quality**
- **Hausdorff distance**
- **Length preservation**
- **Computation time**

---

## **Repository Structure**
- `cuckoopc/`: Core modules
  - `pso.py`: PSO-based curve estimation.
  - `cuckoo.py`: Cuckoo Search-based curve estimation.
  - `smoothers.py`: Spline-based smoother utilities.
  - `comparison.py`: Functions for performance evaluation and visualization.
- `notebooks/`: Jupyter notebooks for experiments.
- `tests/`: Unit tests and verification scripts.

---

## **Installation**
```bash
git clone https://github.com/your-username/CuckooPC-Simulation.git
cd CuckooPC-Simulation
pip install -r requirements.txt
