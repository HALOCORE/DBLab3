from . import db_connect
"""查询"""
#执行查询语句，返回所有表头和所有数据
def query_all(sql:str, parameter=()):
    try:
        cursor = db_connect.connection.cursor()
        if len(parameter)==0:
            cursor.execute(sql)
        else:
            cursor.execute(sql,parameter)
        all_data = cursor.fetchall()
        col = cursor.description
        metadata = [col[i][0] for i in range(len(col))]
    finally:
        cursor.close()
    return metadata, all_data

#查询整个表
def query_table(table_name):
    sql = 'SELECT * FROM '+table_name
    metadata, data = query_all(sql)
    return metadata, data

#精确查询
def query_specify(select_columns,from_table,where_dict):
    sql = "SELECT "
    column_num = len(select_columns)
    if column_num == 0:
        sql += "*"
    else:
        sql += ", ".join(select_columns)
    sql += (" FROM " + from_table + " WHERE ")
    where = [key+"=%s" for key in where_dict.keys()]
    sql += " and ".join(where)
    #print(sql)
    parameter = tuple(where_dict.values())
    #print(parameter)
    metadata, data = query_all(sql,parameter)
    return metadata, data

"""增删改的SQL执行"""
def modify_table(sql,parameter):
    try:
        cursor = db_connect.connection.cursor()
        if len(parameter)==0:
            cursor.execute(sql)
        else:
            cursor.execute(sql,parameter)
        db_connect.connection.commit()
    finally:
        cursor.close()
    return

"""插入"""
def insert_one(table_name,data,debug=False):
    if debug:
        print(data)
    head = "INSERT INTO "+table_name
    entry = ", ".join(list(data.keys()))
    para = ["%s"]*len(data)
    values = ", ".join(para)
    sql = head + " (" +entry+ ") VALUES (" +values+ ")"
    parameter = tuple(data.values())
    if debug:
        print(sql)
        print(parameter)
    modify_table(sql,parameter)
    return



# if __name__ == '__main__':
#     #插入语句测试
#     table = "branch"
#     data = {"city":"","branchName":"BBB"}
#     insert_one(table,data,True)
#     #查询语句测试
#     select_columns = ["city","name"]
#     from_table = "branch"
#     where_dict = {'x': 1, 'y': 2, 'z': 3}
#     query_specify(select_columns,from_table,where_dict)
