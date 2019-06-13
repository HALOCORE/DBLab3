package banksrv;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.mysql.cj.jdbc.ha.FailoverConnectionProxy;
import com.sun.prism.shader.FillRoundRect_Color_AlphaTest_Loader;

import banksrv.DBConnector;
import banksrv.MyQueryResult;
/**
 * Servlet implementation class APIBranch
 */
@WebServlet("/APIBranch/*")
public class APIBranch extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public APIBranch() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String prefix = "# APIBranch doGet ";
		DBConnector connector = new DBConnector();
		
		String path = request.getPathInfo();
		Enumeration<String> params = request.getParameterNames();
		System.out.println(prefix + "@" + path);
		
		System.out.println(prefix + params);
		MyQueryResult result = connector.sqlQuery("select * from customer limit 20,30;");
		
		for (String key : result.columns) {
			ArrayList<Object> datalist = result.datas.get(key); 
			System.out.println("datas.get(\"" + key + "\") is :"+datalist);    
		}
		
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}

}
