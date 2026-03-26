# Starter `src/` Project Structure

This is a clean starter structure for turning your current notebook-style scripts into an end-to-end Python pipeline.

## Folder layout

```text
src_project/
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ loaders.py
│  ├─ preprocess.py
│  ├─ models.py
│  ├─ plot.py
│  ├─ validate.py
│  ├─ utils.py
│  └─ pipeline.py
├─ scripts/
│  └─ run_pipeline.py
├─ data/
│  ├─ raw/
│  ├─ interim/
│  ├─ processed/
│  └─ outputs/
└─ logs/
```

## Recommended workflow

1. Put your raw CSV files into `data/raw/`
2. Update paths and column names in `src/config.py`
3. Edit the `REGISTRY` dictionary in `scripts/run_pipeline.py`
4. Run the pipeline:

```bash
python scripts/run_pipeline.py
```

## What each module does

- `config.py` -> central paths, file names, parcel names, and defaults
- `loaders.py` -> reading CSV files and preparing parcel-level inputs
- `preprocess.py` -> date cleaning, duplicate handling, alignment, interpolation, merging
- `models.py` -> weighted mean, dielectric, roughness, Dubois, WCM, SV-SIM, simple calibration
- `plot.py` -> final plots and evaluation figures
- `validate.py` -> checks for files, required columns, and data quality
- `pipeline.py` -> runs the stages in order

## Important note

This is intentionally a **clean starter architecture**, not a raw copy of every line from your old scripts. Your original files contain overlap, hard-coded paths, and debug snippets. This version is made so you can understand the structure and extend it safely.
