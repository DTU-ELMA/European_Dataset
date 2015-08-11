startyear = 2014
startmonth = 06
endyear = 2014
endmonth = 06

# Geographical files

onshoremapfilename = '../../Data/Metadata/onshore.npy'

latitudefile = '../../Data/Metadata/lats.npy'
longitudefile = '../../Data/Metadata/lons.npy'

# Wind files

# onshoreturbinecfg = 'TurbineData/Vestas_V90_3MW.cfg'
# offshoreturbinecfg = 'TurbineData/Vestas_V164_7MW_offshore.cfg'
onshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_smoothed.cfg'
offshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_anholt_smoothed.cfg'

windforecastdatadir = "../../Data/ECMWF-data/"
windforecastoutdir = "../../Data/Nodal_Forecasts/"

windprojectionmatrix = '../../Data/Metadata/wndtransfercsr.npz'
nodeorder = '../../Data/Metadata/nodeorder.npy'


# Solar files
solarforecastdatadir = "../../Data/ECMWF-data/"
solarforecastoutdir = "../../Data/Nodal_Forecasts/"

solarpanelcfg = 'SolarPanelData/Scheuten215IG.cfg'
solarprojectionmatrix = '../../Data/Metadata/solartransfercsr.npz'
