import requests
import datetime

def printresp(resp:requests.Response):
    print("\n# Request:", resp.request.method, resp.request.url)
    if resp.status_code >= 500:
        print("# ERROR! ", resp, resp.reason)
        with open('error.html','w') as f:
            f.write(str(resp.content))
        assert(False)
    elif resp.status_code == 404:
        print("# 404.")
    else:
        rtxt = str(resp.content, encoding = "utf-8")
        if len(rtxt) > 500:
            print("status:", resp.status_code, " content:", rtxt[:500], "...... ")
        else:
            print("status:", resp.status_code, " content:", rtxt)


###################################################################################################

# ------------------ 测试控制 ------------------
test_ctl = {
    'Customer':False, 
    'Staff':False, 
    'DepAccount':False, 
    'CheAccount':False, 
    'Branch':False, 
    'Loan':False,
    'Statistic':False
}

# # Customer
# 基本
if test_ctl['Customer']:
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer"))
    # 合法查询(参数错误的例子略)
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer?customName=%E5%B1%B1"))
    # 获取单个（存在）
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer/221403200601286584"))
    # 获取单个（不存在） printresp(requests.get("http://localhost:8000/api/v1/APICustomer/123455543211111111"))
    # 删除单个（不存在） printresp(requests.delete("http://localhost:8000/api/v1/APICustomer/221888888888888888"))
    # 删除单个（存在）主键约束不可删 printresp(requests.delete("http://localhost:8000/api/v1/APICustomer/221403200601286584"))
    # 创建单个（存在）重复主键不能创建 printresp(requests.post("http://localhost:8000/api/v1/APICustomer",
        # {"customID": "221403200601286584", "customPhone": "1385110025900", "customAddress": "上海", "customName": "宋大山", 
        # "relName": "钱上", "relPhone": "1735054008861", "relEmail": "centbest@hotmail.com", "relRelation": "配偶"}))
    # 更新单个
    printresp(requests.put("http://localhost:8000/api/v1/APICustomer/221403200601286584", {'field':['customPhone', 'customAddress'], 'field_value':['1331101010000', '吉林']}))
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer/221403200601286584"))
    printresp(requests.put("http://localhost:8000/api/v1/APICustomer/221403200601286584", {'field':['customPhone', 'customAddress'], 'field_value':['1385110025900', '长沙']}))
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer/221403200601286584"))
    # 测试一个Customer的Account
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer/221403200504282880/CusAccount"))
    # 测试一个Customer的Loan
    printresp(requests.get("http://localhost:8000/api/v1/APICustomer/221403200601286584/Loan"))
';'


# # Staff
if test_ctl['Staff']:
    # 基本
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff"))
    # 合法查询 参数错误略
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff?bran_branchName=AHB"))
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff?staffName=小牛&staffAddress=上海"))
    
    # 获取单个（存在）（不存在略）
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff/443403199605063164"))
    # 创建单个
    printresp(requests.post("http://localhost:8000/api/v1/APIStaff", 
        {"staffID": "410400200001010000", "bran_branchName": "AHB", "startWorkDate": "2019-01-01", "staffName": "哇哈哈", "staffPhone": "1887777555555", "staffAddress": "南京"}))
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff/410400200001010000"))
    # 更新单个
    printresp(requests.put("http://localhost:8000/api/v1/APIStaff/410400200001010000", {'field':['staffPhone', 'startWorkDate'], 'field_value':['1776666444444', '2019-06-15']}))
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff/410400200001010000"))
    # 删除单个
    printresp(requests.delete("http://localhost:8000/api/v1/APIStaff/410400200001010000"))
    
    # 删除单个（约束删不掉）（不存在略）
    printresp(requests.delete("http://localhost:8000/api/v1/APIStaff/443403199605063164"))
    
    # 一个Staff的Account
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff/443403199605063164/CusAccount"))
    # 一个Staff的Loan
    printresp(requests.get("http://localhost:8000/api/v1/APIStaff/443403199605063164/Loan"))



if test_ctl['DepAccount']:
    # DepAccount
    # 储蓄基本
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Deposit"))
    # 储蓄查询
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Deposit?currency=RMB"))
    # 单个储蓄账户
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Deposit/00403386247866740608"))
    # 单个储蓄账户的客户
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Deposit/00403386247866740608/Customer"))
    # 储蓄创建
    printresp(requests.post("http://localhost:8000/api/v1/APIAccount/Deposit",
        {
            "staf_staffID": "221403198701122751", # AHB银行
            "cust_customID": "221403199203056861",
            "accountIDX": "00000088888866666699",
            "remain": 10000.0,
            "currency": "RMB",
            "interest": "3.230"
        }))
    # 给这个账户添加其它用户
    printresp(requests.post("http://localhost:8000/api/v1/APIAccount/Deposit/00000088888866666699",{
        "cust_customID": "410403198512235470"}))
    # 这个客户应该多了一个账户 printresp(requests.get("http://localhost:8000/api/v1/APICustomer/410403198512235470/CusAccount"))
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Deposit/00000088888866666699"))
    # 储蓄更改（余额变动为-10000(花完)，否则下一步不能删除）
    printresp(requests.put("http://localhost:8000/api/v1/APIAccount/Deposit/00000088888866666699", {
        'field': ['cust_customID', 'remain_change'],
        'field_value':['221403199203056861', -10000]
    }))
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Deposit/00000088888866666699"))
    # 储蓄删除
    printresp(requests.delete("http://localhost:8000/api/v1/APIAccount/Deposit/00000088888866666699"))
    # 这个客户应该少一个账户 printresp(requests.get("http://localhost:8000/api/v1/APICustomer/410403198512235470/CusAccount"))



if test_ctl['CheAccount']:
    # CheAccount
    # 支票基本
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Cheque"))
    # 支票查询
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Cheque?remainlt=20000&neg_limitgt=3000"))
    # 单个支票账户
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Cheque/00278883948040893941"))
    # 单个支票账户的客户
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Cheque/00278883948040893941/Customer"))
    # 支票创建
    printresp(requests.post("http://localhost:8000/api/v1/APIAccount/Cheque",
        {
            "staf_staffID": "221403199112040167", # BJB银行
            "cust_customID": "221403200504282880", 
            "accountIDX": "11111188888866666600",
            "remain": 10000.0
        }))
    # 给这个支票账户添加其它用户(添加后410403199604140379多一个账户)
    printresp(requests.post("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600",{
        "cust_customID": "410403199604140379"}))
    # 支票修改(改为0)
    printresp(requests.put("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600", {
        'field': ['cust_customID', 'remain_change'],
        'field_value':['221403200504282880', -11000]
    }))
    printresp(requests.put("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600", {
        'field': ['cust_customID', 'remain_change'],
        'field_value':['221403200504282880', -1000]
    }))
    # 这个会花超，失败。
    # printresp(requests.put("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600", {
    #     'field': ['cust_customID', 'remain_change'],
    #     'field_value':['221403200504282880', -1000]}))
    printresp(requests.get("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600"))
    printresp(requests.put("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600", {
        'field': ['cust_customID', 'remain_change'],
        'field_value':['221403200504282880', +2000]
    }))
    # 支票删除（余额0才能删）（删除后410403199604140379少一个账户）
    printresp(requests.delete("http://localhost:8000/api/v1/APIAccount/Cheque/11111188888866666600"))


if test_ctl['Branch']:
    # Branch
    # 基本
    printresp(requests.get("http://localhost:8000/api/v1/APIBranch"))
    # 合法查询
    printresp(requests.get("http://localhost:8000/api/v1/APIBranch?branchName=AH"))
    # 查询某个支行
    printresp(requests.get("http://localhost:8000/api/v1/APIBranch/AHB"))
    # 添加某个支行
    printresp(requests.post("http://localhost:8000/api/v1/APIBranch", {"city":"NewYork", "branchName":"AAA"}))
    # 删除某个支行(约束删不掉, 略)  printresp(requests.delete("http://localhost:8000/api/v1/APIBranch/AHB"))
    # 添加某个支行(约束加不了, 略)  printresp(requests.post("http://localhost:8000/api/v1/APIBranch", {"city":"Hefei", "branchName":"AHB"}))
    # 更新某个支行
    printresp(requests.put("http://localhost:8000/api/v1/APIBranch/AAA", {"field":['city'], "field_value": ['Tokyo']}))
    printresp(requests.get("http://localhost:8000/api/v1/APIBranch/AAA"))
    # 删除某个支行
    printresp(requests.delete("http://localhost:8000/api/v1/APIBranch/AAA"))


if test_ctl['Loan']:
    # Loan  
    # 基本
    printresp(requests.get("http://localhost:8000/api/v1/APILoan"))
    # 合法查询（非法查询如果是值格式错误有些不报错。注意格式要正确）
    printresp(requests.get("http://localhost:8000/api/v1/APILoan?loanAmountgt=2000&loanAmountlt=4000"))
    printresp(requests.get("http://localhost:8000/api/v1/APILoan?loanDatefrom=2019-11-01&loanDateto=2020-01-01"))
    # 获取某个贷款
    printresp(requests.get("http://localhost:8000/api/v1/APILoan/41423895546771431063"))  
    # 获取某个贷款的用户
    printresp(requests.get("http://localhost:8000/api/v1/APILoan/41423895546771431063/Customer"))  
    # 获取某个贷款的发放记录
    printresp(requests.get("http://localhost:8000/api/v1/APILoan/41423895546771431063/Pay"))  
    # 创建贷款
    printresp(requests.post("http://localhost:8000/api/v1/APILoan", 
        {
            "loanIDX": "44449999000022221111",
            "staf_staffID": "443403199605063164",
            "bran_branchName": "SHB",
            "loanDate": "2019-06-16 00:00:00",
            "loanAmount": 55000.0
        }
    ))
    # 获取某个贷款
    printresp(requests.get("http://localhost:8000/api/v1/APILoan/44449999000022221111"))  
    # 给该贷款账户添加客户
    printresp(requests.post("http://localhost:8000/api/v1/APILoan/44449999000022221111", {
        "cust_customID": "410403199312140490"}))
    # 支付贷款（支付2次，总共达到总额）
        # 第一次支付
    printresp(requests.post("http://localhost:8000/api/v1/APILoan/44449999000022221111/Pay", {"loanPayDate": datetime.datetime.now(), "loanPayAmount": 22000}))  
    printresp(requests.get("http://localhost:8000/api/v1/APILoan/44449999000022221111/Pay"))  
        # 失败的删除
    # printresp(requests.delete("http://localhost:8000/api/v1/APILoan/44449999000022221111"))
        # 第二次支付
    printresp(requests.post("http://localhost:8000/api/v1/APILoan/44449999000022221111/Pay", {"loanPayDate": datetime.datetime.now(), "loanPayAmount": 33000}))  
    printresp(requests.get("http://localhost:8000/api/v1/APILoan/44449999000022221111/Pay"))  
        # 成功删除贷款
    printresp(requests.delete("http://localhost:8000/api/v1/APILoan/44449999000022221111"))


if test_ctl['Statistic']:
    # 按照三类账户统计全部
    printresp(requests.get("http://localhost:8000/api/v1/APIStatistic/Loan"))
    printresp(requests.get("http://localhost:8000/api/v1/APIStatistic/Deposit"))
    printresp(requests.get("http://localhost:8000/api/v1/APIStatistic/Cheque"))
    # 按照三类账户,统计起止时间
    printresp(requests.get("http://localhost:8000/api/v1/APIStatistic/Loan?loanDatefrom=2012-01-01&loanDateto=2020-12-01"))
    printresp(requests.get("http://localhost:8000/api/v1/APIStatistic/Deposit?openTimefrom=2012-01-01&openTimeto=2020-12-01"))
    printresp(requests.get("http://localhost:8000/api/v1/APIStatistic/Cheque?openTimefrom=2012-01-01&openTimeto=2020-12-01"))
    