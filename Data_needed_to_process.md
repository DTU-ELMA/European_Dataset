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

```
ctr_P165_LSFC
edition      centre       typeOfLevel  level        dataDate     stepRange    dataType     shortName    packingType  gridType     
1            ecmf         surface      0            20120101     0            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     1            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     2            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     3            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     4            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     5            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     6            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     7            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     8            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     9            fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     10           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     11           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     12           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     13           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     14           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     15           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     16           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     17           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     18           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     19           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     20           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     21           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     22           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     23           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     24           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     25           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     26           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     27           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     28           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     29           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     30           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     31           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     32           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     33           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     34           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     35           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     36           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     37           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     38           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     39           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     40           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     41           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     42           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     43           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     44           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     45           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     46           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     47           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     48           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     49           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     50           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     51           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     52           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     53           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     54           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     55           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     56           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     57           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     58           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     59           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     60           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     61           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     62           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     63           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     64           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     65           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     66           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     67           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     68           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     69           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     70           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     71           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     72           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     73           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     74           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     75           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     76           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     77           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     78           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     79           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     80           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     81           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     82           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     83           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     84           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     85           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     86           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     87           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     88           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     89           fc           10u          grid_simple  regular_ll  
1            ecmf         surface      0            20120101     90           fc           10u          grid_simple  regular_ll  
91 of 91 grib messages in ctr_P165_LSFC
```

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

# ENTSO-E Load

Entso-e load files are downloaded as country packages from

https://www.entsoe.eu/data/data-portal/country-packages/Pages/default.aspx

These should be placed as
`./Data/ENTSOE-load/excel_files/XXX_YYYY.xls`
where `XXX` is a three-letter country code (ISO Alpha-3), e.g. `AUT_2012.xls` contains data from Austria for 2012.
