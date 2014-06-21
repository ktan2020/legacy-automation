#
# Generic Test Case Loader Library
#

import sys
from robot.api import logger


logger.debug(" ... Importing generic_testloader library ... ")


class generic_testloader:

    def __init__(self):
        logger.debug(" ... in generic_testloader constructor ... ")
            
    def run_pybot(self, tcfile=None):
        logger.debug(" ... in generic_testloader.run_pybot running [%s] ... " % tcfile)
        if tcfile==None: raise UnboundLocalError("Test case file name not defined!")
        import os
        from robot import run
        rc = run(tcfile, loglevel=os.getenv('ROBOT_SYSLOG_LEVEL'), outputdir=os.getenv('ROBOT_REPORTDIR'), debugfile=os.getenv('ROBOT_DEBUGFILE'))
        assert rc == 0
        return rc		

    def run_pytest(self, tcfile=None, debug=False):
        logger.debug(" ... in generic_testloader.run_pytest running [%s] ... " % tcfile)
        if tcfile==None: raise UnboundLocalError("Test case file name not defined!")
        import pytest
        # pytest will return 0 as all tests passed, 1 if any tests failed
        rc = pytest.main(["-s","-v", tcfile] if not debug else ["-s","-v","--pdb", tcfile])
        assert rc == 0
        return rc

    def run_makesuds(self, tcfile=None):
        logger.debug(" ... in generic_testloader.run_soapui running [%s] ... " % tcfile)
        if tcfile==None: raise UnboundLocalError("Test case file name not defined!")
        
        import subprocess
        from params import HOST, DB
        p = subprocess.Popen("makesuds -v %s %s" % (("-j %s "%(HOST if HOST else "")+("-o %s "%(DB if DB else "")),tcfile)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        map(lambda x: sys.stdout.write(x), iter(p.stdout.readline,""))
        rc = p.wait()        
        
        if rc==None: return 0
        else: return rc
        
    def run_container(self, tcfile=None):
        logger.debug(" ... in generic_testloader.run_Container ... ")
        if tcfile==None: raise UnboundLocalError("Test case file name not defined!")