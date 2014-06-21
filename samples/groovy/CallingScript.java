import javax.script.*;

public class CallingScript {
	public static void main(String[] args) {
		ScriptEngineManager manager = new ScriptEngineManager();
		ScriptEngine engine = manager.getEngineByName("groovy");
		System.out.println("Calling script from Java");
		try {
			engine.eval("println 'Hello from Groovy'");
		} catch(ScriptException ex) {
			System.out.println(ex);
		}
	}
}