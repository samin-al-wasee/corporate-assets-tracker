from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..authentication.models import Account
from .models import Device, DeviceLog, Employee
from .serializers import DeviceLogSerializer, DeviceSerializer, EmployeeSerializer


# Create your views here.
class EmployeeListCreateView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        current_user: Account = request.user
        self.queryset = self.queryset.filter(company_id=current_user.id)
        return super().list(request, *args, **kwargs)


class EmployeeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class DeviceListCreateView(ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        current_user: Account = request.user
        self.queryset = self.queryset.filter(company_id=current_user.id)
        return super().list(request, *args, **kwargs)


class DeviceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]


class DeviceLogListCreateView(ListCreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        current_user: Account = request.user
        self.queryset = self.queryset.filter(company_id=current_user.id)
        return super().list(request, *args, **kwargs)


class DeviceLogRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    permission_classes = [IsAuthenticated]
