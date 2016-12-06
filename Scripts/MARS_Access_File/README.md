# MARS Access file

**get_re-europe_files_ncdf.job:** Downloads data files for use in RE-Europe conversion.

Downloading the necessary data in this way requires shell access to the ECMWF MARS system. Sorry.

## Configuration
To configure the process, edit the following lines:
* **#@ initialdir = \\changeme\\notafolder\\:** directory on the server to which the data will be downloaded. E.g. \\scratch\\yourusername\\asubfolder\\
* **DATE_START** and **DATE_END:** Dates for which data will be extracted. With the typical \\scratch\\ allowance, it is possible to store one year of data at a time. One year amounts to ~250GB of data.

Move the .job file to a folder on the ECMWF server and run it.
The data will be downloaded to the folder specified in *initialdir*.

## Moving data from the ECMWF servers
Download the data files to

**RE-Europe basedir\\Data\\ECMWF-data\\**

The final directory structure will be of the type

**RE-Europe basedir\\Data\\ECMWF-data\\YYYMMDDHH\\ctr_PXXX_LSFC**

where XXX is the number code for the field.