import os
import csv

def read_csv(tablename):
    """
    读取csv文件，返回head和rows
    """
    txt = open('./csvdata/%s.csv' % tablename, 'r')
    all_content = str(txt.read()).strip()
    # print(all_content)
    lines = [x.strip() for x in all_content.split('\n')]
    head = [x.strip() for x in lines[0].split(',')]
    print(head)
    rows = [(x.strip() for x in line.split(',')) for line in lines[1:]]
    txt.close()
    return (head, rows)
    

def read_all_tables():
    table_dict = dict()
    for file in os.listdir('./csvdata'):
        if file.endswith('.csv'):
            table_name = file.split('.')[0]
            table_dict[table_name] = read_csv(table_name)
    return table_dict


def gen_insert(table_name, fields:list, valuess:list):
    code = "insert into %s (%s) values\n" % (table_name, ", ".join(fields))
    val_codes = ",\n".join(["    (%s)" % ", ".join(vals) for vals in valuess])
    return code + val_codes + ";"


def gen_delete(table_name, pkey, val):
    return "delete from %s where %s = \"%s\";" % (table_name, pkey, val)


def gen_all_insert_codes():
    tabs = read_all_tables()
    insert_codes = list()
    for table_name in tabs:
        insert_codes.append(gen_insert(table_name, tabs[table_name][0], tabs[table_name][1]))
    all_code = '\n\n'.join(insert_codes)
    return all_code


if __name__ == '__main__':
    all_code = gen_all_insert_codes()
    with open("insert.sql", 'w') as f:
        f.write(all_code)
    print("# SQL 数据插入代码写入完成")