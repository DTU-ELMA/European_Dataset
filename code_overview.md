# RE-Europe code overview

This document attempts to give an overview of the scripts needed to be run in order to re-generate the dataset.
For a list of required data, see Data\_Overview.md.

This document is divided into 4 parts, each dealing with a separate part of the dataset:

1. Transmission Network
2. Generator Database
3. Renewable production data
4. Demand data

In order to proceed with points 2-4, point 1 must have been executed.
Point 4 further requires that the latitude/longitude grid from point 3 has been extracted.

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

# 4. Demand signal

## ENTSOE load data to nodal signals

(Requires the network to have been built.)

(Requires the latitude and longitude grids from the ECMWF data to be present as ./Data/Metadata/{lats, lons}\_ECMWF.npy)


TODO: Add me
