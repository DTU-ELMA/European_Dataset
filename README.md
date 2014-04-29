Author: Tue Jensen

This repository contains a cleanup of my code for building the large-scale European dataset from ECMWF weather data, the Bialek network and GEO generator data.
The following is meant to be a guideline for reproducing the dataset using the sources as indicated.


## Network building/data extraction

TODO: Add me

## Building Projection matrices for wind, solar and load

TODO: Add me

## Renewable data conversion to nodal production signals

TODO: Add me

## ENTSOE load data to nodal signals

TODO: Add me

## Generator extraction from Global Energy Observatory data

Download all relevant datafiles from www.globalenergyobservatory.com in kml format and place them in ./Data/Generator_Datafiles/.
Run ./Scripts/Generator_Handling/1-Extract_GEO_Files to generate a database.
Run ./Scripts/Generator_Handling/2-assign_generators_to_nodes to associate generators with network nodes, and build the final database. (Requires the network to have been built.)
