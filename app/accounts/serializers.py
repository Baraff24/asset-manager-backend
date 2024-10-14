from rest_framework import serializers
from .models import (
    Department,
    User,
    MaintenanceIntervention,
    Device,
    Supplier,
    Software
)


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
            'device_id', 'user', 'brand', 'serial_number', 'status',
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
