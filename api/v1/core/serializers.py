# There are duplicate/redundant codes in this module which need to be taken care of. Some possible approaches:
# 1. Creating a new module and transfer the redundant code there
# 2. Using a "getter" methods/functions
# 3. Using dynamic Meta classes

from rest_framework.fields import empty
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    DateTimeField,
    ModelSerializer,
    PrimaryKeyRelatedField,
)

from ..authentication.models import Account
from .constants import *
from .models import Device, DeviceLog, Employee


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    employee_name = CharField(
        max_length=128,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
    )
    employee_id = CharField(
        min_length=8,
        max_length=8,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
    )
    department = ChoiceField(
        allow_blank=False,
        allow_null=False,
        required=True,
        choices=DEPARTMENTS,
    )
    company = PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        allow_null=False,
        required=True,
    )

    def __init__(self, instance=None, data=empty, **kwargs):
        if data is empty:
            current_user: Account = kwargs["context"]["request"].user
            company_field: PrimaryKeyRelatedField = self.fields["company"]
            company_field.queryset = company_field.queryset.filter(id=current_user.id)
            super().__init__(instance, **kwargs)
        else:
            super().__init__(data=data, **kwargs)


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

    device_name = CharField(
        max_length=128,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
    )
    serial_no = CharField(
        min_length=16,
        max_length=16,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
    )
    device_type = ChoiceField(
        allow_blank=False,
        allow_null=False,
        required=True,
        choices=DEVICE_TYPES,
    )
    availability = ChoiceField(
        allow_blank=False,
        allow_null=False,
        required=True,
        choices=DEVICE_AVAILABILITY,
    )
    company = PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        allow_null=False,
        required=True,
    )
    employee = PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        allow_null=True,
        required=True,
    )

    def __init__(self, instance=None, data=empty, **kwargs):
        if data is empty:
            current_user: Account = kwargs["context"]["request"].user
            company_field: PrimaryKeyRelatedField = self.fields["company"]
            company_field.queryset = company_field.queryset.filter(id=current_user.id)
            employee_field: PrimaryKeyRelatedField = self.fields["employee"]
            employee_field.queryset = employee_field.queryset.filter(
                company_id=current_user.id
            )
            super().__init__(instance, **kwargs)
        else:
            super().__init__(data=data, **kwargs)


class DeviceLogSerializer(ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = "__all__"

    log_type = ChoiceField(
        allow_blank=False,
        allow_null=False,
        required=True,
        choices=DEVICE_LOG_TYPES,
    )
    details = CharField(
        trim_whitespace=True,
        allow_blank=True,
        allow_null=False,
        required=False,
    )
    device = PrimaryKeyRelatedField(
        queryset=Device.objects.all(),
        allow_null=False,
        required=True,
    )
    employee = PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        allow_null=True,
        required=False,
    )
    company = PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        allow_null=False,
        required=True,
    )

    created_at = DateTimeField(read_only=True)

    def __init__(self, instance=None, data=empty, **kwargs):
        if data is empty:
            current_user: Account = kwargs["context"]["request"].user
            device_field: PrimaryKeyRelatedField = self.fields["device"]
            device_field.queryset = device_field.queryset.filter(
                company_id=current_user.id
            )
            employee_field: PrimaryKeyRelatedField = self.fields["employee"]
            employee_field.queryset = employee_field.queryset.filter(
                company_id=current_user.id
            )
            company_field: PrimaryKeyRelatedField = self.fields["company"]
            company_field.queryset = company_field.queryset.filter(id=current_user.id)
            super().__init__(instance, **kwargs)
        else:
            super().__init__(data=data, **kwargs)
