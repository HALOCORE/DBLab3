import os
import csv

insert_order = ['branch', 'staff', 'customer', 'cusAccount', 'depositAccount', 'cus_and_depAccount', 'chequeAccount', 'cus_and_cheAccount', 'loan', 'cus_and_loan', 'loanPay']

def read_csv(tablename):
    """
    读取csv文件，返回head和rows
    """
    txt = open('./csvdata/%s.csv' % tablename, 'r', encoding='utf-8')
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
    assert(len(list(table_dict.keys())) == len(insert_order))
    for key in table_dict:
        assert key in insert_order
    return table_dict


def gen_insert(table_name, fields:list, valuess:list):
    code = "insert into %s (%s) values\n" % (table_name, ", ".join(fields))
    val_codes = ",\n".join(["    (%s)" % ", ".join(vals) for vals in valuess])
    return code + val_codes + ";"


def gen_truncate(table_name):
    return "truncate table %s;" % (table_name)

def gen_truncate_all_tables():
    truncate_codes = list()
    truncate_codes.append('SET FOREIGN_KEY_CHECKS = 0;')
    for table_name in reversed(insert_order):
        truncate_codes.append(gen_truncate(table_name))
    truncate_codes.append('SET FOREIGN_KEY_CHECKS = 1;')
    return '\n'.join(truncate_codes)


def gen_delete(table_name):
    return "delete from %s;" % (table_name)

def gen_delete_all_tables():
    truncate_codes = list()
    for table_name in reversed(insert_order):
        truncate_codes.append(gen_delete(table_name))
    truncate_codes.append('commit;')
    return '\n'.join(truncate_codes)



def gen_all_insert_codes():
    tabs = read_all_tables()
    insert_codes = list()
    for table_name in insert_order:
        insert_codes.append(gen_insert(table_name, tabs[table_name][0], tabs[table_name][1]))
    all_code = '\n\n'.join(insert_codes)
    return all_code


if __name__ == '__main__':
    all_code = 'use BankDB;'
    all_code += gen_truncate_all_tables() 
    all_code += "\n\n----------------------------------------------------------------\n\n"
    all_code += gen_all_insert_codes()
    with open("insert.sql", 'w', encoding='utf-8') as f:
        f.write(all_code)
    print("# SQL 数据插入代码写入完成")