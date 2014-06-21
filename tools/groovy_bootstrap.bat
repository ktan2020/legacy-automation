@ECHO OFF
REM = '''
groovy "%~dp0%~nx0" %*
GOTO :EOF
'''
@interface ECHO {}
	 
def packages = new File(System.getenv()['TOOLCHAIN'] + File.separator + "grape.list")
packages.eachLine {
	regex = (it =~ /([-\.a-zA-Z]+) *([-\.a-zA-Z]+) *(\[.*\])/)
	
	if (regex.matches()) {
		println " * package: [" + regex[0][1] + "] [" + regex[0][2] + "]"
		str = "grape.bat install " + regex[0][1] + " " + regex[0][2]
		println "   => Running: " + str
		def p = str.execute()
		p.in.eachLine { l -> println l }
		p.waitFor()
		//new BufferedReader(new InputStreamReader(System.in)).readLine()
	}
}

System.exit(0)