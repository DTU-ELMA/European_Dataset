# RE-Europe code overview

This document attempts to give an overview of the scripts needed to be run in order to re-generate the dataset.
For a list of required data, see Data\_Overview.md.

This document is divided into 5 parts, each dealing with a separate part of the dataset:

1. Transmission Network
2. Generator Database
3. Renewable production data
4. Demand data
5. Saving CSV files

In order to proceed with points 2-4, point 1 must have been executed.
Point 4 further requires that the latitude/longitude grid from point 3 has been extracted.
Point 5 depends on the relevant parts of the preceding points.

# 1. Transmission network

## Network building/data extraction

Extract data from the Bialek network dataset into .csv files as described in Scripts/Network\_latlon/README.md .
Run Scripts/Network\_latlon/1-Parse\_network\_data.py to parse the network data.
Run Scripts/Network\_latlon/2-Fit\_positions.py to add positional data to the network.

A list of bus positions is located in Scripts/Network_latlon/coordinates-mercator.txt -- The user should check that the 'x' and 'y' columns of this datafile matches their extracted data.

# 2. Generator database

## Generator extraction from Global Energy Observatory data

(Requires the network to have been built.)
Download all relevant datafiles from www.globalenergyobservatory.com in kml format and place them in ./Data/Generator_Datafiles/excel_files.
Run ./Scripts/Generator_Handling/1-Extract_GEO_Files to generate a database.
Run ./Scripts/Generator_Handling/2-assign_generators_to_nodes to associate generators with network nodes, and build the final database.

# 3. Renewable production signals

## Renewable forecast data conversion

TODO: Add me

## Interpolating and converting real-time renewable production signal

TODO: Add me

## Building Projection matrices for wind, solar and load

TODO: Add me

## Aggregating wind and solar production to the nodal domain

TODO: Add me

## Notes for converting COSMO data

TODO: Add me

# 4. Demand signal

## ENTSOE load data to nodal signals

(Requires the network to have been built.)

(Requires the latitude and longitude grids from the ECMWF data to be present as ./Data/Metadata/{lats, lons}\_ECMWF.npy)

(Requires the projection matrixes from the ECMWF data to have been built: `./Data/Metadata/loadtransfercsr_ECMWF.npz`)

Running `extract_excel_files.py` parses the raw ENTSO-E country packages into .npy files.

Running `load_to_maps.py` then projects these .npy files according to the population in each grid cell.

Finally, running project_nodal_load.py then aggregates these maps of electrical demand onto the nodal domain.

# 5. Saving CSV files

The scripts located in `./Scripts/Save_{forecast,network,signal}_csv/` translates .npy files into the csv format, with the output located in `./Output_Data/{Nodal_FC,Metadata,Nodal_TS}/`, respectively.
