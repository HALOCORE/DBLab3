from . import db_connect

def query_all():
    try:
        cursor = db_connect.connection.cursor()
        cursor.execute('SELECT * FROM branch')
        all_branch = cursor.fetchall()
        col = cursor.description
        metadata = [col[i][0] for i in range(len(col))]
    finally:
        cursor.close()
    