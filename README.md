# CAOS Sentinel-2 Pipeline in Python

Pipeline for the processing of Sentinel-2 data and ground truth in the CAOS-Lux project

Workflow for creating a dataset out of soil moisture data and Sentinel-2A
images for the CAOS-lux soil moisture dataset in the Attert region of Luxemburg.
The data was aquired from 2014 to 2018.

**License:** [3-Clause BSD license](LICENSE)

**Authors:**

* [Philipp Wagner](https://github.com/philipp01wagner)
* [Felix M. Riese](https://github.com/felixriese)
* [Sina Keller](https://github.com/sinakeller)

**Citation:** See [Citation](#citation) and [bibliography.bib](bibliography.bib).

## Requirements

The dependencies and requirements can be found in `/dependencies`.

Install dependencies with:

```bash
./install_dependencies_and_scihub_account.sh
```

This script asks also for the Scihub account data which is stored in
`account.ini`.

## Howto

To create a dataset the script `py/create_dataset.py` has to be executed with
the desired date as command line argument in the format YYYYMMDD, e.g.:

```bash
python create_dataset.py 20161204
```

Alternative is to give a file as argument with a date in every line.
A new directory named after the date will be created in the directory
`/processed_data`. The script will download the desired S2A file, extract the
zip, and construct gtiffs for the measured area and the prediction area.
The IPython Notebooks provide an analysis of the constructed data. They include
visualization of soil moisture and Sentinel-bands, further pre-processing and
filtering and regression/classification where the soil moisture is predicted
based on the Sentinel-data. For the machine learning part, the common
regressors/classificators are used:

-  Random Forest,
-  Extra Trees,
-  Support Vector Machine,
-  Multilayer Perceptron.

## Citation

Philipp Wagner, Felix M. Riese and Sina Keller, "CAOS Sentinel-2 Pipeline in
Python", Code, Zenodo, 2020.

```tex
@misc{wagner2020caos,
  author       = {Wagner, Philipp and Riese, Felix~M. and Keller, Sina},
  title        = {CAOS Sentinel-2 Pipeline in Python},
  year         = 2020,
  publisher    = {Zenodo}
}
```
