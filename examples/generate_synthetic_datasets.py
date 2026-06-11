#!/usr/bin/env python3
"""Generate the synthetic principal-curve datasets used in the paper.

The generated files correspond to the six scenarios in the manuscript:
Spiral I, Spiral II, Heart, Butterfly, Pedal, and Elvis.  The script writes
one CSV per scenario, plus a metadata JSON file recording the seed, sample
size, noise level, and analytic curve definition.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import splev, splprep


DEFAULT_SEED = 42
DEFAULT_N = 120


def _normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.where(norms < 1e-12, 1.0, norms)
    return vectors / norms


def _normal_noise_3d(rng: np.random.Generator, tangent: np.ndarray, sigma: float) -> np.ndarray:
    tangent = _normalize(tangent)
    raw = rng.normal(size=tangent.shape)
    projected = raw - np.sum(raw * tangent, axis=1, keepdims=True) * tangent
    return sigma * _normalize(projected)


def _normal_noise_2d(rng: np.random.Generator, tangent: np.ndarray, sigma: float) -> np.ndarray:
    tangent = _normalize(tangent)
    normal = np.column_stack([-tangent[:, 1], tangent[:, 0]])
    return sigma * rng.normal(size=(len(tangent), 1)) * normal


def _spiral_i(lam: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            np.sin(2 * np.pi * lam),
            np.exp(-lam),
            np.cos(2 * np.pi * lam),
        ]
    )


def _d_spiral_i(lam: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            2 * np.pi * np.cos(2 * np.pi * lam),
            -np.exp(-lam),
            -2 * np.pi * np.sin(2 * np.pi * lam),
        ]
    )


def _spiral_ii(lam: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            lam,
            2 * lam * np.cos(6 * lam),
            2 * lam * np.sin(6 * lam),
        ]
    )


def _d_spiral_ii(lam: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            np.ones_like(lam),
            2 * np.cos(6 * lam) - 12 * lam * np.sin(6 * lam),
            2 * np.sin(6 * lam) + 12 * lam * np.cos(6 * lam),
        ]
    )


def _heart(lam: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            16 * np.sin(lam) ** 3,
            13 * np.cos(lam) - 5 * np.cos(2 * lam) - 2 * np.cos(3 * lam) - np.cos(4 * lam),
            np.abs(np.sin(lam)),
        ]
    )


def _d_heart(lam: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            48 * np.sin(lam) ** 2 * np.cos(lam),
            -13 * np.sin(lam) + 10 * np.sin(2 * lam) + 6 * np.sin(3 * lam) + 4 * np.sin(4 * lam),
            np.cos(lam) * np.sign(np.sin(lam)),
        ]
    )


def _butterfly(lam: np.ndarray) -> np.ndarray:
    t = 2 * np.pi * lam
    r = np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12) ** 5
    return np.column_stack([np.sin(t) * r, np.cos(t) * r])


def _d_butterfly(lam: np.ndarray) -> np.ndarray:
    t = 2 * np.pi * lam
    dt = 2 * np.pi
    r = np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12) ** 5
    dr_dt = -np.exp(np.cos(t)) * np.sin(t) + 8 * np.sin(4 * t) - (
        5 * np.sin(t / 12) ** 4 * np.cos(t / 12) / 12
    )
    dx = np.cos(t) * r * dt + np.sin(t) * dr_dt * dt
    dy = -np.sin(t) * r * dt + np.cos(t) * dr_dt * dt
    return np.column_stack([dx, dy])


def _pedal(lam: np.ndarray) -> np.ndarray:
    r = np.cos(10 * np.pi * lam)
    theta = 2 * np.pi * lam
    return np.column_stack([r * np.cos(theta), r * np.sin(theta)])


def _d_pedal(lam: np.ndarray) -> np.ndarray:
    r = np.cos(10 * np.pi * lam)
    dr = -10 * np.pi * np.sin(10 * np.pi * lam)
    theta = 2 * np.pi * lam
    dtheta = 2 * np.pi
    dx = dr * np.cos(theta) - r * np.sin(theta) * dtheta
    dy = dr * np.sin(theta) + r * np.cos(theta) * dtheta
    return np.column_stack([dx, dy])


ELVIS_CONTROL_POINTS = np.array(
    [
        [-2.0, 1.4],
        [-1.6, 1.7],
        [-0.6, 1.6],
        [-1.4, 1.1],
        [-0.3, 0.8],
        [-1.5, 0.4],
        [-0.2, 0.1],
        [-1.1, -0.4],
        [-1.8, -1.1],
        [-0.7, -1.4],
        [0.0, -0.8],
        [0.5, -1.4],
        [1.3, -1.1],
        [0.7, -0.5],
        [1.6, 0.1],
        [0.5, 0.4],
        [1.4, 0.9],
        [0.2, 1.1],
        [1.1, 1.5],
        [2.0, 1.2],
    ],
    dtype=float,
)


def _elvis_spline():
    return splprep([ELVIS_CONTROL_POINTS[:, 0], ELVIS_CONTROL_POINTS[:, 1]], s=0.25, k=3, per=False)[0]


def _elvis(lam: np.ndarray, tck=None) -> np.ndarray:
    tck = _elvis_spline() if tck is None else tck
    return np.array(splev(lam, tck)).T


def _d_elvis(lam: np.ndarray, tck=None) -> np.ndarray:
    tck = _elvis_spline() if tck is None else tck
    return np.array(splev(lam, tck, der=1)).T


def generate_synthetic_datasets(seed: int = DEFAULT_SEED, n: int = DEFAULT_N) -> dict[str, dict[str, np.ndarray]]:
    """Generate all six synthetic datasets with fixed, reproducible randomness."""
    rng = np.random.default_rng(seed)
    datasets: dict[str, dict[str, np.ndarray]] = {}

    lam = np.sort(rng.uniform(-1, 1, n))
    true = _spiral_i(lam)
    datasets["spiral_i"] = {
        "lambda": lam,
        "observed": true + _normal_noise_3d(rng, _d_spiral_i(lam), sigma=0.1),
        "true": true,
    }

    lam = np.sort(rng.uniform(0, 2, n))
    true = _spiral_ii(lam)
    datasets["spiral_ii"] = {
        "lambda": lam,
        "observed": true + _normal_noise_3d(rng, _d_spiral_ii(lam), sigma=0.1),
        "true": true,
    }

    lam = np.sort(rng.uniform(1e-10, 2 * np.pi, n))
    true = _heart(lam)
    datasets["heart"] = {
        "lambda": lam,
        "observed": true + _normal_noise_3d(rng, _d_heart(lam), sigma=0.1),
        "true": true,
    }

    lam = np.sort(rng.uniform(0, 1, n))
    true = _butterfly(lam)
    datasets["butterfly"] = {
        "lambda": lam,
        "observed": true + _normal_noise_2d(rng, _d_butterfly(lam), sigma=0.05),
        "true": true,
    }

    lam = np.sort(rng.uniform(0, 1, n))
    true = _pedal(lam)
    datasets["pedal"] = {
        "lambda": lam,
        "observed": true + _normal_noise_2d(rng, _d_pedal(lam), sigma=0.05),
        "true": true,
    }

    lam = np.sort(rng.uniform(0, 1, n))
    tck = _elvis_spline()
    true = _elvis(lam, tck=tck)
    datasets["elvis"] = {
        "lambda": lam,
        "observed": true + _normal_noise_2d(rng, _d_elvis(lam, tck=tck), sigma=1.0),
        "true": true,
    }

    return datasets


def _metadata(seed: int, n: int) -> dict[str, object]:
    return {
        "seed": seed,
        "n_per_scenario": n,
        "format": "Each CSV contains lambda, observed coordinates y*, and noiseless true-curve coordinates true_y*.",
        "noise_model": "Gaussian noise in the normal space of the true curve.",
        "scenarios": {
            "spiral_i": {"lambda_range": [-1, 1], "dimension": 3, "noise_sd": 0.1},
            "spiral_ii": {"lambda_range": [0, 2], "dimension": 3, "noise_sd": 0.1},
            "heart": {"lambda_range": [0, "2*pi"], "dimension": 3, "noise_sd": 0.1},
            "butterfly": {"lambda_range": [0, 1], "dimension": 2, "noise_sd": 0.05},
            "pedal": {"lambda_range": [0, 1], "dimension": 2, "noise_sd": 0.05},
            "elvis": {
                "lambda_range": [0, 1],
                "dimension": 2,
                "noise_sd": 1.0,
                "curve": "Cubic B-spline through hard-coded control points in examples/generate_synthetic_datasets.py.",
            },
        },
    }


def write_datasets(datasets: dict[str, dict[str, np.ndarray]], output_dir: Path, seed: int, n: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, values in datasets.items():
        lam = values["lambda"][:, None]
        observed = values["observed"]
        true = values["true"]
        dim = observed.shape[1]
        columns = ["lambda"] + [f"y{i + 1}" for i in range(dim)] + [f"true_y{i + 1}" for i in range(dim)]
        table = np.column_stack([lam, observed, true])
        np.savetxt(output_dir / f"{name}.csv", table, delimiter=",", header=",".join(columns), comments="")

    with (output_dir / "metadata.json").open("w", encoding="utf-8") as fh:
        json.dump(_metadata(seed, n), fh, indent=2)
        fh.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic"), help="Output directory for CSV files.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed.")
    parser.add_argument("--n", type=int, default=DEFAULT_N, help="Number of observations per scenario.")
    args = parser.parse_args()

    datasets = generate_synthetic_datasets(seed=args.seed, n=args.n)
    write_datasets(datasets, args.output, seed=args.seed, n=args.n)

    print(f"Wrote {len(datasets)} synthetic datasets to {args.output}")
    for name, values in datasets.items():
        print(f"  - {name}: observed shape {values['observed'].shape}")


if __name__ == "__main__":
    main()
