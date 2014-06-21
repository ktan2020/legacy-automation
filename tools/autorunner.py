#
# Integrated runner 
#

import os, sys, glob, string, subprocess, time, re, socket, datetime
import ConfigParser
from optparse import OptionParser, OptionGroup
from Timer import Timer
from hurry.filesize import size


print "sys.argv = ", sys.argv
CWD = os.getcwd()
if sys.platform.startswith("linux"):
	print "@@@ [script: %s] [pwd: %s] [host: %s] @@@" % (sys.argv[0], CWD, os.popen("ifconfig | grep -A 2 'eth' | grep 'inet addr:' | cut -d':' -f2 | awk '{print $1}'").read().strip())


# optionparser cb
def vararg_cb(option, opt_str, value, parser):
	assert value is None
	value = []
	for arg in parser.rargs:
		if arg[:2]=="--" and len(arg)>2: break
		value.append(arg)
	del parser.rargs[:len(value)]
	setattr(parser.values, option.dest, value)
	
parse = OptionParser(usage="Usage: %prog [options] test_script [test_scripts]")
parse.add_option("--dry-run", action="store_true", dest="dryrun", default=False, help="dry run mode - Don't actually do it, just pretend and go through the motions.")
parse.add_option("--env", action="store", dest="env", type="string")
parse.add_option("--tag", dest="tag", action="callback", callback=vararg_cb)
parse.add_option("--ie", action="store_true", dest="ie", default=False, help="Use IE WebDriver. This will launch IE instead of the default Firefox.")
parse.add_option("--chrome", action="store_true", dest="chrome", default=False, help="Use Chrome WebDriver. This will launch Chrome instead of the default Firefox.")
parse.add_option("--safari", action="store_true", dest="safari", default=False, help="Use Safari WebDriver. This will launch Safari instead of the default Firefox.")
parse.add_option("--phantomjs", action="store_true", dest="phantom", default=False, help="Use PhantomJS WebDriver. This will launch PhantomJS instead of the default Firefox.")

group = OptionGroup(parse, "Debug options")
group.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Break into python debugger on first fail.")
group.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose mode.")
group.add_option("-b", "--batch", action="store_true", dest="batch", default=False, help="RobotFramework batch mode.")
group.add_option("-p", "--pause", action="store", dest="pause", type="string", metavar="[secs pause]", default="1.0", help="Pause in seconds in between each run. [Default set to 1.0s]")

parse.add_option_group(group)


if len(sys.argv)==1 or sys.argv[0]=='-h' or sys.argv[0]=='--help' or sys.argv[0]=='-help': 
	parse.print_help()
	sys.exit(1)

(options,args) = parse.parse_args()
if options.verbose:
	print " => options: %s" % str(options) 
	print " => args:    %s" % str(args)



# XXX FIXME XXX
import params
if options.ie or options.safari:
	if sys.platform != "win32":
		sys.stderr.write("!!! WARN: You selected to run IE on a non-Windows platform. Defaulting to Firefox !!!\n")
	else:	
		if options.ie:
			print " => Using IE Webdriver"
			params.BROWSER = 'Ie'
		elif options.safari:
			print " => Using Safari Webdriver"
			params.BROWSER = 'Safari'
elif options.chrome:
	print " => Using Chrome Webdriver"
	params.BROWSER = 'Chrome'
elif options.phantom:
	print " => Using PhantomJS Webdriver"
	params.BROWSER = 'PhantomJS'
else:
	print " => Using default Firefox Webdriver"
import sst.config
sst.config.browser_type = params.BROWSER



# hosts.ini is only for Windows platform 
if HOST==None or DB==None: 
	HOSTS_INI = "hosts.ini"
	if os.path.exists(HOSTS_INI): 
		config = ConfigParser.ConfigParser()
		config.read(HOSTS_INI)
		
		if not all(map(config.has_section, ['HOST','DB'])): 
			sys.stderr.write(" XXX Fatal Error XXX\n ")
			sys.exit(1)
		
		if HOST==None: 
			HOST = config.get('HOST','host')
		if DB==None: 
			DB = config.get('DB','db',None)
	
	if HOST==None or DB==None: 
		sys.stderr.write(" XXX Fatal Error XXX\n ")
		sys.exit(1)
# End of hosts.ini

	
	
def seed_sequence_list(l):
	import random
	random.shuffle(l)	
	return l

def generate_runlist(l):
	r = []
	for (seq,tc) in enumerate(l,1):
		# from testcase name get actual testcase file (filename). testcase = testcase file - file extension
		files = glob.glob(tc + "*")
		files = sorted(files)
		
		# check to make sure TC file(s) actually exists and match the TC in runlist
		if len(files)==0: 
			sys.stderr.write("!!! WARN: Can't find TC: %s in current dir: %s !!!\n" % (tc,os.getcwd()))
			continue
		
		filename = files[0]	# container is always first	after sorting
		
		# if multiple TC files found, need to make sure container file exists
		if len(files)>1:
			if options.verbose: print " [%s] => glob(TC*) returned => %s " % (tc,str(files))
		
			if os.path.splitext(filename)[-1]!='':
				print "!!! WARN: Inconsistency in TC detected. It appears that you have multiple files for TC (%s) but no container for it. Skipping !!!" % (tc)
				continue

		print "	@@@ (%d) [%s] @@@ " % (seq,filename) 
		r.append(create_runner(filename))				
	return r		

	
import generic_testloader
loader = generic_testloader.generic_testloader()
	
def create_runner(file):
	(name,ext) = os.path.splitext(file)
	if   ext == ".txt":
		return PyBotRunner(name, file)
	elif ext == ".py":
		return PyTestRunner(name, file)
	elif ext == ".xml":
		return SoapUIRunner(name, file)
	elif ext == "":
		return ContainerRunner(name, file)
	else:
		raise NotImplementedError("No runner found for this file type.") 

class AbstractRunner(object):
	def __init__(self, name, file):
		self.name = name
		self.file = file
		self.seq = 0
		
	def __str__(self):
		return "#%d. [%s (%s)] => [%s]"%(self.seq,self.file,self.name,self.__class__.__name__)
		
	def run(self):
		raise NotImplementedError
	
	
from functools import wraps
def run(s):
	@wraps(s)
	def wrapper(*args):
		args[0].seq = [ i.name for i in runlist ].index(args[0].name)+1
		status = " [%d / %d] " % (args[0].seq, len(runlist))
		pad = (78-len(status))/2
		print "%s%s%s" % ("<"*pad,status,">"*pad)
		
		if options.pause: 
			if options.verbose: 
				print " ... sleeping for %s s between runs ... " % options.pause
			time.sleep(float(options.pause))
		with Timer() as t:
			result = s(*args)
		status = " [%s] " % (str(datetime.timedelta(seconds=t.secs)))
		pad = (78-len(status))/2
		print "%s%s%s" % (">"*pad,status,"<"*pad) 

		return result
	return wrapper
	
class PyBotRunner(AbstractRunner):
	def __init__(self, name, file):
		AbstractRunner.__init__(self, name, file)
		
	@run	
	def run(self):
		if options.verbose: print " @@@ in PyBotRunner (%s) @@@ " % self.file	

		rc = 0
		if not options.batch:
			os.putenv('DB_PROPERTIES',db_prop)
			try:
				rc = loader.run_pybot(self.file)
			except AssertionError: 
				rc = 1
				
		else:
			from robot.api import TestSuite, TestSuiteBuilder
			suite = TestSuite(str(self))
			suite.imports.resource("common_resource.txt")
			suite.imports.library("generic_testloader")
			t = suite.tests.create(name=self.name)
			t.keywords.create("Set Environment Variable", args=["DB_PROPERTIES",db_prop])
			t.keywords.create("Run Pybot", args=[self.file])			
			rc = suite.run(loglevel=os.getenv('ROBOT_SYSLOG_LEVEL'), outputdir=os.path.join(os.getenv('ROBOT_REPORTDIR'),self.name))
			#debugfile=os.getenv('ROBOT_DEBUGFILE')
			rc = rc.return_code		
		return rc
	
class PyTestRunner(AbstractRunner):
	def __init__(self, name, file):
		AbstractRunner.__init__(self, name, file)
		
	@run	
	def run(self):
		if options.verbose: print " @@@ in PyTestRunner (%s) @@@ " % self.file

		rc = 0
		if not options.batch:
			os.putenv('DB_PROPERTIES',db_prop)
			try:
				rc = loader.run_pytest(self.file, debug=options.debug)
			except AssertionError:
				rc = 1
				
		else:
			from robot.api import TestSuite, TestSuiteBuilder
			suite = TestSuite(str(self))
			suite.imports.resource("common_resource.txt")
			suite.imports.library("generic_testloader")
			t = suite.tests.create(name=self.name)
			t.keywords.create("Set Environment Variable", args=["SCREENSHOT_DIR",os.getenv('ROBOT_REPORTDIR')+'/'+'SEL-SCREENSHOTS'])
			t.keywords.create("Set Environment Variable", args=["DB_PROPERTIES",db_prop])
			t.keywords.create("Run Pytest", args=[self.file])			
			rc = suite.run(loglevel=os.getenv('ROBOT_SYSLOG_LEVEL'), outputdir=os.path.join(os.getenv('ROBOT_REPORTDIR'),self.name))
			#debugfile=os.getenv('ROBOT_DEBUGFILE')
			rc = rc.return_code		
		return rc
			
class SoapUIRunner(AbstractRunner):
	def __init__(self, name, file):
		AbstractRunner.__init__(self, name, file)
		
	@run	
	def run(self):		
		if options.verbose: print " @@@ in SoapUIRunner (%s) @@@ " % self.file
		
		rc = 0
		if not options.batch:
			os.putenv('DB_PROPERTIES',db_prop)
			rc = loader.run_makesuds(self.file)
			
		else:
			from robot.api import TestSuite, TestSuiteBuilder
			suite = TestSuite(str(self))
			suite.imports.resource("common_resource.txt")
			suite.imports.library("generic_testloader")
			t = suite.tests.create(name=self.name)
			t.keywords.create("Set Environment Variable", args=["NO_SOAPUI_REPORT","1"])
			t.keywords.create("Set Environment Variable", args=["SOAPUI_LOGSDIR",os.getenv('ROBOT_REPORTDIR')+'/'+self.name+'/'+'SOAPUI_LOGS'])
			t.keywords.create("Set Environment Variable", args=["DB_PROPERTIES",db_prop])
			t.keywords.create("Run Makesuds", args=[self.file])
			t.keywords.create("Soapui Project Passed", args=[os.getenv('ROBOT_REPORTDIR')+'/'+self.name+'/'+'SOAPUI_LOGS/soapui-errors.log']) # dirty hack since create doesn't expand vars
			rc = suite.run(loglevel=os.getenv('ROBOT_SYSLOG_LEVEL'), outputdir=os.path.join(os.getenv('ROBOT_REPORTDIR'),self.name))
			#debugfile=os.getenv('ROBOT_DEBUGFILE')
			rc = rc.return_code		
		return rc		
	
class ContainerRunner(AbstractRunner):
	def __init__(self, name, file):		
		AbstractRunner.__init__(self, name, file)
		lines = open(file).read().split()
		if not all(map(lambda l: os.path.splitext(l)[0]==name, lines)): 
			sys.stderr.write(" XXX Serious Error: TestCase (%s) contains sub-testcase(s) that do not belong to it. XXX \n " % name)
			sys.exit(1)
		self.runners = map(lambda l: create_runner(l), lines)
	
	@run
	def run(self):
		if options.verbose: print " @@@ in ContainerRunner (%s) @@@ " % self.file	
		
		rc = 0
		if not options.batch:
			for r in self.runners:
				if r.run()==1: 
					rc=1
					break 

		else:
			from robot.running import TestSuite, TestSuiteBuilder
			suite = TestSuite(str(self))
			suite.imports.resource("common_resource.txt")
			suite.imports.library("generic_testloader")
			t = suite.tests.create(name=self.name)
			
			for r in self.runners:
				if isinstance(r,RobotRunner):
					t.keywords.create("Run Pybot", args=[r.file])	
					t.keywords.create("Set Environment Variable", args=["DB_PROPERTIES",db_prop])
				
				elif isinstance(r,PyTestRunner):
					t.keywords.create("Set Environment Variable", args=["SCREENSHOT_DIR",os.getenv('ROBOT_REPORTDIR')+'/'+'SEL-SCREENSHOTS'])
					t.keywords.create("Set Environment Variable", args=["DB_PROPERTIES",db_prop])
					t.keywords.create("Run Pytest", args=[r.file])
				
				elif isinstance(r,SoapUIRunner):
					t.keywords.create("Set Environment Variable", args=["NO_SOAPUI_REPORT","1"])
					t.keywords.create("Set Environment Variable", args=["SOAPUI_LOGSDIR",os.getenv('ROBOT_REPORTDIR')+'/'+r.name+'/'+'SOAPUI_LOGS'])
					t.keywords.create("Set Environment Variable", args=["DB_PROPERTIES",db_prop])
					t.keywords.create("Run Makesuds", args=[r.file])
					t.keywords.create("Soapui Project Passed", args=[os.getenv('ROBOT_REPORTDIR')+'/'+r.name+'/'+'SOAPUI_LOGS/soapui-errors.log']) # dirty hack since create doesn't expand vars
			
			rc = suite.run(loglevel=os.getenv('ROBOT_SYSLOG_LEVEL'), outputdir=os.path.join(os.getenv('ROBOT_REPORTDIR'),r.name)) #debugfile=os.getenv('ROBOT_DEBUGFILE') XXX not working ???
			rc = rc.return_code		
		return rc	


# run list containing different Runner instances	
runlist = []


db_prop = ""
if options.env != None:
	### run using specified env ###
	ENV_INI = options.env_file if options.env_file else os.path.join(os.getenv('TOOLCHAIN'),"conf","env.ini")

	if not os.path.exists(ENV_INI):
		sys.stderr.write(" XXX Fatal Error: ENV_INI - %s not found. XXX\n " % ENV_INI)
		sys.exit(1)
		
	config = ConfigParser.ConfigParser()
	config.optionxform = str
	config.read(ENV_INI)
	
	# get tclist: this can be either specified via --tag parameter or via env.ini tag ini variable 
	for sect in config.sections():
		def _find_(K,V):
			s=re.compile('\[(.*?)\]').search(V)
			if s: 
				V=V.replace(s.group(), config.get(s.group(1), K))
				_find_(K,V)
			return V
	
		for (k,v) in config.items(sect):
			config.set(sect,k,_find_(k,v))
	
	env_properties = dict(config.items(options.env.upper()))
	
	for k,v in { i: env_properties[i] for i in ['user','password','db','dbPort'] }.items():
		db_prop = db_prop + " -P%s=%s " % (k,v) 
	
	# get set of tags and set to options
	options.tag = options.tag if options.tag else env_properties['tag'].split() if 'tag' in env_properties else None
		
	if options.verbose:
		print " => env_properties: %s" % env_properties
		print " => db_prop: %s" % db_prop


if options.runlist != None:
	### run in list mode ###
	tclist = open(options.runlist).read().split()
	if options.verbose: print " *** tc running sequence: %s *** " % str(tclist)
	
elif options.tag != None:
	### run in tag mode ###
	TAG_INI = "tag.ini"
	
	if not os.path.exists(TAG_INI):
		sys.stderr.write(" XXX Fatal Error: tag not found. XXX\n ")
		sys.exit(1)
	
	tclist = set()
	taglist = map(lambda s: s.upper(), options.tag)
	
	config = ConfigParser.ConfigParser()
	# generate tc list from tags
	config.read(TAG_INI)
	
	for tag in taglist:
		try:
			tclist = tclist.union(set(config.get(tag, 'tc').split()))
		except ConfigParser.NoSectionError as e: 
			sys.stderr.write(" *** Error! %s *** \n" % str(e))

	if not tclist: 
		sys.stderr.write("!!! WARN: No test cases were found !!! \n")
		sys.exit(0)

	tclist = sorted(list(tclist)) 
	if options.verbose: print " *** tc running sequence: %s *** " % str(tclist)	
		
else:
	### run in user-specified file or glob mode ###
	tclist = []
	
	for file in args:
		if not os.path.exists(file):
			sys.stderr.write("XXX Error! Can't find the file: [%s] XXX\n" % file)
				
		elif os.path.isdir(file) and os.getcwd()==os.path.abspath(file):
			tclist.extend(list(set(map(lambda x: os.path.splitext(x)[0], glob.glob("TC*")))))
			
		else:
			tclist.append(file)


# from tclist generate runlist - runlist contains runner object instances 			
if len(tclist)==0: 
	sys.stderr.write(" XXX Fatal Error: runner was not able to generate TC list. XXX\n ")
	sys.exit(0)
	
# validate file names to make sure they conform to naming convention TC[0-9]{5}.py
m = map(re.compile("^TC[0-9]{5}$").search, map(lambda x: os.path.splitext(x)[0], tclist))
if not all(m):
	sys.stderr.write(" XXX Fatal Error: TC %s does not meet naming convention. XXX\n " % [ tclist[j] for j in [ i for i in range(len(m)) if not m[i] ] ])
	sys.exit(1)
	

with Timer() as t:
	runlist = generate_runlist(tclist)
if options.verbose:  print " $$$ generate_runlist took: %s $$$ " % (str(datetime.timedelta(seconds=t.secs)))
if len(runlist) != len(tclist):
	sys.stderr.write("!!! WARN: Detected some TC(s) is/are missing from filesystem. !!!\n")
	_ = [ j for j in tclist if j not in [ i.name for i in runlist ] ]
	sys.stderr.write("The following TC's are missing: %s \n" % _)
	sys.stderr.write("!!! Expected: [%d], Present: [%d], Missing: [%d] !!!\n" % (len(tclist),len(runlist),len(_)))
runlist = seed_sequence_list(runlist)


# check runlist list
if len(runlist)==0: 
	sys.stderr.write(" XXX Fatal Error: runner was not able to generate list of TC runner(s). XXX\n ")
	sys.exit(0)


# now start running	
if options.dryrun:
	# dry-run mode
	_ = [ i.name for i in runlist]
	print "*** The following testscripts will be run => # [%d]:%s ***" % (len(_),_)
	sys.exit(0)
else:	
	# remove all report dirs first before running
	import shutil
	if options.batch:
		for r,d,f in os.walk(os.getcwd()):
			d = map(lambda x: (lambda y: os.path.join(y,x))(r), filter(re.compile(os.getenv('ROBOT_REPORTDIR'), re.I).search, d))
  			if d:
  				if options.verbose:	print " ... removing %s ... " % d
  				shutil.rmtree(d[0], True)
  	else:
  		if options.verbose:	print " ... removing screenshots dir ... "
  		shutil.rmtree(os.path.join(os.getcwd(),"screenshots"),True)
  		if options.verbose:	print " ... removing soapui_logs dir ... "
  		shutil.rmtree(os.path.join(os.getcwd(),"soapui_logs"),True)
		
	import ext_robot, ext_dbi
	op = ext_robot.ext_robot()
	dbi = ext_dbi.ext_dbi()
	
	if sys.platform.startswith("linux"):
		import signal
		def _handler_(s,f):
			op.stop_display()
			print " !!! Execution was prematurely interrupted. Quitting !!! "
			sys.exit(1)
		signal.signal(signal.SIGTERM, _handler_)

	with Timer() as t:
		op.start_display()
		dbi.start_jdbc()
		
		rc = map(lambda r: r.run(), runlist) 
	
		op.stop_display()

	if options.verbose: print " $$$ setup + run + teardown took: %s $$$ " % (str(datetime.timedelta(seconds=t.secs)))
		


if options.batch:
	'''
	rbxml = []
	import fnmatch
	for r,d,f in os.walk(os.getenv('ROBOT_REPORTDIR')):
		for xml in f:
			if fnmatch.fnmatch(xml,'output.xml'): 
				rbxml.append(os.path.join(r,xml))
	'''			

	rbxml = map(lambda r: os.path.join(os.getenv('ROBOT_REPORTDIR'),r,'output.xml'), [ i.name for i in runlist ])
	if options.verbose: 
		print " => output.xml: ", rbxml
		sizes = map(lambda x: os.stat(x).st_size , rbxml)
		print " => sizes: ", sizes
		print " => total: %s" % size(reduce(lambda x,y: x+y, sizes))  
		

	# generate robotfw report and log html
	from robot.api import ResultWriter
	with Timer() as t:
		ResultWriter(*rbxml).write_results( loglevel=os.getenv('ROBOT_SYSLOG_LEVEL')+":INFO", \
                                        name='%s Test Suite' % ("" if not getattr(options,'tag',None) else options.tag), \
                                        outputdir=os.getenv('ROBOT_REPORTDIR'), \
                                        logtitle="Test Log", \
                                        reporttitle="Test Report", \
                                        output='combined.xml', \
                                        splitlog=True )
	if options.verbose: print " $$$ ResultWriter.write_results took: %s $$$ " % (str(datetime.timedelta(seconds=t.secs)))

	
	# Start of dirty hack
	buildxml = '''\
    <project name="report" default="report" basedir=".">
        <target name="report">
            <mkdir dir="@@"/>
	        <junitreport todir="@@">
                <fileset dir="." includes="**/TEST*.xml"/>
                <report format="frames" todir="@@">
                    <param name="TITLE" expression="SoapUI Test Results."/>
                </report>
            </junitreport>
        </target>
    </project>\
    '''
	buildxml = string.replace(buildxml, "@@", "soapui")
	
	with open(os.path.join(os.getenv('ROBOT_REPORTDIR'), "build.xml"),"w") as f:
		f.write(buildxml)
	
	print " Generating soapui reports. This could take a while ... "
	with Timer() as t:
		os.popen('ant -q -f %s' % os.path.join(os.getenv('ROBOT_REPORTDIR'),'build.xml')).close()
	print " ... done! \n"
	if options.verbose: print " $$$ ant took: %s $$$ " % (str(datetime.timedelta(seconds=t.secs)))
	# End of dirty hack
	
	
if options.verbose: 
	print " => rc: ", rc
	print " => runlist: ", [ i.name for i in runlist ]

if any(rc): 
	failed = [ runlist[i].name for i in [ i for i in range(len(rc)) if rc[i] ] ]
	print "=> FAILED ! :( [%03.2f%% fail]|[%d]|%s" % (float(sum(rc))*100/len(runlist),sum(rc),str(failed))
	print '''
      ______
     (( ____ \-
     (( _____
     ((_____
     ((____   ----
          /  /
         (_((

	'''        
	
	sys.exit(1)
else:
	print "=> PASSED ! :)"
	print '''
          _
         /(|
        (  :
       __\  \  _____
     (____)  -|
    (____)|   |
     (____).__|
      (___)__.|_____
    
	'''
	
	sys.exit(0)
			
