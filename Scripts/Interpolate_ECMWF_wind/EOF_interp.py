import numpy as np
import scipy.interpolate as interpolate
from itertools import izip

def do_EOF_interpolation(ts,cutindx,fullindx):
	'''
	EOF interpolation on the time series ts.
	ts: T by NxMx.. array of field slices
	cutindx: Times from which the time series should be interpolated
	fullindx: Times for the output time series.
	'''
	tsshape = ts[0].shape
	fcts = np.array([w.flatten() for w in ts[cutindx]])
	fctsmean = np.mean(fcts,axis=0)
	fcts -= fctsmean
	
	interpindx = np.setdiff1d(fullindx,cutindx)
	
	# Problem: Find vector C: F^T F C = l C
	# Let D = F C
	# We find D: F F^T D = l D
	# Then C = F^T D / l
	S = np.dot(fcts,fcts.T) # Ignore factor 1/(n-1) as it doesn't impact results.
	vals, tvecs = np.linalg.eig(S)
	vecs = np.dot(fcts.T,tvecs)
	norms = np.apply_along_axis(np.linalg.norm,0,vecs)
	vecs /= norms
	print 'QR decomposition'
	vecs2, factors = np.linalg.qr(vecs)
	# Projects states F(t) on eigenstates to get eigenvalue timeseries
	print 'Do Projection'
	proj = np.dot(vecs2.T,fcts.T)
	print 'Do Interpolation'
	iproj = np.array([interpolate.UnivariateSpline(cutindx,projt,k=3,s=0)(interpindx) for projt in proj])
	print 'Construct outgoing time series'
	its = np.dot(iproj.T,vecs2.T)
	#its = [np.sum((l*v for v in vecs2.T),axis=0) for l in iproj]
	outts = np.zeros(shape = (len(fullindx),len(fcts[0])))
	outts[cutindx] = fcts
	outts[interpindx] = its
	outts += fctsmean
	def toimg(X):
		return np.reshape(X,tsshape)
	return np.array([toimg(X) for X in outts])

