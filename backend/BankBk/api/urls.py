from django.urls import include, path

from .api_handle import api_customer, api_staff, api_account, api_branch, api_loan, api__AUTH

urlpatterns = [
    path('auth/login', api__AUTH.login),
    path('auth/logout', api__AUTH.logout),

    # Customer
    path('APICustomer/', api_customer.handle_main),
    path('APICustomer/<customer_id>', api_customer.handle_id),
    path('APICustomer/<customer_id>/CusAccount', api_customer.handle_id_cusaccount),
    path('APICustomer/<customer_id>/Loan', api_customer.handle_id_loan),

    # Staff
    path('APIStaff/', api_staff.handle_main),
    path('APIStaff/<staff_id>', api_staff.handle_id),
    path('APIStaff/<staff_id>/CusAccount', api_staff.handle_id_cusaccount),
    path('APIStaff/<staff_id>/Loan', api_staff.handle_id_loan),

    # Account
    path('APIAccount/Deposit', api_account.handle_deposit),
    path('APIAccount/Cheque', api_account.handle_cheque),
    path('APIAccount/Deposit/<deposit_id>', api_account.handle_deposit_id),
    path('APIAccount/Cheque/<cheque_id>', api_account.handle_cheque_id),

    path('APIAccount/<account_id>', api_account.handle_id),
    path('APIAccount/<account_id>/Customer', api_account.handle_id_customer),
    path('APIAccount/<account_id>/Staff', api_account.handle_id_staff),

    # Branch
    path('APIBranch/', api_branch.handle_main),
    path('APIBranch/<branch_name>', api_branch.handle_name),

    # Loan
    path('APILoan/', api_loan.handle_main),
    path('APILoan/<loan_id>', api_loan.handle_id),
    path('APILoan/<loan_id>/Pay', api_loan.handle_pay),
]