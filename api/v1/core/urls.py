from django.urls import path

from .views import (
    DeviceListCreateView,
    DeviceLogListCreateView,
    DeviceLogRetrieveUpdateDestroyView,
    DeviceRetrieveUpdateDestroyView,
    EmployeeListCreateView,
    EmployeeRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "employees/",
        EmployeeListCreateView.as_view(),
        name="employee_list_or_create",
    ),
    path(
        "employees/<int:pk>",
        EmployeeRetrieveUpdateDestroyView.as_view(),
        name="employee_details_update_or_delete",
    ),
    path("devices/", DeviceListCreateView.as_view(), name="device_list_or_create"),
    path(
        "devices/<int:pk>",
        DeviceRetrieveUpdateDestroyView.as_view(),
        name="device_details_update_or_delete",
    ),
    path(
        "devices/logs/",
        DeviceLogListCreateView.as_view(),
        name="device_log_list_or_create",
    ),
    path(
        "devices/logs/<int:pk>",
        DeviceLogRetrieveUpdateDestroyView.as_view(),
        name="device_log_details_update_or_delete",
    ),
]
