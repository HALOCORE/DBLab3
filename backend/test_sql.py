import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='193.112.68.240',
                             port=3306,
                             user='root',
                             password='612089',
                             db='BankDB',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    cursor = connection.cursor()
    
    # # 执行查询 SQL
    # cursor.execute('SELECT * FROM branch')
    # # 获取单条数据
    # result = cursor.fetchall()
    # colmon = cursor.description#列的元组
    # title = [colmon[i][0] for i in range(len(colmon))]
    # cursor.close()
    # print(result)
    # print(colmon)
    # print(title)


    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO branch (city, branchName) VALUES (%s, %s)"
        cursor.execute(sql, ('', 'AAA'))
        
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    # with connection.cursor() as cursor:
    #     # Read a single record
    #     sql = "SELECT city FROM branch WHERE branchName='AHB'"
    #     cursor.execute(sql)
    #     #cursor.execute(sql, ('AHB',))
    #     result = cursor.fetchall()
    #     print(result)
finally:
    connection.close()
