import ConfigParser
from optparse import (OptionParser,BadOptionError,AmbiguousOptionError)
import subprocess, sys, os, datetime
from Timer import Timer


class Alarm(Exception): pass

class PassThroughOptionParser(OptionParser):
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError,AmbiguousOptionError), e:
                largs.append(e.opt_str)
  
def vararg_cb(option, opt_str, value, parser):
    assert value is None
    value = []
    for arg in parser.rargs:
        if arg[:2]=="--" and len(arg)>2: break
        value.append(arg)
    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)
      
parse = PassThroughOptionParser(usage="Usage: %prog [options]")
parse.add_option("--env", action="callback", callback=vararg_cb, dest="env", help="which env to use. See XXX for more info.")


(options,args) = parse.parse_args()

print " => options: %s" % options 
print " => args:    %s" % args  
 
if options.env == None:
    sys.stderr.write("XXX FATAL: Missing param XXX\n")
    sys.exit(1)


config = ConfigParser.ConfigParser()
config.read(os.path.join(os.getenv("TOOLCHAIN"),"conf","env.ini"))
keys = ['username','password']

DBSERVER = os.getenv("DBSERVER")
if DBSERVER == None or DBSERVER == "":
    sys.stderr.write("XXX FATAL: DBSERVER needs to be defined as an var XXX\n")
    sys.exit(1) 


for env in options.env:
    TIMEOUT_OCCURRED = False
    
    if sys.platform.startswith("linux"):
        import signal
        
        def alarm_handler(signum, frame):
            raise Alarm
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(3*60) # give db 3 minutes to complete
        
        try:      
            values = map(lambda k: config.get(env,k), keys)
            
            with Timer() as t:
                print " => Refreshing db for [%s] env: %s/%s@%s/%s ... " % (env,values[0],values[1],DBSERVER,values[2])
                p = subprocess.Popen("connect %s/%s@%s/%s"%(values[0],values[1],DBSERVER,values[2]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
                map(lambda x: sys.stdout.write(x), iter(p.stdout.readline,""))
                rc = p.wait()     
            print " ... Done! => db connect for [%s] took: [%s] " % (env,str(datetime.timedelta(seconds=t.secs)))
                
            signal.alarm(0)  
        except Alarm:
            TIMEOUT_OCCURRED = True
            p.terminate()
            signal.alarm(0)
                    
        if TIMEOUT_OCCURRED: 
            sys.stderr.write(" !!!! WARN: [timedout after 3 mins] connect returned an error code for [%s] !!!!\n" % env)
            sys.exit(1)
        
    else:        
        sys.stderr.write("XXX FATAL: This script only works on Linux XXX")
        sys.exit(1) 