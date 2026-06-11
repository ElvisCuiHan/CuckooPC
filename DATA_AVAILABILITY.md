# Data Availability

The single-cell RNA-seq dataset used for the scGTM example is publicly
available from the Gene Expression Omnibus under accession `GSE111976`:

https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE111976

The synthetic principal-curve datasets used in the manuscript are fully
reproducible from the code in this repository.  They can be regenerated with:

```bash
python examples/generate_synthetic_datasets.py --output data/synthetic --seed 42 --n 120
```

The generated CSV files are also included under `data/synthetic/` for
convenience.  Each file contains both noisy observations and the corresponding
noiseless true-curve coordinates.

For reproducibility, the default generation settings are:

- random seed: `42`
- observations per scenario: `120`
- scenarios: Spiral I, Spiral II, Heart, Butterfly, Pedal, and Elvis
- noise model: Gaussian noise in the normal space of the true curve
