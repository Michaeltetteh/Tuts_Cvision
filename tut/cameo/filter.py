import cv2 as cv 
import numpy as np 
import utils


class VconvolutionFilter(object):
	"""A filter that applies a convolution to V (or all BGR)"""
	def __init__(self,kernel):
		self._kernel = kernel

	def apply(self,src,dst):
		"""Apply filter with BGR or gray src/dst"""
		cv.filter2D(src,-1,self._kernel,dst)

class SharpenFilter(object):
	"""docstring for SharpenFilter
		A sharpen filter with 1-pixel radius"""
	def __init__(self):
		kernel = np.array([[-1,-1,-1],
							[-1,9,-1],
							[-1,-1,-1]])
		VconvolutionFilter.__init__(self,kernel)


class FindEdgefilter(VconvolutionFilter):
	"""edge finding filter with 1-pixel radius"""
	def __init__(self):
		kernel = np.array([[0.04,0.04,0.04,0.04,0.04],
						   [0.04,0.04,0.04,0.04,0.04],
						   [0.04,0.04,0.04,0.04,0.04],
						   [0.04,0.04,0.04,0.04,0.04],
						   [0.04,0.04,0.04,0.04,0.04]])
		VconvolutionFilter.__init__(self,kernel)

		
def strokeEdges(src,dst,blurKsize=7,edgeKsize=5):
	if blurKsize >= 3:
		blurredSrc = cv.medianBlur(src,blurKsize)
		graySrc = cv.cvtColor(blurredSrc,cv.COLOR_BGR2GRAY)
	else:
		graySrc = cv.cvtColor(src,cv.COLOR_BGR2GRAY)
	cv.Laplacian(graySrc,cv.CV_8U,graySrc,ksize=edgeKsize)
	normalizeInverseAlpha = (1.0 / 255) * (255 - graySrc)
	channels = cv.split(src)
	for channel in channels:
		channel[:] = channel * normalizeInverseAlpha
	cv.merge(channels,dst)

