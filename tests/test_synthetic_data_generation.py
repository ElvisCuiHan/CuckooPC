"""Smoke tests for manuscript synthetic data generation."""

from pathlib import Path
import importlib.util


SCRIPT = Path(__file__).resolve().parents[1] / "examples" / "generate_synthetic_datasets.py"
spec = importlib.util.spec_from_file_location("generate_synthetic_datasets", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_generate_synthetic_datasets_shapes():
    datasets = module.generate_synthetic_datasets(seed=42, n=120)

    assert set(datasets) == {"spiral_i", "spiral_ii", "heart", "butterfly", "pedal", "elvis"}

    assert datasets["spiral_i"]["observed"].shape == (120, 3)
    assert datasets["spiral_ii"]["observed"].shape == (120, 3)
    assert datasets["heart"]["observed"].shape == (120, 3)
    assert datasets["butterfly"]["observed"].shape == (120, 2)
    assert datasets["pedal"]["observed"].shape == (120, 2)
    assert datasets["elvis"]["observed"].shape == (120, 2)

    for values in datasets.values():
        assert values["lambda"].shape == (120,)
        assert values["observed"].shape == values["true"].shape


if __name__ == "__main__":
    test_generate_synthetic_datasets_shapes()
    print("Synthetic data generation smoke test passed.")
