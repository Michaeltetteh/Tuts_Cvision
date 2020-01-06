import cv2 as cv
import numpy as np

class WindowManager(object):

	def __init__(self, windowName, keypressCallback=None):
		self.keypressCallback = keypressCallback
		self._windowName = windowName
		self._isWindowCreated = False


	@property
	def isWindowCreated(self):
		return self._isWindowCreated

	def createWindow(self):
		cv.namedWindow(self._windowName)
		self._isWindowCreated = True

	def show(self):
		cv.imshow(self._windowName,frame)

	def destroyWindow(self):
		cv.destroyWindow(self._windowName)
		self._isWindowCreated = False

	def processEvents(self):
		keycode = cv.waitKey(1)
		if self.keypressCallback is not None and keycode != -1:
			keycode &= 0xFF
			self.keypressCallback(keycode)
	