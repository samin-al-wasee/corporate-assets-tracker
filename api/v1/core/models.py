# The method Token.save() needs refactoring

from typing import Any

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..authentication.models import Account
from .constants import *


# Create your models here.
class Employee(models.Model):
    employee_name = models.CharField(
        _("employee name"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
    )
    employee_id = models.CharField(
        _("employee id"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=[MinLengthValidator(MODEL_CHARFIELD_MIN_LENGTH)],
    )
    department = models.CharField(
        _("department"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
        choices=DEPARTMENTS,
    )
    company = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, blank=False, null=False
    )

    class Meta:
        pass

    def __str__(self) -> str:
        return str(self.employee_name)

    def save(self, *args, **kwargs) -> Any:
        return super().save(*args, **kwargs)


class Device(models.Model):
    device_name = models.CharField(
        _("device name"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
    )
    serial_no = models.CharField(
        _("serial no."),
        max_length=SERIAL_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=[MinLengthValidator(SERIAL_LENGTH)],
    )
    device_type = models.CharField(
        _("device type"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
        choices=DEVICE_TYPES,
    )
    availability = models.CharField(
        _("device availability"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
        choices=DEVICE_AVAILABILITY,
    )
    company = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, blank=False, null=False
    )
    employee = models.ForeignKey(
        to=Employee, on_delete=models.DO_NOTHING, blank=False, null=True
    )

    def __str__(self) -> str:
        return str(self.device_name)


class DeviceLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    log_type = models.CharField(
        _("log type"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
        choices=DEVICE_LOG_TYPES,
    )
    details = models.TextField(blank=True, null=False)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(to=Employee, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(to=Account, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.log_type

    def save(self, *args, **kwargs) -> None:
        match self.log_type:
            case "ASSIGNED":
                Device.objects.filter(id=self.device_id).update(
                    availability=DEVICE_AVAILABILITY[1][0], employee=self.employee
                )
            case "SENT_FOR_MAINTENANCE":
                Device.objects.filter(id=self.device_id).update(
                    availability=DEVICE_AVAILABILITY[2][0], employee=self.employee
                )
            case "LOST":
                Device.objects.filter(id=self.device_id).update(
                    availability=DEVICE_AVAILABILITY[3][0], employee=self.employee
                )
            case _:
                Device.objects.filter(id=self.device_id).update(
                    availability=DEVICE_AVAILABILITY[0][0], employee=None
                )

        return super().save(*args, **kwargs)
