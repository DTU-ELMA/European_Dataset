# RE-Europe dataset code

Authors: Tue Jensen & Hugo de Sevin

This repository is licensed under the Apache license. See LICENSE.markdown for further information.

This repository contains code for building the large-scale European dataset from ECMWF weather data, COSMO data,  the Bialek network and GEO generator data.
All scripts have been tested working as of 20/08 on machines running Ubuntu Linux 15.04, using python version 2.7.9, Pandas version 0.15.0, Numpy 1.8.2 and PyGrib 2.0.0.

An overview of the scripts provided is  given in `code_overview.md`.

An overview of the data required to re-generate the dataset is given in `data_required.md`

# Contributors

**Tue Vissing Jensen**: Repository manager, organizer. Contributor if not listed below.

**Hugo de Sevin**: COSMO-REA6 conversion code. UK grid specification.

**Pierre Pinson**: ECMWF Extraction code.

**Anders Søndergaard**: Main wind/solar conversion loop (Together with Gorm Bruun Andresen), wind/solar conversion data files.

**Gorm Andresen**: Smoothed wind turbine curves.
