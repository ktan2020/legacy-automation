 
@Grab('com.googlecode.gbench:gbench:0.2.2')
@Grab('org.testng:testng:6.3.1')
import org.testng.annotations.*
import org.testng.TestNG
import org.testng.TestListenerAdapter
import org.testng.xml.*
import gbench.*
 
 
interface Reverser {
	Object reverse(Object item)
}
 
@Benchmark
class GroovyReverser implements Reverser {
	def reverse(item) {
		if (item instanceof Number) return -item
		item.reverse()
	}
}
 
class Storer {
	def stored
	Reverser reverser = new GroovyReverser()
	def put(item) {
		stored = item
	}
	def get() {
		stored
	}
	def getReverse() {
		reverser.reverse(stored)
	}
}
 
 
class StorerIntegrationTest {
 
	private storer
 
	@BeforeClass
	def setUp() {
		storer = new Storer()
	}
 
	private checkPersistAndReverse(value, reverseValue) {
		println "[func]checkPersistAndReverse($value,$reverseValue)"
		storer.put(value)
		assert value == storer.get()
		assert reverseValue == storer.getReverse()
	}
 
	@Test(groups="G1")
	void shouldPersistAndReverseStrings() {
		def _func_name ="shouldPersistAndReverseStrings"
		println "\n== $_func_name start =="
		checkPersistAndReverse 'hello', 'olleh'
		println "== $_func_name end ==\n"
	}
 
	@Test(groups="G1")
	void shouldPersistAndReverseNumbers() {
		def _func_name ="shouldPersistAndReverseNumbers"
		println "\n== $_func_name start =="
		checkPersistAndReverse 123.456, -123.456
		println "== $_func_name end ==\n"
	}
 
	@Test(groups="G1")
	void shouldPersistAndReverseLists() {
		def _func_name ="shouldPersistAndReverseLists"
		println "\n== $_func_name start =="
		checkPersistAndReverse([1, 3, 5], [5, 3, 1])
		println "== $_func_name end ==\n"
	}
	
	@DataProvider(name = "testdata")
	public Object[][] createData() {
		[
			[
				[new Integer(2) , new Integer(4)],[new Integer(4) , new Integer(2)]
			],
			[
				[new Integer(4) , new Integer(2)],[new Integer(2) , new Integer(4)]
			],
		]
	}
 
	@Benchmark
	@Test(groups="G1",dataProvider = "testdata")
	void shouldPersistAndReverseLists2(List l_a,List l_b) {
		def _func_name ="shouldPersistAndReverseLists2($l_a,$l_b)"
		println "\n== $_func_name start =="
		checkPersistAndReverse(l_a,l_b)
		println "== $_func_name end ==\n"
	}
 
	@Test(groups="G1",expectedExceptions= [AssertionError.class ])
	void shouldPersistAndReverseNumbersError() {
		def _func_name ="shouldPersistAndReverseNumbersError"
		println "\n== $_func_name start =="
		checkPersistAndReverse 123.456, -125.456
		println "== $_func_name end ==\n"
	}
 
	@Test(groups="G1")
	@Parameters(["p_a","p_b"])
	void shouldPersistAndReverseParameter(@Optional("8876") String p_a,@Optional("-8876") String p_b) {
		def _func_name ="shouldPersistAndReverseParameter($p_a,$p_b)"
		assert p_a =="-9876"
		assert p_b =="9876"
		println "\n== $_func_name start =="
		checkPersistAndReverse(p_a as int,p_b as int)
		println "== $_func_name end ==\n"
	}
 
	@Test(groups="G1")
	@Parameters(["p_c","p_d"])
	void shouldPersistAndReverseParameterNone(@Optional("1942") String p_a,@Optional("2491") String p_b) {
		def _func_name ="shouldPersistAndReverseParameterNone($p_a,$p_b)"
		println "\n== $_func_name start =="
		checkPersistAndReverse(p_a,p_b)
		println "== $_func_name end ==\n"
	}
 
	//TimeOut testing
	@Test(groups="G1",timeOut = 1000L , expectedExceptions= [org.testng.internal.thread.ThreadTimeoutException.class] )
	public void infinity() {
		def _func_name ="infinity"
		println "\n== $_func_name start =="
		while (true);
		println "== $_func_name end ==\n"
	}
	
	@Test(groups="G1")
	public void method1() {
		def _func_name ="method1"
		println "\n== $_func_name start =="
		println "This is method 1"
		println "== $_func_name end ==\n"
	}

	@Test(groups="G1",dependsOnMethods=["method1"])
	public void method2() {
		def _func_name ="method2"
		println "\n== $_func_name start =="
		println "This is method 2"
		println "== $_func_name end ==\n"
	}

	//skip test
	@Test(groups="G1",enabled=false)
	public void divisionWithException() {
		println "Method is not ready yet"
	}
}
 
 
class Dept {
	def val_a
	def val_b
}
 
class DeptDao{
	List<Dept> listAllDept(){
		[
			new Dept(val_a:100,val_b:-100),
			new Dept(val_a:50,val_b:-50),
			new Dept(val_a:"xyz",val_b:"zyx")
		]
	}
}
 
class DeptIterator implements Iterator {
	int index =0;
	DeptDao deptDao = new DeptDao()
	 
	def list;
	long list_size = 0;
	public DeptIterator(){
		list = deptDao.listAllDept()
		list_size = list.size();
	}
 
	public boolean hasNext() {
		println "==[func] hasNext<$index> start =="
		if (index < list_size)return true;
		return false;
	}
 
	public Object[] next() {
		println "==[func] next<$index> start =="
		Dept data = list.get(index)
		println "data=${data.dump()}"
		index++;
		return [data] as Object[];
	}
	
	public void remove() {
		println "==[func] remove start =="
		throw new UnsupportedOperationException();
	}
}
 
 
//Iterating DataProvider Test
class StorerIntegrationTest2 {
	private storer
	
	@BeforeClass
	def setUp() {
		storer = new Storer()
	}
	 
	private checkPersistAndReverse(value, reverseValue) {
		println "[func]checkPersistAndReverse($value,$reverseValue)"
		storer.put(value)
		assert value == storer.get()
		assert reverseValue == storer.getReverse()
	}
	 
	@DataProvider(name = "dataIterator")
	public Iterator DeptIteratorData() {
		println "==[func] DeptIteratorData start =="
		return new DeptIterator()
	}
	 
	@Test(groups="G2",dataProvider = "dataIterator")
	public void shouldPersistAndReverseIterator(Dept dept) {
		def _func_name ="shouldPersistAndReverseIterator(${dept.dump()})"
		println "\n== $_func_name start =="
		checkPersistAndReverse(dept.val_a,dept.val_b)
		println "== $_func_name end ==\n"
	}
}
 
 
//Test NG Runnner
def testng = new TestNG()
//TestListenerAdapter adapter = new TestListenerAdapter()
//testng.addListener(adapter)
 
//1) only no parameter test
//testng.setTestClasses(StorerIntegrationTest)
 
//2) parameter using test
// replacing
// <parameter name="p_a" value="-9876"></parameter>
// <parameter name="p_b" value="9876></parameter>
//
XmlSuite suite = new XmlSuite()
Map<String, String> param = new HashMap<String, String>()
param.put("p_a", "-9876")
param.put("p_b", "9876")
suite.setParameters(param)
 
XmlTest test = new XmlTest(suite)
test.setXmlClasses([new XmlClass(StorerIntegrationTest),new XmlClass(StorerIntegrationTest2)])
testng.setXmlSuites([suite])
 
//[REMARKS]Grouping Test
//
//[TODO]setGroups strange actions
//testng.setGroups("G1")
//testng.setGroups("G2")
 
 
//testng.setExcludedGroups("G1")
//testng.setExcludedGroups("G2")
testng.run()
 
println "PassedTests: ${adapter.getPassedTests()}"
println "FailedTests: ${adapter.getFailedTests()}"
println "SkippedTests: ${adapter.getSkippedTests()}"