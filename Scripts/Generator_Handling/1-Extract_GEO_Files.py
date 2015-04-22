from bs4 import BeautifulSoup
import os
import pickle
import random

datadir = '../../Data/'
inputdir = datadir + 'Generator_Datafiles/'
metadatadir = datadir + 'Metadata/'
inputfiles = os.listdir(inputdir)
inputfiles = [x for x in inputfiles if 'kml' in x]


def coordinate_string_to_latlon_pair(x):
    return map(float, x.split(','))


def none_to_empty(x):
    if x is None:
        return '0'
    else:
        return x


def parse_description(nodedescription,plant_type='Coal'):
    mignon = BeautifulSoup(str(nodedescription[0]))
    # Nothing here we need
    mignon = BeautifulSoup(str(nodedescription[1]))
    cutlets = mignon.find_all('tr')
    nodestatus = unicode(cutlets[0].select('td')[1].string)
    # Str conversion to catch nonetype return
    nodecapacity = float(none_to_empty(cutlets[3].select('td')[1].string))
    if plant_type == 'Coal' or plant_type == 'Gas':
        nodeprimaryfuel = unicode(cutlets[8].select('td')[1].string.lstrip('Primary: '))
        nodesecondaryfuel = unicode(cutlets[8].select('td')[2].string.lstrip('Secondary: '))
    elif plant_type == 'Hydro':
        nodeprimaryfuel = 'Hydro'
        nodesecondaryfuel = None
    elif plant_type == 'Nuclear':
        nodeprimaryfuel = 'Nuclear'
        nodesecondaryfuel = None
    else:
        nodeprimaryfuel = 'Unknown'
        nodesecondaryfuel = None
    mignon = BeautifulSoup(str(nodedescription[2]))
    cutlets = mignon.select('tr')
    generators = {}
    for line in cutlets[2:]:
        chops = line.find_all('td')
        if not chops[1].string == None:
            if plant_type == 'Nuclear':
                generators[int(chops[0].string)] = {'capacity': float(chops[2].string), 'Turbine Model': unicode(chops[9].string)}
            else:
                generators[int(chops[0].string)] = {'capacity': float(chops[1].string), 'Turbine Model': unicode(chops[7].string)}

    if nodecapacity == 0.0:
        nodecapacity = sum(generators[g]['capacity'] for g in generators)

    return {'capacity': nodecapacity, 'primaryfuel': nodeprimaryfuel, 'secondaryfuel': nodesecondaryfuel, 'generators': generators, 'status': nodestatus}

# # MAIN SCRIPT FOLLOWS

database = {}
i = 0
print ''
for inputfile in inputfiles:
    with open(inputdir + inputfile, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

    plant_type = inputfile.split('_')[2]
    country = inputfile.split('_')[3]
    for node in soup.select('placemark'):
        i += 1
        print '\r', str(i)
        nodeid = node.attrs['id'].lstrip('placemark')
        nodename = unicode(node.select('name')[0].string)
        nodelocation = coordinate_string_to_latlon_pair(node.select('coordinates')[0].string)
        nodedescription = map(str, node.select('description')[0].contents)
        if not nodedescription == []:
            nodedescdict = parse_description(nodedescription, plant_type)
        else:
            nodedescdict = {'capacity': 0, 'primaryfuel': plant_type, 'secondaryfuel': None, 'generators': {}, 'status': 'No Data in GEO'}

        database[nodeid] = {'name': nodename, 'location': nodelocation, 'country': country}  # , 'description': nodedescription}
        database[nodeid].update(nodedescdict)

# # # Cleanup of database

# # # So many fuel types - let's simplify
translatefuel = {
    None: None,
    u'': None,
    u'Please Select': None,
    u'Anthracite coal': 'Coal',
    u'Biomass': u'Biomass',
    u'Bituminous Coal': 'Coal',
    u'Blast Furnace Gas (Dowson Gas)': 'Natural Gas',
    u'Blast furnace gas and coke oven gas': 'Natural Gas',
    u'Brown Coal': 'Lignite',
    u'Brown Coal  and Lignite': 'Lignite',
    u'Brown Coal (Lignite)': 'Lignite',
    u'Coal': 'Coal',
    u'Coal Anthracite': 'Coal',
    u'Coal Anthracite and bituminous': 'Coal',
    u'Coal Bituminous': 'Coal',
    u'Coal Brown Lignite': 'Lignite',
    u'Coal Hard': 'Coal',
    u'Coal Lignite': 'Lignite',
    u'Coal Lignite and bituminous': 'Lignite',
    u'Coal Sub-bituminous': 'Coal',
    u'Coal Syngas': 'Natural Gas',
    u'Coal bituminous': 'Coal',
    u'Coal bituminous and lignite': 'Coal',
    u'Coal lignite': 'Lignite',
    u'Coal lignite and Brown Coal': 'Lignite',
    u'Coal lignite and sub-bituminous': 'Lignite',
    u'Coal lignite black': 'Lignite',
    u'Coal, Heavy Fuel Oil': 'Coal',
    u'Coal, slag, petroleum coke': 'Coal',
    u'Diesel Oil': 'Fuel Oil',
    u'Distillate Oil': 'Fuel Oil',
    u'Fuel Oil': 'Fuel Oil',
    u'Fuel Oil Heavy': 'Fuel Oil',
    u'Fuel Oil Light': 'Fuel Oil',
    u'Furnace Gas': 'Coal',
    u'Gas': 'Natural Gas',
    u'Gas from Steel Mills': 'Natural Gas',
    u'Gas Oil': 'Natural Gas',
    u'Hard Coal': 'Coal',
    u'Hard Coal, Heavy Fuel Oil': 'Coal',
    u'Heavy Fuel Oil': 'Fuel Oil',
    u'Hydro': 'Hydro',
    u'Lignite': 'Lignite',
    u'Light Fuel Oil/Diesel': 'Fuel Oil',
    u'Mixed Fuel (Coal NG, Blast Furnance Gas, Wood Pellets)': 'Coal',
    u'Natual Gas': 'Natural Gas',
    u'Natural Gas': 'Natural Gas',
    u'Natural Gas (Recovery gas from steel mill)': 'Natural Gas',
    u'Nuclear': 'Nuclear',
    u'Oil distillate': 'Fuel Oil',
    u'Sub-bituminous': 'Coal',
    u'Syn gas from Coal Gasification': 'Coal',
    u'Unknown': 'Unknown',
    u'Waste': 'Waste',
    u'Waste Furnace Gas': 'Waste',
    u'Wood Waste': u'Biomass',
    u'blast furnace gas (BFG)': 'Natural Gas',
    u'coal': 'Coal',
    u'high-calorific coke-oven gas and blast furnace gas': 'Coal',
    u'oal Bituminous': 'Coal',
    u'syngas from refinery residual oil': 'Fuel Oil'}

for g in database.iterkeys():
    database[g]['primaryfuel'] = translatefuel[database[g]['primaryfuel']]
    database[g]['secondaryfuel'] = translatefuel[database[g]['secondaryfuel']]


## Ramp rates set by fuel type (relative to max capacity)
ramprates = {None: 1.0, u'Biomass': 1.0, 'Coal': 0.8, 'Fuel Oil': 1.0, 'Hydro': 1.0, 'Lignite': 0.7,
       'Natural Gas': 1.0, 'Nuclear': 0.5, 'Unknown': 1.0, 'Waste': 1.0}

for g in database.iterkeys(): 
    database[g]['ramp'] = ramprates[database[g]['primaryfuel']]

## Linear cost set by fuel type [$ / MWh] - Uniformly chosen from 90-110% of below.
lincosts = {None: 90.0, u'Biomass': 60.0, 'Coal': 40.0, 'Fuel Oil': 80.0, 'Hydro': 15.0, 'Lignite': 35.0,
       'Natural Gas': 50.0, 'Nuclear': 4.0, 'Unknown': 90.0, 'Waste': 60.0}

for g in database.iterkeys(): 
    database[g]['lincost'] = lincosts[database[g]['primaryfuel']]*(random.random()*0.2+0.9)


## Minimal up- and downtimes by fuel type [in hours]
uptimes = {None: 1, u'Biomass': 4, 'Coal': 4, 'Fuel Oil': 2, 'Hydro': 1, 'Lignite': 4,
       'Natural Gas': 1, 'Nuclear': 24, 'Unknown': 1, 'Waste': 4}
downtimes = {None: 1, u'Biomass': 4, 'Coal': 4, 'Fuel Oil': 2, 'Hydro': 1, 'Lignite': 4,
       'Natural Gas': 1, 'Nuclear': 24, 'Unknown': 1, 'Waste': 4}

for g in database.iterkeys(): 
    f = database[g]['primaryfuel']
    database[g]['minuptime'] = uptimes[f]
    database[g]['mindowntime'] = downtimes[f]


## Minimal production set by fuel type
mincapacity = {
    None: 0.30, u'Biomass': 0.40, 'Coal': 0.30,  # http: //ebooks.asmedigitalcollection.asme.org/content.aspx?bookid=240&sectionid=38774800
    'Fuel Oil': 0.40, 'Hydro': 0.30, 'Lignite': 0.40,
    'Natural Gas': 0.40,  # http: //www.alstom.com/Global/Power/Resources/Documents/Brochures/gas-power-plants.pdf
    'Nuclear': 0.40,  # http://www.iaea.org/NuclearPower/Meetings/2013/2013-09-04-09-06-TM-NPE.html
    'Unknown': 0.30, 'Waste': 0.40}

for g in database.iterkeys():
    database[g]['minonlinecapacity'] = mincapacity[database[g]['primaryfuel']]*database[g]['capacity']


# # Warm start cycling costs [$/MW cap]
# # Based on data from NREL - "Power plant cycling costs" (April 2012) and
# # http://www.ipautah.com/data/upfiles/newsletters/CyclingArticles.pdf (coal)
# # http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00574921 (hydro)
cyclecost = {
    None: 100, u'Biomass': 4, 'Coal': 65, 'Fuel Oil': 58, #Assumed equal to gas open cycle steam
    'Hydro': 4.2, # Based on swedish data, in 2008 dollars
    'Lignite': 65, #Assumed equal to coal
    'Natural Gas': 55, #Assumes CCGT
    'Nuclear': 300, # No source - set at large number to represent usual baseload operation
    'Unknown': 100, 'Waste': 65 #assumed equal to coal
}

for g in database.iterkeys():
    f = database[g]['primaryfuel']
    database[g]['cyclecost'] = cyclecost[f]*database[g]['capacity']


pickle.dump(database, open(metadatadir + 'generator_database_no_affiliation.pickle','w'))
