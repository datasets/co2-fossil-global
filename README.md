<a className="gh-badge" href="https://datahub.io/core/co2-fossil-global"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Global CO2 emissions from fossil fuels annually since 1750 through 2024.

## Data

Data comes from the [Global Carbon Project (GCP)](https://globalcarbonproject.org/) annual Global Carbon Budget release.

- **Source:** Andrew, R. M., & Peters, G. P. (2025). *The Global Carbon Project's fossil CO2 emissions dataset* (2025v15). Zenodo. https://doi.org/10.5281/zenodo.17417124
- **Coverage:** 1750–2024 (updated annually each December after the GCP release)
- **Units:** `global.csv` values are in million metric tonnes of Carbon (MtC). `data/fuel-breakdown.csv` values are in million metric tonnes of CO2 (MtCO2).

## Updating

Run the update script to fetch the latest GCP data:

```bash
python3 scripts/update.py
```

This fetches the GCP flat CSV from Zenodo, filters for global aggregates, converts units, and overwrites `global.csv` and `data/fuel-breakdown.csv`. A GitHub Actions workflow runs this automatically each December.

To update to a specific GCP release, edit the `GCP_URL` constant in `scripts/update.py`.

## Citation

Please cite the upstream source as:

> Andrew, R. M., & Peters, G. P. (2025). The Global Carbon Project's fossil CO2 emissions dataset (2025v15). Zenodo. https://doi.org/10.5281/zenodo.17417124

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).

Upstream data is licensed under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
