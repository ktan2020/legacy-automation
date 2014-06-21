import ConfigParser
from optparse import OptionParser
import subprocess, sys, os
       

if sys.platform == "win32":
    import shutil
    shutil.rmtree(os.path.join(os.getenv('APPDATA'),'Subversion','auth'), True)  

  
cwd = os.getcwd()  

  
def vararg_cb(option, opt_str, value, parser):
    assert value is None
    value = []
    for arg in parser.rargs:
        if arg[:2]=="--" and len(arg)>2: break
        value.append(arg)
    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)
      
parse = OptionParser(usage="Usage: %prog [options] test_script [test_scripts]")
parse.add_option("--component", action="callback", callback=vararg_cb, dest="comp", help="which component's TC to run. See XXX for more info on the different Component/Module options.")


try:
    (options,args) = parse.parse_args()
except: 
    pass

print " => options: %s" % options 
print " => args:    %s" % args  
  
  
config = ConfigParser.ConfigParser()
config.read(os.path.join(os.getenv("TOOLCHAIN"),"conf","svn.ini"))

l = config.sections()

if not options.comp or options.comp == "ALL": 
    for s in l:
        p = subprocess.Popen("svn_export %s %s"%(config.get(s,"svn"),s), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        map(lambda x: sys.stdout.write(x), iter(p.stdout.readline,""))
        rc = p.wait()
        
        if rc != 0: sys.stderr.write(" !!!! WARN: svn_export failed for [%s] !!!!\n" % c)
        
        os.chdir(os.path.join(cwd,s))
        p = subprocess.Popen("rally %s" % s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        map(lambda x: sys.stdout.write(x), iter(p.stdout.readline,""))
        rc = p.wait()
        os.chdir(cwd)
        
        if rc != 0: sys.stderr.write(" !!!! WARN: rally failed for [%s] !!!!\n" % c)

else:
    for c in options.comp:
        assert c in l, "Specified option %s not in Config" % c
        
        print " !!! WARN: Removing (%s) first before svn export !!!" % c
        import shutil
        shutil.rmtree(c, True)
        
        p = subprocess.Popen("svn_export %s %s"%(config.get(c,"svn"),c if not args or not args[0] else args[0]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        map(lambda x: sys.stdout.write(x), iter(p.stdout.readline,""))
        rc = p.wait()
        
        if rc != 0: sys.stderr.write(" !!!! WARN: svn_export failed for [%s] !!!!\n" % c)
        
        os.chdir(os.path.join(cwd,c))
        p = subprocess.Popen("rally %s " % c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        map(lambda x: sys.stdout.write(x), iter(p.stdout.readline,""))
        rc = p.wait()
                
        if rc != 0: sys.stderr.write(" !!!! WARN: rally failed for [%s] !!!!\n" % c)

