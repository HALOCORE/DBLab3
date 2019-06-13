package banksrv;

import java.util.ArrayList;
import java.util.HashMap;

public class MyQueryResult {
	ArrayList<String> columns;
	HashMap<String, ArrayList<Object>> datas;
	
	MyQueryResult(){
		columns = new ArrayList<>();
		datas = new HashMap<String, ArrayList<Object>>();
	}
}
