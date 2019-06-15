


import random

# 常量区
def sqlstr(normstr):
    return '"' + normstr + '"'

branch_cities = [sqlstr(x) for x in ['Hefei', 'Beijing', 'Shanghai']]
branch_names = [sqlstr(x) for x in ['AHB', 'BJB', 'SHB']]

unique_digits = {"x"}
def rand_digits(dglength:int, quote=True):
    global unique_digits
    dgstr = "x"
    while dgstr in unique_digits:
        digs = [str(random.randint(0, 9)) for _ in range(dglength)]
        dgstr = "".join(digs)
        assert(len(dgstr) == dglength)
    
    assert(dgstr not in unique_digits)
    unique_digits.add(dgstr)
    if quote:
        return sqlstr(dgstr)
    return dgstr

def rand_digitss(dglength:int, dg_count:int):
    dif_dgs = set()
    for i in range(dg_count):
        dif_dgs.add(rand_digits(dglength))
    return list(dif_dgs)

unique_idstr = {"x"}
def rand_idstr():
    global unique_idstr
    idstr = "x"
    while idstr in unique_idstr:
        pf1 = ['410','443','221']
        pf2 = ['621','403']
        year = str(random.randint(1980, 2010))
        month = "%02d" % random.randint(1, 12)
        day = "%02d" % random.randint(1, 28)
        suf = rand_digits(4, False)
        idstr = random.choice(pf1) + random.choice(pf2) + year + month + day + suf
    assert(idstr not in unique_idstr)
    unique_idstr.add(idstr)
    
    return sqlstr(idstr)


def rand_idstrs(idcount:int):
    dif_ids = set()
    for i in range(idcount):
        dif_ids.add(rand_idstr())
    return list(dif_ids)



def rand_address():
    cities = ['合肥', '郑州','武汉','北京','上海']
    return sqlstr(random.choice(cities))

def rand_name():
    xing = ['王', '赵', '李', '吴', '张','钱','雷','胡','温','宋']
    ming = ['清','亮','树','想','上','飞','小牛','大山','源','凯','天乐','泽','一鸣','远']
    return sqlstr(random.choice(xing) + random.choice(ming))

def rand_email():
    uname1 = ['wing','fly','kite','cent', 'bob', 'flow']
    uname2 = ['best', '0', 'ok', 's', 'er']
    comp = ['gmail', 'outlook', '163', 'hotmail']
    return sqlstr(random.choice(uname1) + random.choice(uname2) + '@' + random.choice(comp) + ".com")

def rand_phone():
    prefs = ['173', '138', '158', '188', '136']
    return sqlstr(random.choice(prefs) + rand_digits(10, quote=False))

def rand_date():
    year = ['2017', '2018', '2019', '2020']
    month = [str(x) for x in range(1, 13)]
    day = [str(x) for x in range(1, 28)]
    return sqlstr("%s-%s-%s" % (random.choice(year), random.choice(month), random.choice(day)))

def write_csv(table_name, field_names, vals):
    with open(table_name + ".csv", 'w', encoding='utf-8') as f:
        f.write(", ".join(field_names))
        f.write('\n')
        for val in vals:
            try:
                f.write(", ".join(val))
            except Exception:
                print(val)
                assert(False)
            f.write('\n')


def csv_branch():
    field_names = ['city', 'branchName']
    vals = [(city, name) for city, name in zip(branch_cities, branch_names)]
    write_csv("branch", field_names, vals)
    return field_names, vals


def csv_cusAccount(idxs:list, branchnames:list, staffids:list, types:list):
    field_names = ['accountIDX', 'bran_branchName', 'staf_staffID', 'remain', 'visitTime', 'openTime', 'accountType']
    vals = list()
    for accidx, branchName, staffId, acctype in zip(idxs, branchnames, staffids, types):
        vals.append((accidx, branchName, staffId, str(random.randint(10, 200000)), '"2019-06-12"', '"2012-12-21"', acctype))
    write_csv("cusAccount", field_names, vals)
    return field_names, vals


def csv_chequeAccount(idxs:list):
    field_names = ['cusA_accountIDX', 'neg_limit']
    sel_neg_limits = ['1000', '2000', '5000', '10000']
    vals = [(idx, str(random.choice(sel_neg_limits))) for idx in idxs]
    write_csv("chequeAccount", field_names, vals)
    return field_names, vals


def csv_depositAccount(idxs:list):
    field_names = ['cusA_accountIDX', 'currency', 'interest']
    sel_currencies = ['RMB', 'USD', 'SGD', 'HKD']
    sel_interests = ['1.11', '2.45', '3.23', '4.45', '2.23', '0.80']
    vals = [(idx, sqlstr(random.choice(sel_currencies)), random.choice(sel_interests)) for idx in idxs]
    write_csv("depositAccount", field_names, vals)
    return field_names, vals


def csv_loan(idxs:list, staffids:list):
    field_names = ['loanIDX', 'staf_staffID', 'bran_branchName', 'loanDate', 'loanAmount', 'loanStatus']
    vals = list()
    for idx, staffid in zip(idxs, staffids):
        branch_name = random.choice(branch_names)
        loan_date = rand_date()
        loan_amount = str(random.randint(1, 100) * 1000)
        vals.append([idx, staffid, branch_name, loan_date, loan_amount, "0"])
    write_csv("loan", field_names, vals)
    return field_names, vals


def csv_cus_and_cheAccount(cusids:list, idxs:list):
    field_names = ['cust_customID', 'cheq_cusA_accountIDX']
    vals = [p for p in zip(cusids, idxs)]
    write_csv("cus_and_cheAccount", field_names, vals)
    return field_names, vals


def csv_cus_and_depAccount(cusids:list, idxs:list):
    field_names = ['cust_customID', 'depo_cusA_accountIDX']
    vals = [p for p in zip(cusids, idxs)]
    write_csv("cus_and_depAccount", field_names, vals)
    return field_names, vals


def csv_cus_and_loan(cusids:list, idxs:list):
    field_names = ['cust_customID', 'loan_loanIDX']
    vals = [p for p in zip(cusids, idxs)]
    write_csv("cus_and_loan", field_names, vals)
    return field_names, vals

def csv_customer(cus_num:int):
    field_names = ["customID","customPhone" ,"customAddress" ,"customName","relName","relPhone","relEmail","relRelation"]
    vals = list()
    cus_ids = rand_idstrs(cus_num)
    for cus_id in cus_ids:
        cusPhone = rand_phone()
        cusAddress = rand_address()
        cusName = rand_name()
        relName = rand_name()
        relPhone = rand_phone()
        relEmail = rand_email()
        relRelation = sqlstr(random.choice(['父亲','母亲','哥哥','弟弟','妹妹','姐姐','配偶']))
        vals.append((cus_id, cusPhone, cusAddress, cusName,relName, relPhone, relEmail, relRelation))
    write_csv('customer', field_names, vals)
    return field_names, vals


def csv_loanPay(loan_idxs:list, loan_amounts:list):
    field_names = ['loan_loanIDX', 'loanPayDate', 'loanPayAmount']
    vals = list()
    for idx, amount in zip(loan_idxs, loan_amounts):
        cur_amount = int(amount)
        for _ in range(random.randint(0,3)):
            loan_date = rand_date()
            cur_pay = min(cur_amount, int(random.randint(1, 10) * int(amount) / 10))
            if cur_pay == 0:
                break
            cur_amount -= cur_pay
            vals.append((idx, loan_date, str(cur_pay)))
    write_csv('loanPay', field_names, vals)
    return field_names, vals


def csv_staff(staff_num:int):
    field_names = ['staffID', 'bran_branchName', 'startWorkDate', 'staffName', 'staffPhone', 'staffAddress']
    vals = list()
    sids = rand_idstrs(staff_num)
    for sid in sids:
        sbranchname = random.choice(branch_names)
        sworkdate = rand_date()
        sname = rand_name()
        sphone = rand_phone()
        saddr = rand_address()
        vals.append((sid, sbranchname, sworkdate, sname, sphone, saddr))
    write_csv('staff', field_names, vals)
    return field_names, vals


def generate_all():
    _, _ = csv_branch()
    _, staffs = csv_staff(50)
    _, customers = csv_customer(300)
    sids = [x[0] for x in staffs]
    cids = [x[0] for x in customers]
    
    cus_idxs = list()
    cus_branchnames = list()
    cus_staffids = list()
    cus_types = list()
    
    che_idxs = list()
    dep_idxs = list()

    cu_che_ids = list()
    cu_che_idxs = list()
    cu_dep_ids = list()
    cu_dep_idxs = list()

    branch_che_idxs_dict = {branch:list() for branch in branch_names}
    branch_dep_idxs_dict = {branch:list() for branch in branch_names}

    filtval1 = 5
    filtval2 = 5
    for cid in cids:
        for branch in branch_names:
            if random.randint(0, 10) < filtval1:
            
                if random.randint(0, 10) < filtval2:
                    cus_branchnames.append(branch)
                    idx = rand_digits(20)
                    cus_idxs.append(idx)
                    staffid = random.choice(sids)
                    cus_staffids.append(staffid)
                    cus_types.append('"cheque"')

                    che_idxs.append(idx)
                    cu_che_ids.append(cid)
                    cu_che_idxs.append(idx)
                    branch_che_idxs_dict[branch].append(idx)
                
                if random.randint(0, 10) < filtval2:
                    cus_branchnames.append(branch)
                    idx = rand_digits(20)
                    cus_idxs.append(idx)
                    staffid = random.choice(sids)
                    cus_staffids.append(staffid)
                    cus_types.append('"deposit"')

                    dep_idxs.append(idx)
                    cu_dep_ids.append(cid)
                    cu_dep_idxs.append(idx)
                    branch_dep_idxs_dict[branch].append(idx)
            else:
                if random.randint(0, 10) < filtval2:
                    valid_idxs = branch_che_idxs_dict[branch]
                    if len(valid_idxs) > 0:
                        idx = random.choice(valid_idxs)
                        cu_che_ids.append(cid)
                        cu_che_idxs.append(idx)
                
                if random.randint(0, 10) < filtval2:
                    valid_idxs = branch_dep_idxs_dict[branch]
                    if len(valid_idxs) > 0:
                        idx = random.choice(valid_idxs)
                        cu_dep_ids.append(cid)
                        cu_dep_idxs.append(idx)
                
    _, accounts = csv_cusAccount(cus_idxs, cus_branchnames, cus_staffids, cus_types)
    _, depAccounts = csv_depositAccount(dep_idxs)
    _, cheAccounts = csv_chequeAccount(che_idxs)
    _, cu_che_rels = csv_cus_and_cheAccount(cu_che_ids, cu_che_idxs)
    _, cu_dep_rels = csv_cus_and_depAccount(cu_dep_ids, cu_dep_idxs)


    loan_idxs = rand_digitss(20, 350)
    loan_staffs = random.choices(sids, k=len(loan_idxs))
    _, loans = csv_loan(loan_idxs, loan_staffs)
    check_loan_idxs = [x[0] for x in loans]
    loan_amounts = [x[4] for x in loans]

    assert(len(loan_amounts) == len(loan_idxs))
    for idx in loan_idxs:
        assert(idx in check_loan_idxs)

    cu_loan_ids = list()
    cu_loan_idxs = list()

    for loan_idx in loan_idxs:
        custom_count = random.randint(1, 5) # 1~5个对应用户
        custom_ids = random.sample(cids, custom_count)
        for custom_id in custom_ids:
            cu_loan_ids.append(custom_id)
            cu_loan_idxs.append(loan_idx)
        
    _, cu_loan_rels = csv_cus_and_loan(cu_loan_ids, cu_loan_idxs)

    _, loanpays = csv_loanPay(loan_idxs, loan_amounts)


if __name__ == "__main__":
    print("# 生成所有文件")
    generate_all()