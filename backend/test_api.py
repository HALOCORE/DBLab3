import requests

def printresp(resp:requests.Response):
    if resp.status_code >= 500:
        print("# ERROR! ", resp, resp.reason)
        with open('error.html','w') as f:
            f.write(str(resp.content))
        assert(False)
    elif resp.status_code == 404:
        print("# 404.")
    else:
        print(resp, resp.content)


# # Customer
# printresp(requests.get("http://localhost:8000/api/v1/APICustomer/"))

# # Staff
# printresp(requests.get("http://localhost:8000/api/v1/APIStaff/"))

# # Account
# printresp(requests.get("http://localhost:8000/api/v1/APIAccount/"))

# Branch
# printresp(requests.get("http://localhost:8000/api/v1/APIBranch/"))
# printresp(requests.get("http://localhost:8000/api/v1/APIBranch/?branch=AH"))
# printresp(requests.get("http://localhost:8000/api/v1/APIBranch/AAA"))
# printresp(requests.delete("http://localhost:8000/api/v1/APIBranch/AAA"))
# printresp(requests.post("http://localhost:8000/api/v1/APIBranch/", {"city":"Henan", "name":"河南分行"}))
printresp(requests.put("http://localhost:8000/api/v1/APIBranch/AHB", {"field":['city'], "field_value": ['RRRRRR']}))

# Loan
# printresp(requests.get("http://localhost:8000/api/v1/Loan/"))    
# printresp(requests.get("http://localhost:8000/api/v1/Loan/2312"))  