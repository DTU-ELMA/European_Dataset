Authors: Tue Jensen & Hugo de Sevin
This repository is licensed CC-BY. See LICENSE.markdown for further information.

This repository contains code for building the large-scale European dataset from ECMWF weather data, COSMO data,  the Bialek network and GEO generator data.
All scripts have been tested working as of 20/08 on machines running Ubuntu Linux 15.04, using python version 2.7.9, Pandas version 0.15.0, Numpy 1.8.2 and PyGrib 2.0.0.
The following is meant to be a guideline for reproducing the dataset using the sources as indicated.

## Network building/data extraction

Extract data from the Bialek network dataset into .csv files as described in Scripts/Network_latlon/README.md .
Run Scripts/Network_latlon/1-Parse_network_data.py to build the first network.
Run Scripts/Network_latlon/2-Fit_positions.py to add positional data to the network.

## Renewable forecast data conversion

TODO: Add me

## Interpolating and converting real-time renewable production signal

TODO: Add me

## Building Projection matrices for wind, solar and load

TODO: Add me

## ENTSOE load data to nodal signals

TODO: Add me

## Generator extraction from Global Energy Observatory data

(Requires the network to have been built.)
Download all relevant datafiles from www.globalenergyobservatory.com in kml format and place them in ./Data/Generator_Datafiles/excel_files.
Run ./Scripts/Generator_Handling/1-Extract_GEO_Files to generate a database.
Run ./Scripts/Generator_Handling/2-assign_generators_to_nodes to associate generators with network nodes, and build the final database.

