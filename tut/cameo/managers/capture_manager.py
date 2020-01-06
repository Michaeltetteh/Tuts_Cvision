import cv2 as cv
import numpy as np
import time

class CaptureManager(object):
	
	def __init__(self,capture,previewWindowManager = None,shouldMirrorPreview=False):
		self.previewWindowManager = previewWindowManager
		self.shouldMirrorPreview = shouldMirrorPreview
		self._channel = 0
		self._capture = capture
		self._enteredFrame = False
		self._frame = None
		self._imageFileName = None
		self._videoFileName = None
		self._videoEncoding = None
		self._videoWriter = None
		self._startTime = None
		self._framesElapsed = 0
		self._fpsEstimate = None

	@property
	def channel(self):
		return self._channel
	
	@channel.setter
	def channel(self,value):
		if self._channel != value:
			self._channel = value
			self._frame = None

	@property
	def frame(self):
		if self._enteredFrame and self._frame is None:
			_,self._frame = self._capture.retrieve()
		return self._frame
	
	@property
	def isWritingImage(self):
		return self._imageFileName is not None

	@property
	def isWritingVideo(self):
		return self._videoFileName is not None


	def enterFrame(self):
		"""Captures the next frame if any"""
		# First lets check that any previous frame was exited
		assert not self._enteredFrame, "previous enterFrame() had no matching exitFrame()"

		if self._capture is not None:
			self._enteredFrame = self._capture.grab()

	def exitFrame(self):
		"""Draw to the window, write to file. release the frame"""
		# check whether any grabbd frame is retrievable
		# The getter may retieve anf cache the frame.
		if self.frame is None:
			self._enteredFrame = False
			return

		# update the FPS estimate and related variables
		if self._framesElapsed == 0:
			self._startTime = time.time()
		else:
			timeElapsed = time.time() - self._startTime
			self._fpsEstimate = self._framesElapsed/timeElapsed
		self._framesElapsed += 1

		# Draw to the window if any
		if self.previewWindowManager is not None:
			if self.shouldMirrorPreview:
				mirroredFrame = np.fliplr(self._frame).copy()
				# print(mirroredFrame)
				# self.previewWindowManager.show(mirroredFrame)
			else:
				self.previewWindowManager.show(self._frame)

		# write to the image file
		if self.isWritingImage:
			cv.imwrite(self._imageFileName,self._frame)
			self._imageFileName = None

		# write to video file if any
		self._writeVideoFrame()

		# release the frame
		self._frame = None
		self._enteredFrame = False


	def writeImage(self, filename):
		"""Write the next exited frame to an image file"""
		self._imageFileName = filename

	def startWritingVideo(self,filename,encoding=cv.VideoWriter_fourcc('I','4','2','0')):
		"""Start to write exited frame to file"""
		self._videoFileName = filename
		self._videoEncoding = encoding

	def stopWritingVideo(self):
		"""stop writing exited frame to video file"""
		self._videoFileName = None
		self._videoEncoding = None
		self._videoWriter = None
	
	def _writeVideoFrame(self):
			
			if not self.isWritingVideo:
				return

			if self._videoWriter is None:
				fps = self._capture.get(cv.CAP_PROP_FPS)
				if fps == 0.0:
					# the captures fps is unknown  so use estimate
					if self._framesElapsed < 20:
						# wait untill more frames elapse so that the 
						# estimate is more stable
						return
					else:
						fps = self._fpsEstimate
				size = (int(self._capture.get(
						cv.CAP_PROP_FRAME_WIDTH)),
						int(self._capture.get(cv.CAP_PROP_FRAME_HEIGHT)))
				self._videoWriter = cv.VideoWriter(self._videoFileName,self._videoEncoding,fps,size)
			self._videoWriter.write(self._frame)

			