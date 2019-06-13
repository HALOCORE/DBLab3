from django.urls import include, path

from .api_handle import api_customer, api_staff

urlpatterns = [
    path('APICustomer/', api_customer.handle_main),
    path('APICustomer/(?P<id>[0-9]+)', api_customer.handle_id),
    
    path('APIStaff/', api_staff.handle_main),
    path('APIStaff/(?P<id>[0-9]+)', api_staff.handle_id),
]