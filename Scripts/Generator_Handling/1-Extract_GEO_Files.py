from bs4 import BeautifulSoup
import os
import pickle
import random

datadir = '../../Data/'
inputdir = datadir + 'Generator_Data/'
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


def parse_description(nodedescription, plant_type='Coal'):
    mignon = BeautifulSoup(str(nodedescription[0]))
    # Nothing here we need

    mignon = BeautifulSoup(str(nodedescription[1]))
    cutlets = mignon.find_all('tr')
    nodestatus = unicode(cutlets[0].select('td')[1].string)
    # Str conversion to catch nonetype return
    nodecapacity = float(none_to_empty(cutlets[3].select('td')[1].string))
    if plant_type == 'Coal' or plant_type == 'Gas' or plant_type == 'Oil':
        nodeprimaryfuel = unicode(cutlets[8].select('td')[1].string.lstrip('Primary: '))
        nodesecondaryfuel = unicode(cutlets[8].select('td')[2].string.lstrip('Secondary: '))
    elif plant_type == 'Geothermal':
        nodeprimaryfuel = 'Geothermal'
        nodesecondaryfuel = None
    elif plant_type == 'Hydro':
        nodeprimaryfuel = 'Hydro'
        nodesecondaryfuel = None
    elif plant_type == 'Nuclear':
        nodeprimaryfuel = 'Nuclear'
        nodesecondaryfuel = None
    elif plant_type == 'Waste':
        nodeprimaryfuel = 'Waste'
        nodesecondaryfuel = None
    elif plant_type == 'Biomass':
        nodeprimaryfuel = 'Biomass'
        nodesecondaryfuel = None
    else:
        nodeprimaryfuel = 'Unknown'
        nodesecondaryfuel = None

    mignon = BeautifulSoup(str(nodedescription[2]))
    cutlets = mignon.select('tr')
    generators = {}
    for line in cutlets[2:]:
        chops = line.find_all('td')
        if not chops[1].string is None:
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

        database[nodeid] = {'name': nodename, 'location': nodelocation, 'country': country}
        database[nodeid].update(nodedescdict)

# # # Cleanup of database

# # So many fuel types - let's simplify
translatefuel = {None: 'Unknown',
                 u'': 'Unknown',
                 u'Please Select': 'Unknown',
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
                 u'Coal Brown': 'Lignite',
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
                 u'Diesel': 'Fuel Oil',
                 u'Diesel Oil': 'Fuel Oil',
                 u'Distillate Oil': 'Fuel Oil',
                 u'Fuel Oil': 'Fuel Oil',
                 u'Fuel Oil Heavy': 'Fuel Oil',
                 u'Fuel Oil Light': 'Fuel Oil',
                 u'Furnace Gas': 'Coal',
                 u'Gas': 'Natural Gas',
                 u'Gas from Steel Mills': 'Natural Gas',
                 u'Gas Oil': 'Natural Gas',
                 u'Geothermal': 'Geothermal',
                 u'Hard Coal': 'Coal',
                 u'Hard Coal, Heavy Fuel Oil': 'Coal',
                 u'Heavy Fuel Oil': 'Fuel Oil',
                 u'Heavy Oil': 'Fuel Oil',
                 u'Hydro': 'Hydro',
                 u'Lignite': 'Lignite',
                 u'Light Fuel Oil/Diesel': 'Fuel Oil',
                 u'Mixed Fuel (Coal NG, Blast Furnance Gas, Wood Pellets)': 'Coal',
                 u'Natual Gas': 'Natural Gas',
                 u'Natural Gas': 'Natural Gas',
                 u'Natural Gas (Recovery gas from steel mill)': 'Natural Gas',
                 u'Nuclear': 'Nuclear',
                 u'Oil': 'Fuel Oil',
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


# # Ramp rates set by fuel type (relative to max capacity)
ramprates = {u'Biomass': 1.0, 'Coal': 0.8, 'Fuel Oil': 1.0, 'Geothermal': 1.0, 'Hydro': 1.0, 'Lignite': 0.7,
             'Natural Gas': 1.0, 'Nuclear': 0.5, 'Unknown': 1.0, 'Waste': 1.0}

for g in database.iterkeys():
    database[g]['ramp'] = ramprates[database[g]['primaryfuel']]

# # Linear cost set by fuel type [$ / MWh] - Uniformly chosen from 90-110% of below.
lincosts = {u'Biomass': 39.5, 'Coal': 38.6, 'Fuel Oil': 122.2, 'Geothermal': 0.0, 'Hydro': 6.4, 'Lignite': 23.8,
            'Natural Gas': 55.6, 'Nuclear': 11.8, 'Unknown': 130.0, 'Waste': 39.5}

# Jitter generators by +-10%
for g in database.iterkeys():
    random.seed(g)
    database[g]['lincost'] = lincosts[database[g]['primaryfuel']]*(random.random()*0.2+0.9)


# # Minimal up- and downtimes by fuel type
# No source - look for one!
uptimes = {u'Biomass': 8, 'Coal': 8, 'Fuel Oil': 2, 'Geothermal': 0, 'Hydro': 0, 'Lignite': 8,
           'Natural Gas': 2, 'Nuclear': 24, 'Unknown': 8, 'Waste': 8}
downtimes = {u'Biomass': 8, 'Coal': 8, 'Fuel Oil': 4, 'Geothermal': 0, 'Hydro': 0, 'Lignite': 8,
             'Natural Gas': 4, 'Nuclear': 24, 'Unknown': 8, 'Waste': 4}

for g in database.iterkeys():
    f = database[g]['primaryfuel']
    database[g]['minuptime'] = uptimes[f]
    database[g]['mindowntime'] = downtimes[f]


# # Set production of generators which are exported incorrectly from the database.
tosetlist = {
    '2175': 2060.,
    '2605': 270.,
    '2609': 1412.,
    '2947': 800.,
    '3913': 730.,
    '43676': 855.3,
    '4396': 372.,
    '45044': 345.,
    '4938': 868.,
    '5270': 466.,
    '5682': 2026.,
    '5910': 2087.
}
for g, p in tosetlist.iteritems():
    database[g]['capacity'] = p

# # Minimal production set by fuel type
mincapacity = {u'Biomass': 0.20,
               'Coal': 0.20,   # http://ebooks.asmedigitalcollection.asme.org/content.aspx?bookid=240&sectionid=38774800
               'Fuel Oil': 0.40,
               'Geothermal': 0.20,  # http://egec.info/wp-content/uploads/2014/10/Flex-Factsheet-Web-Version.pdf
               'Hydro': 0.10,  # http://www.nzdl.org/gsdlmod?e=d-00000-00---off-0cdl--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-about---00-0-1-00-0-0-11-1-0utfZz-8-10&a=d&cl=CL2.12&d=HASH12e30488fe16525235d00f.8.2
               'Lignite': 0.20,  # Assumed same as coal
               'Natural Gas': 0.40,   # http://www.alstom.com/Global/Power/Resources/Documents/Brochures/gas-power-plants.pdf
               'Nuclear': 0.20,  # http://www.iaea.org/NuclearPower/Meetings/2013/2013-09-04-09-06-TM-NPE.html
               'Unknown': 0.40,
               'Waste': 0.20}

for g in database.iterkeys():
    database[g]['minonlinecapacity'] = mincapacity[database[g]['primaryfuel']]*database[g]['capacity']


# # Warm start cycling costs [$/MW cap]
# # Based on data from NREL - "Power plant cycling costs" (April 2012) and
# # http://www.ipautah.com/data/upfiles/newsletters/CyclingArticles.pdf (coal)
# # http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00574921 (hydro)
cyclecost = {u'Biomass': 65,  # Assumed equal to coal
             'Coal': 65,
             'Fuel Oil': 55,  # Assumed equal to gas CCGT
             'Geothermal': 4.3,  # Assumed equal to hydro
             'Hydro': 4.3,  # Based on swedish data, in 2012 dollars
             'Lignite': 65,  # Assumed equal to coal
             'Natural Gas': 55,  # Assumes CCGT
             'Nuclear': 300,  # No source - set at large number to represent usual baseload operation
             'Unknown': 65,
             'Waste': 65}  # assumed equal to coal

for g in database.iterkeys():
    f = database[g]['primaryfuel']
    database[g]['cyclecost'] = cyclecost[f]*database[g]['capacity']

# # # Removing generators that are not connected to mainland Europe or are known duplicates
toremovelist = [
    '43804', '43815',  # Canary Islands, spain
    '42778',  # Crete, Greece
    '42779',  # Chios, Greece
    '2402',  # Duplicate of 39749
    '2638'  # Duplicate of 39746
]

database = {k: v for k, v in database.iteritems() if k not in toremovelist}


pickle.dump(database, open(metadatadir + 'generator_database_no_affiliation.pickle', 'w'))
