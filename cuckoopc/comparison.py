"""
comparison.py
--------------
Contains functions for visualizing and comparing algorithm performance.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_comparison_bar_charts(results):
    scenarios_list = list(results.keys())
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    x = np.arange(len(scenarios_list))
    width = 0.35

    # Distance to True Curve
    ax = axes[0, 0]
    hastie_vals = [results[s]['metrics']['hastie_to_true'] for s in scenarios_list]
    cuckoo_vals = [results[s]['metrics']['cuckoo_to_true'] for s in scenarios_list]
    ax.bar(x - width/2, hastie_vals, width, label='Hastie', color='red', alpha=0.7)
    ax.bar(x + width/2, cuckoo_vals, width, label='Cuckoo', color='purple', alpha=0.7)
    ax.set_title('Distance to True Curve', fontsize=14, weight='bold')
    ax.set_ylabel('Distance')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios_list, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Data Fitting Quality
    ax = axes[0, 1]
    hastie_vals = [results[s]['metrics']['hastie_data_fit'] for s in scenarios_list]
    cuckoo_vals = [results[s]['metrics']['cuckoo_data_fit'] for s in scenarios_list]
    ax.bar(x - width/2, hastie_vals, width, label='Hastie', color='red', alpha=0.7)
    ax.bar(x + width/2, cuckoo_vals, width, label='Cuckoo', color='purple', alpha=0.7)
    ax.set_title('Data Fitting Quality', fontsize=14, weight='bold')
    ax.set_ylabel('Average Distance')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios_list, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Computation Time
    ax = axes[1, 0]
    hastie_vals = [results[s]['hastie_time'] for s in scenarios_list]
    cuckoo_vals = [results[s]['cuckoo_time'] for s in scenarios_list]
    ax.bar(x - width/2, hastie_vals, width, label='Hastie', color='red', alpha=0.7)
    ax.bar(x + width/2, cuckoo_vals, width, label='Cuckoo', color='purple', alpha=0.7)
    ax.set_title('Computation Time', fontsize=14, weight='bold')
    ax.set_ylabel('Time (seconds)')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios_list, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Length Preservation
    ax = axes[1, 1]
    hastie_vals = [results[s]['metrics']['hastie_length_ratio'] for s in scenarios_list]
    cuckoo_vals = [results[s]['metrics']['cuckoo_length_ratio'] for s in scenarios_list]
    ax.bar(x - width/2, hastie_vals, width, label='Hastie', color='red', alpha=0.7)
    ax.bar(x + width/2, cuckoo_vals, width, label='Cuckoo', color='purple', alpha=0.7)
    ax.axhline(y=1, color='green', linestyle='--', alpha=0.7, label='Perfect')
    ax.set_title('Length Preservation', fontsize=14, weight='bold')
    ax.set_ylabel('Length Ratio')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios_list, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("performance_comparison.png", dpi=300, bbox_inches='tight')
    plt.show()
