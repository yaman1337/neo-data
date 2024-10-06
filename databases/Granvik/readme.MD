# Granvik NEO Model Datasets

The datasets `enriched_granvik_model.parquet` and `enriched_granvik_model_w_appmag.parquet` are derived from the Granvik NEO model described in:

Granvik, Morbidelli, Jedicke, Bolin, Bottke, Beshore, Vokrouhlicky, Nesvorny, and Michel (2018). Debiased orbit and absolute-magnitude distributions for near-Earth objects. Accepted for publication in Icarus.

The original data file `Granvik+_2018_Icarus.dat` contains 802,000 synthetic NEOs with 17<H<25 parameterized by their orbits and absolute magnitudes. The 7 columns in the file are:

1. Semimajor axis [au]
2. Eccentricity
3. Inclination [deg]
4. Longitude of ascending node [deg]
5. Argument of perihelion [deg]
6. Mean anomaly [deg]
7. Absolute magnitude

Mikael Granvik
27-04-2018

## Datasets

The datasets are available in Parquet format:

- `enriched_granvik_model.parquet`
- `enriched_granvik_model_w_appmag.parquet`

Due to the large size of these datasets, they are not included in this repository. You can download them from the following links:

[Cleaned and Enriched Dataset](https://furman.box.com/s/6el8ovwea0wb8op947307wy7pu4x2m14)


## Usage

To load the datasets in Python, you can use the following code:

```python
import pandas as pd

# Load the datasets
enriched_granvik_model = pd.read_parquet('path/to/enriched_granvik_model.parquet')
enriched_granvik_model_w_appmag = pd.read_parquet('path/to/enriched_granvik_model_w_appmag.parquet')