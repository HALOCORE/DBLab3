from django.urls import include, path

from .api_handle import api_customer, api_staff, api__AUTH

urlpatterns = [
    path('auth/login', api__AUTH.login),
    path('auth/logout', api__AUTH.logout),
    
    path('APICustomer/', api_customer.handle_main),
    path('APICustomer/1234', api_customer.handle_id),
    
    path('APIStaff/', api_staff.handle_main),
    path('APIStaff/1234', api_staff.handle_id),
]