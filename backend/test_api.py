import requests

def printresp(resp:requests.Response):
    if resp.status_code >= 500:
        print("# ERROR! ", resp, resp.reason)
        with open('error.html','w') as f:
            f.write(str(resp.content))
        assert(False)
    else:
        print(resp, resp.content)


# # Customer
# printresp(requests.get("http://localhost:8000/api/v1/APICustomer/"))

# # Staff
# printresp(requests.get("http://localhost:8000/api/v1/APIStaff/"))

# # Account
# printresp(requests.get("http://localhost:8000/api/v1/APIAccount/"))

# Branch
printresp(requests.get("http://localhost:8000/api/v1/APIBranch"))
printresp(requests.get("http://localhost:8000/api/v1/APIBranch?branch=AH"))

# Loan
printresp(requests.get("http://localhost:8000/api/v1/Loan/"))    
printresp(requests.get("http://localhost:8000/api/v1/Loan/2312"))  