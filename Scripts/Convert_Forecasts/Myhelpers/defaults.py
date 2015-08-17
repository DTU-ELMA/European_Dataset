startyear = 2012
startmonth = 1
endyear = 2014
endmonth = 12

# Geographical files

onshoremapfilename = '../../Data/Metadata/onshore.npy'

latitudefile = '../../Data/Metadata/lats_ECMWF.npy'
longitudefile = '../../Data/Metadata/lons_ECMWF.npy'

# Wind files
onshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_smoothed.cfg'
offshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_anholt_smoothed.cfg'

windforecastdatadir = "../../Data/ECMWF-data/"
windforecastoutdir = "../../Data/Nodal_Forecasts/"

windprojectionmatrix = '../../Data/Metadata/wndtransfercsr_ECMWF.npz'
nodeorder = '../../Data/Metadata/nodeorder.npy'


# Solar files
solarforecastdatadir = "../../Data/ECMWF-data/"
solarforecastoutdir = "../../Data/Nodal_Forecasts/"

solarpanelcfg = 'SolarPanelData/Scheuten215IG.cfg'
solarprojectionmatrix = '../../Data/Metadata/solartransfercsr_ECMWF.npz'
