from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .constants import GENDER_CHOICES, NONE
from .models import (
    Department,
    User,
    MaintenanceIntervention,
    Device,
    Supplier,
    Software
)


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False, default=NONE)
    telephone = serializers.CharField(max_length=20, required=False)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True
    )

    def validate_telephone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Il telefono deve contenere solo cifre.")
        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['gender'] = self.validated_data.get('gender', 'N')
        data['telephone'] = self.validated_data.get('telephone', '')
        data['department'] = self.validated_data.get('department', None)
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.gender = self.cleaned_data.get('gender', 'N')
        user.telephone = self.cleaned_data.get('telephone', '')
        user.department = self.cleaned_data.get('department', None)
        user.save()
        return user


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'first_name', 'last_name',
            'gender', 'telephone', 'department', 'department_id'
        ]


class MaintenanceInterventionSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    technician = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True), allow_null=True, required=False
    )

    class Meta:
        model = MaintenanceIntervention
        fields = ['id', 'device', 'description', 'date_intervention', 'technician']


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )
    maintenance_interventions = MaintenanceInterventionSerializer(many=True, read_only=True)
    softwares = serializers.PrimaryKeyRelatedField(many=True, queryset=Software.objects.all(), required=False)

    class Meta:
        model = Device
        fields = [
            'device_id', 'user', 'brand', 'name', 'serial_number', 'status',
            'purchase_date', 'assigned_to', 'maintenance_interventions', 'softwares'
        ]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'telephone']


class SoftwareSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    installed_on = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Device.objects.all(),
        required=False
    )

    class Meta:
        model = Software
        fields = [
            'id', 'name', 'version', 'supplier', 'license_key',
            'expire_date', 'installed_on', 'max_installations'
        ]
