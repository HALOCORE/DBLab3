package banksrv;

import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;


public class MyQueryResult {
	ArrayList<String> columns;
	HashMap<String, ArrayList<Object>> datas;

	MyQueryResult(){
		columns = new ArrayList<>();
		datas = new HashMap<String, ArrayList<Object>>();
	}
	
	public int rowCount() {
		return datas.get(columns.get(0)).size();
	}
	
	public int columnCount() {
		return columns.size();
	}
	
	public String jsonData() {
		JSONArray dataArr = new JSONArray();
		for(int i = 0; i < rowCount(); i++) {
			JSONObject dataRow = new JSONObject();
			for(String key : columns) {
				dataRow.append(key, datas.get(key).get(i));
			}
			dataArr.put(dataRow);
		}
		return dataArr.toString(2);
	}
}
