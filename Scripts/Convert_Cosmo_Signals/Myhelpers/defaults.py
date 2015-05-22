startyear = 2012
startmonth = 01
endyear = 2012
endmonth = 01

# Geographical files

onshoremapfilename = '../../Data/Metadata/onshore_COSMO.npy'

latitudefile = '../../Data/Metadata/lats_COSMO.npy'
longitudefile = '../../Data/Metadata/lons_COSMO.npy'

# Wind files

# onshoreturbinecfg = 'TurbineData/Vestas_V90_3MW.cfg'
# offshoreturbinecfg = 'TurbineData/Vestas_V164_7MW_offshore.cfg'
onshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_smoothed.cfg'
offshoreturbinecfg = 'TurbineData/Siemens_SWT_107_3600kW_anholt_smoothed.cfg'

winddatadir = "../../Data/COSMO_data/"
windoutdir = "../../Data/Nodal_Power/"

windprojectionmatrix = '../../Data/Metadata/wndtransfercsr_COSMO.npz'
nodeorder = '../../Data/Metadata/nodeorder.npy'


# Solar files
solarforecastdatadir = "../../Data/COSMO_data/"
solarforecastoutdir = "../../Data/Nodal_Power/"

solarpanelcfg = 'SolarPanelData/Scheuten215IG.cfg'
solarprojectionmatrix = '../../Data/Metadata/solartransfercsr_COSMO.npz'
