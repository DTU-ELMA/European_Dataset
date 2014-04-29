Three datafiles are needed here to define the network - they may be extracted from the data at www.powerworld.com/bialek using the Powerworld Viewer available at the same site.
The latitude and longitude fields are not filled in by default, but must be populated by the oneline coordinates through a _Mercator_ transformation. These are used to fit the bus positions using the position pairs in coordinates-mercator.txt.
The three files are
# buses.csv - Bus info
BusNum,Longitude,Latitude,BusName,BusNomVolt
# bus_countries.csv - Bus country assignment
BusNum,AreaName
# lines.csv - Line information
BusNum,BusNum:1,LineX,LineAMVA
