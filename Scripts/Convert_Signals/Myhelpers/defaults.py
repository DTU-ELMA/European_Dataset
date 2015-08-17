startyear = 2012
startmonth = 1
endyear = 2014
endmonth = 12

# Geographical files

onshoremapfilename = '../../Data/Metadata/onshore_ECMWF.npy'
latitudefile = '../../Data/Metadata/lats_ECMWF.npy'
longitudefile = '../../Data/Metadata/lons_ECMWF.npy'
nodeorder = '../../Data/Metadata/nodeorder.npy'

# Wind files

# onshoreturbinecfg = 'TurbineData/Vestas_V90_3MW.cfg'
# offshoreturbinecfg = 'TurbineData/Vestas_V164_7MW_offshore.cfg'
onshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_smoothed.cfg'
offshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_anholt_smoothed.cfg'

windsignaldatadir = "../../Data/Signal_Processed/"
windsignaloutdir = "../../Data/Nodal_Signal/"

windprojectionmatrix = '../../Data/Metadata/wndtransfercsr_ECMWF.npz'

# Solar files
solarsignaldatadir = "../../Data/Signal_Unprocessed/"
solarsignaloutdir = "../../Data/Nodal_Signal/"

solarpanelcfg = 'SolarPanelData/Scheuten215IG.cfg'
solarprojectionmatrix = '../../Data/Metadata/solartransfercsr_ECMWF.npz'
