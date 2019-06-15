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
        if len(rtxt) > 400:
            print("status:", resp.status_code, " content:", rtxt[:400], "...... ")
        else:
            print("status:", resp.status_code, " content:", rtxt)


###################################################################################################

test_ctl = {'Customer':True, 'Staff':True, 'Account':True, 'Branch':True, 'Loan':True}

# # Customer
# 基本
if test_ctl['Customer']:
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/"))
    # 合法查询 TODO
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/?customName=%E5%B1%B1"))
    # 参数错误查询
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/?wahaha=abc"))
    # 获取单个（存在）
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584"))
    # 获取单个（不存在）
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/123455543211111111"))
    # 删除单个（不存在）
    printresp(requests.delete("http://193.112.68.240:8000/api/v1/APICustomer/221888888888888888"))

        # 删除单个（存在）主键约束不可删
    printresp(requests.delete("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584"))
        # 创建单个（存在）重复主键不能创建
    printresp(requests.post("http://193.112.68.240:8000/api/v1/APICustomer/",
        {"customID": "221403200601286584", "customPhone": "1385110025900", "customAddress": "上海", "customName": "宋大山", 
        "relName": "钱上", "relPhone": "1735054008861", "relEmail": "centbest@hotmail.com", "relRelation": "配偶"}))

    # 更新单个
    printresp(requests.put("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584", {'field':['customPhone', 'customAddress'], 'field_value':['1331101010000', '吉林']}))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584"))
    printresp(requests.put("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584", {'field':['customPhone', 'customAddress'], 'field_value':['1385110025900', '长沙']}))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584"))

    # 测试一个Customer的Account
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584/CusAccount"))
    # 测试一个Customer的Loan
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APICustomer/221403200601286584/Loan"))



# # Staff
if test_ctl['Staff']:
    # 基本
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/"))
    # 合法查询 参数错误略
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/?bran_branchName=AHB"))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/?staffName=小牛&staffAddress=合肥"))
    
    # 获取单个（存在）（不存在略）
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/221403199010127986"))
    # 创建单个
    printresp(requests.post("http://193.112.68.240:8000/api/v1/APIStaff/", 
        {"staffID": "410400200001010000", "bran_branchName": "AHB", "startWorkDate": "2019-01-01", "staffName": "哇哈哈", "staffPhone": "1887777555555", "staffAddress": "南京"}))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/410400200001010000"))
    # 更新单个
    printresp(requests.put("http://193.112.68.240:8000/api/v1/APIStaff/410400200001010000", {'field':['staffPhone', 'startWorkDate'], 'field_value':['1776666444444', '2019-06-15']}))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/410400200001010000"))
    # 删除单个
    printresp(requests.delete("http://193.112.68.240:8000/api/v1/APIStaff/410400200001010000"))
    
    # 删除单个（约束删不掉）（不存在略）
    printresp(requests.delete("http://193.112.68.240:8000/api/v1/APIStaff/221403199010127986"))
    
    # 一个Staff的Account
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/221403199010127986/CusAccount"))
    # 一个Staff的Loan
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIStaff/221403199010127986/Loan"))



if test_ctl['Account']:
    pass
    # # Account
    # printresp(requests.get("http://193.112.68.240:8000/api/v1/APIAccount/"))


if test_ctl['Branch']:
    # Branch
    # 基本
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIBranch/"))
    # 合法查询
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIBranch/?branchName=AH"))
    # 参数错误查询
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIBranch/?wawawawa=AH"))
    # 查询某个支行
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIBranch/AAA"))
    # 删除某个支行
    printresp(requests.delete("http://193.112.68.240:8000/api/v1/APIBranch/AAA"))
    # 添加某个支行
    printresp(requests.post("http://193.112.68.240:8000/api/v1/APIBranch/", {"city":"NewYork", "branchName":"AAA"}))
    # 删除某个支行(约束删不掉)
    printresp(requests.delete("http://193.112.68.240:8000/api/v1/APIBranch/AHB"))
    # 添加某个支行(约束加不了)
    printresp(requests.post("http://193.112.68.240:8000/api/v1/APIBranch/", {"city":"Hefei", "branchName":"AHB"}))
    # 更新某个支行
    printresp(requests.put("http://193.112.68.240:8000/api/v1/APIBranch/AAA", {"field":['city'], "field_value": ['Tokyo']}))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APIBranch/AAA"))


if test_ctl['Loan']:
    # Loan  
    # 基本
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APILoan/"))
    # 合法查询（非法查询如果是值格式错误有些不报错。注意格式要正确）
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APILoan/?loanAmountgt=2000&loanAmountlt=4000"))
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APILoan/?loanDatefrom=2019-11-01&loanDateto=2020-01-01"))
    # 获取某个贷款
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APILoan/41423895546771431063"))  
    # 获取某个贷款的发放记录
    printresp(requests.get("http://193.112.68.240:8000/api/v1/APILoan/41423895546771431063/Pay"))  
    # 支付某个贷款的一部分(loan pay)
    printresp(requests.post("http://193.112.68.240:8000/api/v1/APILoan/41423895546771431063/Pay", {"loanPayDate": datetime.datetime.now(), "loanPayAmount": 100}))  
    # 删除贷款 TODO
