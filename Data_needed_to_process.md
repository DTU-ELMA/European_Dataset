# Overview

This file describes the necessary data to re-generate the dataset, along with inventories of meteorological files necessary.

Note that filenames like './' refer to the root folder containing LICENSE.markdown.

# ECMWF data

Forecasts given at YYYY-MM-DD HH:MM are placed in
'./Data/ECMWF-data/YYYYMMDDHH/',
where the necessary files are called ctr_PXXX_LSFC for the following fields:

| Code | Note |
|------|------|
| P165 | Wind, U, 10m |
| P166 | Wind, V, 10m |
| P167 | Temperature, 2m |
| P169 | Incident Beam Radiation |
| P243 | Ground Albedo |
| P246 | Wind, U, 100m | 
| P247 | Wind, V, 100m |

A MARS access file is available as
'./Script/Mars_Access_File/'
which automates this process.
See the included readme for details.

An inventory of P165 looks as follows:

--- TODO: Add Inventory ---

# COSMO-REA6 data

This data was provided by Christoph Bollmeyer over a private connection.
For the current project maintainer, see the project homepage: https://www.herz-tb4.uni-bonn.de/

The COSMO-REA6 data is located as grib files in the format
'./Data/COSMO-data/lafYYYYMMDDHHMMSS'

An example file inventory is given below:

```
laf20120101000000
edition      centre       typeOfLevel  levels       dataDate     stepRange    shortName    packingType  gridType     
1            edzw         hybridLayer  35-36        20120101     0            u            grid_simple  rotated_ll  
1            edzw         hybridLayer  36-37        20120101     0            u            grid_simple  rotated_ll  
1            edzw         hybridLayer  37-38        20120101     0            u            grid_simple  rotated_ll  
1            edzw         hybridLayer  38-39        20120101     0            u            grid_simple  rotated_ll  
1            edzw         hybridLayer  39-40        20120101     0            u            grid_simple  rotated_ll  
1            edzw         hybridLayer  40-41        20120101     0            u            grid_simple  rotated_ll  
1            edzw         hybridLayer  35-36        20120101     0            v            grid_simple  rotated_ll  
1            edzw         hybridLayer  36-37        20120101     0            v            grid_simple  rotated_ll  
1            edzw         hybridLayer  37-38        20120101     0            v            grid_simple  rotated_ll  
1            edzw         hybridLayer  38-39        20120101     0            v            grid_simple  rotated_ll  
1            edzw         hybridLayer  39-40        20120101     0            v            grid_simple  rotated_ll  
1            edzw         hybridLayer  40-41        20120101     0            v            grid_simple  rotated_ll  
1            edzw         surface      not_found    20111231     6            sp           grid_simple  rotated_ll  
1            edzw         surface      not_found    20111231     6            al           grid_simple  rotated_ll  
1            edzw         heightAboveGround  not_found    20111231     6            2t           grid_simple  rotated_ll  
1            edzw         heightAboveGround  not_found    20111231     6            10u          grid_simple  rotated_ll  
1            edzw         heightAboveGround  not_found    20111231     6            10v          grid_simple  rotated_ll  
1            edzw         surface      not_found    20120101     0            ASWDIR_S     grid_simple  rotated_ll  
1            edzw         surface      not_found    20120101     0            ASWDIFD_S    grid_simple  rotated_ll  
1            edzw         surface      not_found    20120101     0            ASWDIFU_S    grid_simple  rotated_ll  
20 of 20 grib messages in laf20120101000000
```

# GlobalEnergyObservatory

Generator data files are downloaded as country/fuel type packages, located in 

'./Data/Generator_Data/GEO_PP_[Type]_[Country]_2000-2009.kml'

E.g. 'GEO_PP_Oil_Serbia_2000-2009.kml' contains information on Oil-fired plants in Serbia.
