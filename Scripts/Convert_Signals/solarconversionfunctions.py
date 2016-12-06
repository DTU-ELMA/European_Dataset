
from __future__ import print_function
import numpy
from numpy import zeros,log,cos,sin,tan,sqrt,abs,arcsin,arccos,ones,deg2rad
from math import pi
import datetime
import sys

VERBOSE = False

def dayNum(utcTime):
    year = utcTime.year;
    #leapyear = (year%4 == 0 and (year%100 != 0 or year%400 == 0));
    startofyear = datetime.datetime(year,1,1);
    endofyear = datetime.datetime(year,12,31);
    dayNumber = (utcTime - startofyear).days;
    numberOfDays = (endofyear - startofyear).days;

    return (dayNumber, numberOfDays);

def dayAngle(utcTime):
    (dayNumber, numberOfDays) = dayNum(utcTime);

    dayAngle = 2*pi*dayNumber/numberOfDays;

    return dayAngle;


def equationOfTime(utcTime):
    dayNumber, numberOfDays = dayNum(utcTime);
    B = 2*pi*(dayNumber-81.0)/numberOfDays;

    ET = 9.87*sin(2*B)-7.53*cos(B)-1.5*sin(B);

    return ET; # in minutes, formula found on p. 50 in Solar Engineering

def apparentSolarTime(longitude,utcTime): # in hours
    return (60*utcTime.hour + utcTime.minute + equationOfTime(utcTime) + 4*longitude)/60;

def hourAngle(longitude,utcTime):
    return 15*(apparentSolarTime(longitude,utcTime) - 12)/180.0*pi;

def solarConstant(utcTime):
    S = 1366.1; # Solar constant, in Watts/m^2, from solar engineering
    return S*(1 + 0.033*cos(dayAngle(utcTime)));


def declination(utcTime): # delta in litterature
    
    d = dayAngle(utcTime);

    decl = 0.006918 - 0.399912*cos(d) + 0.070257*sin(d) - \
         0.006758*cos(2*d) + 0.000907*sin(2*d) - \
         0.002697*cos(3*d) + 0.00148*sin(3*d);
    # This formula is found in Solar energy engineering
    # by Soteris A. Kalogirou page 55
    # It looks like some sort of fourier expansion of the simpler
    # formula above (decl = 23.45*sin(2pi/365*(284+N)) )

    return decl;

def sinSolarAltitude(latitude,longitude,utcTime):
    lat = deg2rad(latitude);
    delta = declination(utcTime);
    h = hourAngle(longitude,utcTime);
    
    return sin(lat)*sin(delta)+cos(lat)*cos(delta)*cos(h);
    # From Solar Engineering page 58

def cosSolarZenith(latitude,longitude,utcTime):
    return sinSolarAltitude(latitude,longitude,utcTime);

def sinSolarAzimuth(declination,h,sinAlpha,lat,lon,utcTime): # h = hourAngle,sinAlpha = sinSolarAltitude
       cosAlpha = sqrt(1-sinAlpha**2);
       sinz = cos(declination)*sin(h)/cosAlpha;

       mask = cos(h) <= tan(declination)/tan(lat/180.0*pi);
       morning = apparentSolarTime(lon,utcTime) < 12;
       evening = apparentSolarTime(lon,utcTime) > 12;

       sinz[mask & morning] = sin(-pi + abs(arcsin(sinz[mask & morning])));
       sinz[mask & evening] = sin(pi - arcsin(sinz[mask & evening]));

       return sinz;

def cosIncidenceAngle(latitude, declination, slope, azimuth, hourangle):
    L = deg2rad(latitude);
    d = declination;
    b = slope;
    z = azimuth; # Solar panel azimuth, not solar!
    h = hourangle;

    # Speed optimization.
    # Previously, 80% of time was spent in this function. After, only 50% is spent here.
    # (Runtime for one month from 180secs to 130secs)
    # This is the main target for future optimization - the current implementation is probably as good as it gets with just numpy...
    sb = sin(b)
    cb = cos(b)
    ch = cos(h)
    sd = sin(d)
    cod = cos(d)
    A = sb*cos(z)
    
    return sin(L)*(sd*cb + cod*ch*A) + \
        cos(L)*(ch*cb - sd*A)  \
        + cod*sin(h)*sb*sin(z);

    # Original return function
    return sin(L)*sin(d)*cos(b) - cos(L)*sin(d)*sin(b)*cos(z) + \
        cos(L)*cos(d)*cos(h)*cos(b) + sin(L)*cos(d)*cos(h)*sin(b)*cos(z) \
        + cos(d)*sin(h)*sin(b)*sin(z);
    # from page 60 in Solar Energy Engineering


def diffuseRadiation(latitude, longitude, utcTime, I, I_solar, sinalpha, mask):
    
    
    Z = sinalpha;
    ClearnessOfSkyIndex = zeros(I.shape);
    ClearnessOfSkyIndex[mask] = I[mask]/I_solar[mask];
    I_d = ones(I.shape);

    # The following formula is equation 3 in Diffuse Fraction Correlations
    # by Reindel, solar energy vol 45, no 1 pp 1-7 1990.
    # If we also had relative humidity (and temperature, which we do)
    # we would have used formula 2 instead.

    negIndex = ClearnessOfSkyIndex<-0.1;
    lowIndex = (ClearnessOfSkyIndex<=0.3);
    midIndex = (ClearnessOfSkyIndex>0.3) & (ClearnessOfSkyIndex<0.78);
    higIndex = (ClearnessOfSkyIndex >= 0.78);
    toohighIndex = ClearnessOfSkyIndex>1.1;

    # Only look at places with solar altitude above 10 degrees
    negIndex = negIndex & mask;
    lowIndex = lowIndex & mask;
    midIndex = midIndex & mask;
    higIndex = higIndex & mask;
    toohighIndex = toohighIndex & mask;

    T = float(latitude.shape[0] * latitude.shape[1]);

    if (negIndex.any() and VERBOSE):
        print("Clearness of Sky index negative! " + utcTime.ctime(), file=sys.stderr);
        print(numpy.min(ClearnessOfSkyIndex), file=sys.stderr);
        print(numpy.where(negIndex == True)[0].shape[0]/T*100, file=sys.stderr);
    if (toohighIndex.any() and VERBOSE):
        print("Clearness of Sky index (much) greater than 1! " + utcTime.ctime(), file=sys.stderr);
        print(numpy.max(ClearnessOfSkyIndex), file=sys.stderr);
        print(numpy.where(toohighIndex == True)[0].shape[0]/T*100, file=sys.stderr);
    I_d[lowIndex] = 1.020 - 0.254*ClearnessOfSkyIndex[lowIndex] + 0.0123 * Z[lowIndex];
    I_d[(lowIndex) & (I_d > 1.0)] = 1.0;
    
    I_d[midIndex] = 0.1400 - 1.749*ClearnessOfSkyIndex[midIndex] + 0.177 * Z[midIndex];
    I_d[(midIndex) & (I_d > 0.97)] = 0.97;
    I_d[(midIndex) & (I_d < 0.1)] = 0.1;

    I_d[higIndex] = 0.486*ClearnessOfSkyIndex[higIndex] - 0.182*Z[higIndex];
    I_d[(higIndex) & (I_d < 0.1)] = 0.1;

    return I_d * I;


# Example orientation function for Hay Davies model.
# This is simply the zero slope, where 
def zeroSlopeFunction(lat,lon,utcTime):
    slope = zeros(lat.shape);
    orientation = slope;
    return (slope,orientation);

def testSlopeFunction(lat,lon,utcTime):
    slope = zeros(lat.shape) + 32.*pi/180.0; # 32 degrees
    orientation = zeros(lat.shape); # Due south
    return (slope,orientation);

def fullTrackingSlopeFunction(lat,lon,utcTime):
    decl = declination(utcTime);
    h = hourAngle(lon,utcTime);
    sinAlpha = sinSolarAltitude(lat,lon,utcTime);
    Zs = sinSolarAzimuth(decl,h,sinAlpha,lat,lon,utcTime);

    slope = arccos(sinAlpha); # sin(alpha) = cos(phi)
    orientation = arcsin(Zs);

    return (slope,orientation);


#def newHayDavies(grbs,outfluxgrbs,orientationFunction):
def newHayDavies(I,O,latitude,longitude,utcTime,orientationFunction):
    """ Calculate diffuse, beam and ground reflected component of
        solar influx data, returning the sum of all three to calculate
        the radiation on a tilted surface """

    #utcTime = datetime.datetime(grbs.year,grbs.month,grbs.day,grbs.hour);
    # grbs.validDate is not updated because of some bug in pygrib;

    (slope, azimuth) = orientationFunction(latitude,longitude,utcTime);
    # (beta, Z_s) in the litterature

    Z = sinSolarAltitude(latitude,longitude,utcTime);
    # as in the article, ignore solar altitudes lower than some degrees
    # We do it to avoid dividing by zero.
    mask = Z >= sin(5.*pi/180.0);
    I_extraterrestial = zeros(I.shape);
    I_extraterrestial[mask] = solarConstant(utcTime)*Z[mask];



    # Get the diffuse, beam and ground components of radiation.
    # First get diffuse by a formla from Reindel:

    I_d = diffuseRadiation(latitude,longitude,utcTime,I,I_extraterrestial,Z,mask);

    # Then, since Ground reflected component is zero
    # in the horizontal plane (I_g_t propto (1-cos(beta)))
    # we get that I, the total radiation, is I_d + I_b,
    # I_b = beam component, and thus (see ref 1)

    I_b = zeros(I.shape);
    I_b[mask] = I[mask] - I_d[mask];

    # Next up: Calculate anisotropy index:

    A = zeros(I.shape);
    A[mask] = I_b[mask] / I_extraterrestial[mask];
    
    # Geometric factor:

    decl = declination(utcTime);
    hourangle = hourAngle(longitude,utcTime);
    R = cosIncidenceAngle(latitude, decl, slope, azimuth, hourangle)/ Z;

    # Horizontal brightening diffuse correction factor
    f = zeros(I.shape);
    f[mask] = sqrt(I_b[mask]/I[mask]);

    I_d_tilted = zeros(I.shape);
    I_d_tilted[mask] = I_d[mask] * ((1-A[mask])*(1+cos(slope[mask]))/2*(1+f[mask]*sin(slope[mask]/2)**3) + A[mask]*R[mask]);

    I_g = zeros(I.shape);
    I_g[mask] = O[mask]*(1-cos(slope[mask]))/2

    return I_d_tilted + I_b*R + I_g;

    
# ref 1: D.T Reindel et al: Evaluation of hourly tilted surface radiation models
# solar energy vol. 45 no 1 pp 9-17 1990


# This is the conversion function made by Suyash/Rachit.
# The model is apparantly found in http://pvsat.de/EurosunBeyerrobustmodel.pdf
#                  (copy in doc/ directory)
#   (A robust model for the MPP performance of different
#   types of PV-modules applied for the performance check
#   of grid connected systems)
# The performance of the model has yet to be evaluated, and maybe
# compared to the five parameter model (4353_001.pdf under doc/)
# but so far it has produced some very reasonable graphs.

def SolarPVConversion(data,c): # c is for config, apparantly
    """Conversion of radiation and temperature to solar PV power"""
    I=data[0]  #Radiation
    T=data[1]  #Temperature

    #Solar panel data
    threshold=c['threshold'] #solar radiation below which the panel stops giving useful power
    A=c['A'] # A, B, C are coefficients for the equation : P= A + B*I + C*logI and are calculated by using the three different values of solar radiation and their peak powers at 25deg C module temperature for corresponding radiations from the data sheet
    B=c['B']
    C=c['C']
    D=c['D'] #temperature power coefficient given in data sheet
    NOCT=c['NOCT'] #Nominal Operating Cell Temperature given in data sheet
    Ts=c['Ts'] #STC (Standard testing Condition) module temperature in K
    Ta=c['Ta'] #NTC (Nomial testing Condition) ambient temperature in K
    In=c['In'] #NTC radiation in W/m2
    ta=c['ta'] #transmittance times absorptance.
    
    #Mask for lower threshold to avoid taking the logarithm of 0.
    index = I>threshold
    #Convert to solar PV power
    RE = zeros(I.shape); # Reference Efficiency
    Efficiency = zeros(I.shape);
    
    RE[index] = A+B*I[index]+C*log(I[index]);

    frac = (NOCT-Ta)/In;

    Efficiency[index] = RE[index]*(1+D*(frac*I[index]+T[index]-Ts))/(1+D*RE[index]/ta*frac*I[index])

    return I*Efficiency;

