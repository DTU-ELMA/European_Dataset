#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAXWIND 40.0
#define STEPS 160

// Changed to use fields at 10m and 100m to interpolate hub height wind speeds.

// linear interpolation. x is the desired values,
// x is the x values of the interpolation points
// xp is the data point x values and fp is the f(x) data values.
// r is overwritten with interpolated values.
// x and xp are assumed to be increasing.
void interp(size_t inpLen, size_t outpLen, const double x[outpLen], const double xp[inpLen], const double fp[inpLen], double r[outpLen]) {

	int i,j;
	double a,b;


	j = -1;
	for (i = 0; i < outpLen; i++) {

		if (x[i] <= xp[0]) {
			r[i] = fp[0];
			continue;
		}
          
          if (x[i] >= xp[inpLen-1]) {
			r[i] = fp[inpLen-1];
			continue;
		} 

		if (x[i] > xp[j+1]) {
			while (x[i] > xp[j+1]) {
				j++;
				if (j > inpLen) {
					fprintf(stderr,"Nonincreasing interpolation values! Quitting!\n");
					exit(1);
				}
			}
			a = (fp[j+1]-fp[j])/(xp[j+1]-xp[j]);
			b = fp[j] - a*xp[j];
		} 

          r[i] = a*x[i] + b;
	}

}

/* We'll not need this anyway
double Weibull(double x, double shape, double scale) {

	double k = shape;
	double l = scale;

     if (l == 0)
          return 0.0;
	if (x > 0)
		return k/l*pow(x/l,k-1)*exp(-pow(x/l,k));
	else
		return 0.0;

}

// Smoothe a power curve by a Weibull distribution.
// Assumes the vs' are equidistant
void evaluateSmoothedPowerCurve(size_t len, const double v[len], const double powercurve[len], double result[len]) {

	size_t i,j;
	double sum;
     double average_v;
	double dt = v[1]-v[0];
     double gamma32 = 0.86582349735; // gamma(3/2)
     double scale;


     for (j = 0; j < len; j++) {
	     sum = 0.0;
          average_v = v[j];
          scale = average_v/gamma32; // Assuming shape parameter is 2
     	for (i = 0; i < len; i++) {
     		sum += powercurve[i]*Weibull(v[i],2.0,scale);
     	}
          result[j] = sum*dt;
     }

}

*/

void windLoop( size_t N, size_t M, const double windspeed10m[N][M], \
			const double windspeed100m[N][M], const _Bool onshoremap[N][M], \
			double onshoreHubHeight, double offshoreHubHeight,
			size_t onLen, const double onV[onLen], const double onPow[onLen],\
			size_t offLen, const double offV[offLen], \
			const double offPow[offLen],\
			double result[N][M])
{
	
	size_t i,j;
	double *Pow;
	double v[STEPS];
	double onshoreCurve[STEPS];
	//double onshoreSmoothedCurve[STEPS];
	double offshoreCurve[STEPS];
	//double offshoreSmoothedCurve[STEPS];
	double lnh1, lnh2, v1, v2, r;
	double H;
	double vHub;
	/*
	printf("Windloop called with\n");
	printf("N, M = %zu, %zu\n",N,M);
	printf("onshoreHubHeight: %f\n", onshoreHubHeight);
	printf("offshoreHubHeight: %f\n", offshoreHubHeight);
	printf("Power curve lengths: %zu, %zu\n", onLen, offLen);
	printf("windspeed 10m: %f\n", windspeed10m[N-1][M-1]);
	printf("windspeed 100m: %f\n", windspeed100m[N-1][M-1]);
	printf("onV: %f\n", onV[5]);
	printf("offV: %f\n", offV[5]);
	printf("onPow: %f\n", onPow[5]);
	printf("offPow: %f\n", offPow[5]);
	printf("bool: %i\n", (int) onshoremap[N-1][M-1]);
	*/
	for (i = 0; i < STEPS; i++) {
		v[i] = (MAXWIND*1.0)/(STEPS*1.0)*i;
	}

	interp(onLen,STEPS,v,onV,onPow,onshoreCurve);
	interp(offLen,STEPS,v,offV,offPow,offshoreCurve);

     //evaluateSmoothedPowerCurve(STEPS,v,onshoreCurve,onshoreSmoothedCurve);
     //evaluateSmoothedPowerCurve(STEPS,v,offshoreCurve,offshoreSmoothedCurve);
/*
     printf("#Power curve:\n");
     for (i = 0; i < STEPS; i++) {
          printf("%f\t%f\t%f\n", v[i], onshoreCurve[i], offshoreCurve[i]);
     }
     printf("#Smoothed:\n");
     for (i = 0; i < STEPS; i++) {
          printf("%f\t%f\t%f\n", v[i], onshoreSmoothedCurve[i], offshoreSmoothedCurve[i]);
     }
*/
     lnh1 = log(100.);
     lnh2 = log(10.);
     r = lnh2 - lnh1; // ln(h2/h1)
	for (i = 0; i < N; i++) {
		for (j = 0; j < M; j++) {
//			printf("Iter: %zu\t %zu\t",i,j);
//			r = roughness[i][j];
			if (onshoremap[i][j]) {
				H = onshoreHubHeight;
				Pow = onshoreCurve;
			} else {
				H = offshoreHubHeight;
				Pow = offshoreCurve;
			}

			
//			if (r <= 0.0)
//				r = 0.0002;

			//d = r*2.0/3.0;
//			d = 0.0; // Don't include displacement height.
			v1 = windspeed10m[i][j];
			v2 = windspeed100m[i][j];
			vHub = ((v2 - v1)*log(H) + v1*lnh2 - v2*lnh1) / r;
//			printf("result\t");
               interp(STEPS,1,&vHub, v, Pow, &result[i][j]); 
//			printf("\n");
		}
	}

	return;
}
