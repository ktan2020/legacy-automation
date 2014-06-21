#
# Common Robot library functions should be placed here ...
#

import sys
from robot.api import logger


logger.debug(" ... Importing ext_robot library ... ")

class ext_robot:

	def __init__(self, display_size=(1280,1024)):
		logger.debug(" ... in ext_robot constructor ... ")
		if sys.platform.startswith("linux"):
			from pyvirtualdisplay import Display
			self.display = Display(visible=0, size=display_size)
		else:
			self.display = None

			
	def start_display(self):
		logger.debug(" ... in ext_robot.start_display ... ")
		if self.display != None:
			self.display.start()


	def stop_display(self):
		logger.debug(" ... in ext_robot.stop_display ... ")
		if self.display != None:
			self.display.stop()
