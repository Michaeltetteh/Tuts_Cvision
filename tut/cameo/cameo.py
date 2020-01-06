import cv2 as cv
from managers.capture_manager import CaptureManager
from managers.window_manager import WindowManager


class Cameo(object):
	

	def __init__(self):
		self._windowManager = WindowManager('Cameo',self.onKeypress)
		self._captureManager = CaptureManager(cv.VideoCapture(0),self._windowManager,True)


	def run(self):
		"""Runs the main program loop"""
		# self._windowManager = WindowManager('Cameo',self.onKeypress)
		self._windowManager.createWindow()
		while self._windowManager.isWindowCreated:
			self._captureManager.enterFrame()
			frame = self._captureManager.frame

			# TODO: filter frame

			self._captureManager.exitFrame()
			self._windowManager.processEvents()


	def onKeypress(self,keycode):
		"""Handles key press
			space -> Take screenshot
			tab -> start/stop recording a screencast
			escape -> Quit
		"""
		if keycode == 32: #space
			self._captureManager.writeImage('screenshot.png')
		elif keycode == 9: #tab
			if not self._captureManager.isWritingVideo:
				self._captureManager.startWritingVideo('screencast.avi')
			else:
				self._captureManager.stopWritingVideo()
		elif keycode == 27: #escape
			self._windowManager.destroyWindow()


if __name__ == "__main__":
	Cameo().run()