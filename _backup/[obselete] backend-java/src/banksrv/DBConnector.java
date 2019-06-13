package banksrv;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;


import java.sql.ResultSet;
import java.sql.ResultSetMetaData;

import banksrv.MyQueryResult;

public class DBConnector {
	private Connection conn;
	public DBConnector() {
		// TODO Auto-generated constructor stub
		System.out.println("oh my god");
		try {
	        // The newInstance() call is a work around for some broken Java implementations
		 	Class.forName("com.mysql.cj.jdbc.Driver").newInstance();
		} catch (Exception ex) {
			System.out.println("# error driver.");
        	assert(false);
        }
		 
	 	conn = null;
		 try {
		     conn = DriverManager.getConnection("jdbc:mysql://193.112.68.240:3306/BankDB?" +
		                                    "user=root&password=612089");
		     System.out.println("# DBConnector: connect succeed.");
		     
		 } catch (SQLException ex) {
		     // handle any errors
		     System.out.println("SQLException: " + ex.getMessage());
		     System.out.println("SQLState: " + ex.getSQLState());
		     System.out.println("VendorError: " + ex.getErrorCode());
		     assert(false);
		 }
	}
	
	public MyQueryResult sqlQuery(String query) {
		String prefix = "# DBConnector: sqlQuery ";
		Statement stmt = null;
		ResultSet rs = null;
		MyQueryResult result = new MyQueryResult();
	     try {
	         stmt = conn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
	         System.out.println(prefix + "[" + query + "]...");
	         rs = stmt.executeQuery(query);
	     
	         // or alternatively, if you don't know ahead of time that the query will be a SELECT...
//	         if (stmt.execute("SELECT foo FROM bar")) {
//	             rs = stmt.getResultSet();
//	         }
	         ResultSetMetaData rsmd = rs.getMetaData();   
	         int columnCount = rsmd.getColumnCount();  
	         System.out.println(prefix + "columnCount = " + columnCount);
	         System.out.print(prefix + "COLUMNS (");
	         for(int i=1; i<=columnCount; i++) {
	        	 String colname = rsmd.getColumnName(i);
	        	 result.columns.add(colname);
	        	 System.out.print(colname + " ");
	         }
	         System.out.println(")");
	         
	         result.datas = convertDatas(rs);
	         System.out.println(prefix + "read done.");
	         return result;
	         
	     }
	     catch (SQLException ex){
	         // handle any errors
	         System.out.println("SQLException: " + ex.getMessage());
	         System.out.println("SQLState: " + ex.getSQLState());
	         System.out.println("VendorError: " + ex.getErrorCode());
	         return null;
	     }
	     finally {
	         // it is a good idea to release resources in a finally{} block
	         // in reverse-order of their creation if they are no-longer needed

	         if (rs != null) {
	             try {
	                 rs.close();
	             } catch (SQLException sqlEx) { } // ignore
	             rs = null;
	         }

	         if (stmt != null) {
	             try {
	                 stmt.close();
	             } catch (SQLException sqlEx) { } // ignore
	             stmt = null;
	         }
	     }
	}
	
	private static HashMap<String, ArrayList<Object>> convertDatas(ResultSet rs) throws SQLException {
        ResultSetMetaData md = rs.getMetaData();
        int columnCount = md.getColumnCount();
        
        HashMap<String, ArrayList<Object>> datas = new HashMap<String, ArrayList<Object>>();
        for (int i = 1; i <= columnCount; i++) {
        	datas.put(md.getColumnName(i), new ArrayList<Object>());
        }
        rs.beforeFirst();
        while(rs.next()) {
            for (int i = 1; i <= columnCount; i++) {
                datas.get(md.getColumnName(i)).add(rs.getObject(i));
            }
        }
        return datas;
}
}
