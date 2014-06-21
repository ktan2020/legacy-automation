#
# Generic DB Interface Abstraction Library
#

import sys
import os
import jpype
from robot.api import logger


logger.debug(" ... Importing ext_dbi library ... ")

class ext_dbi:

    def __init__(self):
        logger.debug(" ... in ext_dbi constructor ... ")
            
    def start_jdbc(self):
        logger.debug(" ... in ext_dbi.start_jdbc ... ")
        if sys.platform.startswith('linux'):
		    jpype.startJVM(os.path.join(os.sep, 'opt','lin','java','latest','jre','lib','i386','client','libjvm.so'), "-Djava.class.path=%s" % os.path.join(os.getenv('TOOLCHAIN'), 'libs', 'jdbc', 'ojdbc5.jar'))
        else:
            jpype.startJVM(os.path.join(os.getenv('TOOLCHAIN'),'jre','jre6','bin','client','jvm.dll'), "-Djava.class.path=%s" % os.path.join(os.getenv('TOOLCHAIN'), 'libs', 'jdbc', 'ojdbc5.jar'))

    def stop_jdbc(self):
        logger.debug(" ... in ext_dbi.stop_jdbc ... ")
        jpype.shutdownJVM()
		