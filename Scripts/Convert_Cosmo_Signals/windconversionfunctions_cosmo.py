
from __future__ import print_function
import numpy
import numpy.ctypeslib
from numpy import log,interp,array,power,exp,pi,sqrt,zeros,max,min;
import ctypes as ct


def Weibull(x,shape,scale):

     k = shape;
     l = scale;

     arr = numpy.zeros(x.shape);
     arr[x>0] = k/l*power((x/l),k-1)*exp(-power(x/l,k));
     return arr;


def convertWind(onshoreconf,offshoreconf,windspeed,onshoremap):

     
     result = numpy.zeros_like(windspeed);
     
     # C expects contigous arrays. Numpy does not guarantee this.
     windspeed = numpy.ascontiguousarray(windspeed,dtype=numpy.double);
     onshoremap = numpy.ascontiguousarray(onshoremap,dtype=numpy.bool);

     dim = windspeed.shape;

     doublearray = numpy.ctypeslib.ndpointer(dtype=numpy.double,ndim=2,shape=windspeed.shape);
     boolarray = numpy.ctypeslib.ndpointer(dtype=numpy.bool,ndim=2,shape=windspeed.shape);
     onarray = numpy.ctypeslib.ndpointer(dtype=numpy.double,ndim=1,shape=(len(onshoreconf['POW']),));
     offarray = numpy.ctypeslib.ndpointer(dtype=numpy.double,ndim=1,shape=(len(offshoreconf['POW']),));
     size_t = ct.c_size_t;
     dbl = ct.c_double;

     windloop = ct.cdll.LoadLibrary("./windloop_cosmo.so");

     windloop.argtypes = [size_t,size_t, doublearray,
               boolarray,dbl,
               dbl,size_t,onarray,onarray,size_t,offarray,offarray,doublearray];
     windloop.windLoop(ct.c_size_t(dim[0]),ct.c_size_t(dim[1]),windspeed.ctypes,
               onshoremap.ctypes,ct.c_double(onshoreconf['H']),ct.c_double(offshoreconf['H']),
               ct.c_size_t(len(onshoreconf['POW'])), numpy.array(onshoreconf['V']).ctypes,
               numpy.array(onshoreconf['POW']).ctypes,
               ct.c_size_t(len(offshoreconf['V'])),numpy.array(offshoreconf['V']).ctypes,
               numpy.array(offshoreconf['POW']).ctypes,
               result.ctypes);

     return result;

# Bypass all that. Call the C routine instead.

     # Get wind speed at hub height
     
     onhubHeight = onshoreconf['H'];
     offhubHeight = offshoreconf['H'];

     # BIG FAT WARNING: The following assumes neutral stability,
     # a condition that is only achieved during mid day.

     
     roughness[roughness<=0.0] = 0.0002; # From wikipedia...
    # probably happens at the poles, should be investigated

     d = 2.0/3.0*roughness;
     k = windspeed / log((10 - d)/roughness);

     onspeedAtHubHeight = zeros(windspeed.shape);
     offspeedAtHubHeight = zeros(windspeed.shape);

     onm = onshoremap;
     offm = numpy.logical_not(onshoremap);

     onspeedAtHubHeight[onm] = k[onm]*log((onhubHeight - d[onm])/roughness[onm]);
     offspeedAtHubHeight[offm] = k[offm]*log((offhubHeight - d[offm])/roughness[offm]);

     # Get Weibull distribution of wind speeds at hub height
     # The found speed is used as the average of the distribution.
     # For now, the shape parameter is held fixed at 2,
     # so we get a Rayleigh distribution.
    
     maxpoints = max((onshoreconf['V'][-1], offshoreconf['V'][-1]));

     vs = numpy.arange(0,maxpoints,1);

     onV = onshoreconf['V'];
     onPOW = onshoreconf['POW'];
     onshorepowercurve = interp(vs,onV,onPOW);

     offV = offshoreconf['V'];
     offPOW = offshoreconf['POW'];
     offshorepowercurve = interp(vs,offV,offPOW);

     # Generate Weibull distribution
     shape = 2.0; # A rough guess. The mean is scale * Gamma(1+1/shape)
                  # Gamma(3/2) = 1/2 sqrt(pi)
                  # The mean is taken to be the speed at hub height
     gamma32 = 1.0/2.0*sqrt(pi)
     onscale = onspeedAtHubHeight / gamma32;
     offscale = offspeedAtHubHeight / gamma32;
   
     # Loop over all grid cells, apply a smoothed power curve
     # to data point and fill out result array.
     # This turns out to be difficult to express in numpy,
     # so if the loop is too slow, it will have to be rewritten in C.

     maxi = windspeed.shape[0];
     maxj = windspeed.shape[1];
     result = numpy.zeros(windspeed.shape);

     for i in xrange(maxi):
          for j in xrange(maxj):
               if (onshoremap[i][j]):
                    powercurve = onshorepowercurve;
                    hubscale = onscale[i][j];
                    v = onspeedAtHubHeight[i][j];
               else:
                    powercurve = offshorepowercurve;
                    hubscale = offscale[i][j];
                    v = offspeedAtHubHeight[i][j];
     
               # Only need to take into account weibull distribution restricted
               # to the support of the power curve, since the integral
               # elsewhere will be zero. That's wrong..
               
               distribution = Weibull(vs,shape,hubscale);
    
               # It's probably a bit inefficient to calculate the entire
               # convolution, as you need at most two points to do the
               # linear interpolation to get the value at the point you're
               # interested in....
               # If this is ever rewritten in C, might aswell optimize that.
               
               smoothedPowerCurve = numpy.convolve(powercurve,distribution,mode='same');
               result[i][j] = (numpy.interp([v],vs,smoothedPowerCurve))[0];

    
     return result;



