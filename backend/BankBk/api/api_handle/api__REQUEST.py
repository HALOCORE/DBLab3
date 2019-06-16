from . import db_connect

from datetime import datetime
    


"""执行无返回值的存储过程"""
def call_procedure(proc_name, params:list):
    str_params = list()
    for param in params:
        if isinstance(param, str):
            str_params.append('"' + param + '"')
        elif isinstance(param, datetime):
            str_params.append('"' + str(datetime) + '"')
        else:
            str_params.append(str(param))
    str_param = ', '.join(str_params)
    cursor = db_connect.connection.cursor()
    command = "call %s(%s)" % (proc_name, str_param)
    print("# call_procedure. ", command)
    cursor.execute(command)
    cursor.close()


"""查询"""
#执行查询语句，返回所有表头和所有数据
def query_all(sql:str, parameter=()):
    try:
        cursor = db_connect.connection.cursor()
        print("# query_all:", sql, ", params:", parameter)
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
# def query_table(table_name):
#     sql = 'SELECT * FROM '+table_name
#     metadata, data = query_all(sql)
#     return metadata, data


#单个获取
def specify_get(select_columns, from_table, key_name, key_value):
    """key_name key_value 是主键名称和值"""
    sql = "SELECT "
    column_num = len(select_columns)
    if column_num == 0:
        sql += "*"
    else:
        sql += ", ".join(select_columns)
    sql += " FROM " + from_table + " WHERE " + key_name + " = %s"
    metadata, data = query_all(sql,(key_value,))
    return metadata, data


# 单个删除
def specify_delete(from_table, key_name, key_value):
    """key_name key_value 是主键名称和值"""
    sql = "SELECT " + key_name + " FROM " + from_table + " WHERE " + key_name + " = %s"
    _, data = query_all(sql,(key_value,))
    if len(data) != 1:
        raise db_connect.MyDeleteError("table: %s, key:%s, keyval:%s" % (from_table, key_name, key_value))
    sql = "DELETE FROM " + from_table + " WHERE " + key_name + " = %s"
    modify_table(sql, (key_value,))



# 单个更新(表无连接) 目前只更新字符串字段。需要引入列类型检查！# TODO: 非字符串字段更新
def specify_update(from_table, field:list,field_value:list, key, value):
    """key_name key_value 是主键名称和值"""
    if field is None or field_value is None:
        print("specify_update ERROR: ", field, field_value)
        raise db_connect.MyUpdateError("field or field_value is None.")
    if len(field) != len(field_value):
        print("specify_update ERROR: ", field, field_value)
        raise db_connect.MyUpdateError("field and field_value have different length.")
    head = "UPDATE "+from_table+" SET "
    new_data = ["%s = '%s'" % (field[i], field_value[i]) for i in range(len(field))]
    where = " WHERE " + key + " = %s "
    sql = head + ", ".join(new_data) + where
    print("# specify update. ", sql)
    modify_table(sql, (value,))



# 生成where子句
def gen_where(query_dict):
    wheres = list()
    for key in query_dict:
        if key.endswith("lt"):
            wheres.append(key[:-2] + " < " + query_dict[key] + " ")
        elif key.endswith("gt"):
            wheres.append(key[:-2] + " > " + query_dict[key] + " ")
        elif key.endswith("from"):
            wheres.append(key[:-4] + " > '" + query_dict[key] + "' ")
        elif key.endswith("to"):
            wheres.append(key[:-2] + " < '" + query_dict[key] + "' ")
        else:
            wheres.append(key + " like " + "'%" + query_dict[key] + "%'" + " ")
    where = " and ".join(wheres)
    print("# gen_where: " + where)
    return where


# 模糊查询
def query_fuzz(select_columns, from_table, query_dict):
    sql = "SELECT "
    column_num = len(select_columns)
    if column_num == 0:
        sql += "*"
    else:
        sql += ", ".join(select_columns)
    where = gen_where(query_dict)
    if where != "":
        sql += " FROM " + from_table + " WHERE " + where
    else:
        sql += " FROM " + from_table
    metadata, data = query_all(sql,())
    return metadata, data


# 模糊查询(连接) 未使用
def query_fuzz_join(select_columns, tab1, key1, tab2, key2, query_dict):
    sql = "SELECT "
    column_num = len(select_columns)
    if column_num == 0:
        sql += "*"
    else:
        sql += ", ".join(select_columns)
    where = "%s = %s " % (key1, key2) + gen_where(query_dict)
    sql += " FROM " + tab1 + ", " + tab2 + " WHERE " + where
    metadata, data = query_all(sql,())
    return metadata, data


"""增删改的SQL执行"""
def modify_table(sql,parameter):
    cursor = db_connect.connection.cursor()
    if len(parameter)==0:
        cursor.execute(sql)
    else:
        cursor.execute(sql,parameter)
    db_connect.connection.commit()
    cursor.close()

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

"""统计的SQL执行，返回字典"""
def excu_statistics(sql):
    cursor = db_connect.connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    colmon = cursor.description#列的元组
    title = [colmon[i][0] for i in range(len(colmon))]
    cursor.close()
    return title, result

"""求和"""
def calc_sum(column,table_name,sum_where):
    sql = "SELECT bran_branchName,SUM("+column+") AS sum_"+column+" FROM "
    +table_name+" WHERE "+sum_where+" GROUP BY bran_branchName"
    metadata, data = excu_statistics(sql)
    return metadata, data

def calc_currency(sum_where):
    sql = "SELECT a.bran_branchName, b.currency SUM('remain') AS sum_remain \
    FROM cusAccount a,depositAccount b WHERE "+sum_where+" GROUP BY a.bran_branchName, b.currency"
    metadata, data = excu_statistics(sql)
    return metadata, data

def calc_count(table_name,count_where):
    sql = "SELECT bran_branchName,COUNT(*) AS count_"+table_name+" FROM "
    +table_name+" WHERE "+count_where+" GROUP BY bran_branchName"
    metadata, data = excu_statistics(sql)
    return metadata, data