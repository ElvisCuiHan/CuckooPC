# Novel Applications of Cuckoo Search: Design, Bioinformatics, and Big Data

<p align="center">
  <img src="cuckoopc.jpg" alt="Banner" width="80%"/>
</p>

<p align="center">
A nature-inspired optimization toolkit across disciplines: from experimental design to single-cell analysis
</p>

<p align="center">
  <a href="https://www.r-project.org/"><img src="https://img.shields.io/badge/R-4.0+-blue.svg" alt="R"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-green.svg" alt="Python"></a>
  <a href="https://shiny.rstudio.com/"><img src="https://img.shields.io/badge/Shiny-1.7+-brightgreen.svg" alt="Shiny"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <a href="#"><img src="https://img.shields.io/badge/DOI-10.1016%2Fj.procs.2025.xx.xxx-blue.svg" alt="DOI"></a>
</p>

<p align="center">
🚀 <a href="#quick-start">Quick Start</a> • 📱 <a href="#-interactive-application">Interactive App</a> • 📖 <a href="#-paper">Paper</a> • 🔍 <a href="#examples">Examples</a> • 🤝 <a href="#-contribution">Contribution</a>
</p>

---

## 🎯 What is this?

This repository contains the complete implementation of Cuckoo Search (CS) algorithm applications across three cutting-edge domains: optimal experimental design, bioinformatics parameter estimation, and principal curve estimation for big data analysis.

Our work demonstrates the power of nature-inspired metaheuristic algorithms in solving complex optimization problems across disciplines, with a particular focus on Operations Research methodology and data-driven decision support systems.

> 🔥 **Why Cuckoo Search?**  
> Unlike traditional optimization methods, CS excels at navigating complex, non-convex landscapes with **global search capabilities** and **minimal parameter tuning**. Perfect for real-world problems where gradients don't exist or are unreliable.

---

## 🌟 Key Applications

### Optimal Experimental Design
- **Challenge**: Find D-optimal exact designs for EMAX models with correlated errors and small sample sizes  
- **Solution**: CS algorithm for locally optimal designs with autoregressive AR(1) covariance structures  
- **Features**: 3–5 observations per subject, efficiency evaluation, robustness to parameter misspecification  

### Single-Cell Gene Trajectory Analysis (scGTM)
- **Challenge**: Constrained maximum likelihood estimation for hill-shaped gene expression patterns  
- **Solution**: CS optimization for zero-inflated Poisson models with mixed continuous/discrete parameters  
- **Features**: Interactive R Shiny application, pseudotime modeling, biological pattern classification  

### Principal Curve Estimation
- **Challenge**: Estimate smooth curves through high-dimensional data clouds for dimensionality reduction  
- **Solution**: Metric-based principal curves using CS optimization with multiple distance functions  
- **Features**: 2D/3D visualization, six synthetic scenarios, comparison with classical Hastie–Stuetzle algorithm  

---

## 🚀 Quick Start {#quick-start}

### Repository Structure
```bash
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
└── README.md           # This file
```

## 🚀 Installation

Clone the repository and install Python dependencies:

```bash
git clone https://github.com/ElvisCuiHan/CuckooPC.git
cd CuckooPC
pip install -r requirements.txt
```

Install R dependencies:

```{r}
install.packages(c('shiny', 'shinydashboard', 'DT', 'plotly', 'ggplot2', 'dplyr', 'MASS', 'pracma'))
```

---

## 📱 Interactive Application

### 🧬 scGTM Analysis Tool

Live Demo: [https://heatheryu.shinyapps.io/scGTMApp/](https://heatheryu.shinyapps.io/scGTMApp/)

A comprehensive R Shiny application for single-cell gene trajectory modeling with Cuckoo Search optimization.

### Features

- Real-time parameter estimation for scGTM models  
- Support for multiple distributions (ZIP, ZINB, Poisson, NB)  
- Interactive visualization of gene expression patterns  
- Export results and plots  

---

## 🔍 Examples

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

---

## 📖 Paper

#### 💭 How to Cite
If you use this work, please cite:

```bibtex
@article{cui2025cuckoo,
  title   = {Novel Applications of Cuckoo Search to Tackle Design, Bioinformatics, and Big Data Problems},
  author  = {Cui, Elvis Han and Yu, Heather Xihe and Qi, Guanghao and Wong, Weng Kee},
  journal = {Procedia Computer Science},
  volume  = {00},
  pages   = {1--22},
  year    = {2025},
  publisher = {Elsevier},
  note    = {Preprint under review},
  url     = {https://github.com/ElvisCuiHan/CuckooPC}
}

```

#### 🔗 Theoretical Foundation
Built upon key methodological advances in:

- [Cuckoo Search optimization (Yang & Deb, 2009)](https://doi.org/10.1109/NABIC.2009.5393690)  
- [D-optimal design theory (Atkinson, Donev & Tobias, 2007)](https://doi.org/10.1007/978-0-387-98135-6)  
- [Single-cell trajectory analysis (Trapnell et al., 2014, *Nature Biotechnology*)](https://doi.org/10.1038/nbt.2859)  
- [Principal curve estimation techniques (Hastie & Stuetzle, 1989, *JASA*)](https://doi.org/10.1080/01621459.1989.10478797)  

---

## 🤝 Contribution

We welcome contributions to improve and extend this work! Whether it's bug fixes, new features, or additional applications of the Cuckoo Search algorithm, your input is valuable.

### 👥 Contributors

- [**@ElvisCuiHan**](https://github.com/ElvisCuiHan) - Original implementation and research  
- [**@roxberry119**](https://github.com/roxberry119) - Single-cell genomics application  

### 🚀 How to Contribute

Feel free to:  
- Report issues or suggest improvements  
- Submit pull requests for bug fixes  
- Propose new applications or extensions  
- Improve documentation and examples  

For major changes, please open an issue first to discuss your ideas.

---

**Questions?** Feel free to reach out through GitHub issues or email [elviscuihan@g.ucla.edu](mailto:elviscuihan@g.ucla.edu)
