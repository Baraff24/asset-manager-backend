from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import STATUS_DEVICE_CHOICES, ACTIVE, GENDER_CHOICES, NONE


class Department(models.Model):
    """
    Model for storing information about a department.
    Fields:
    - name: Department's name
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    Fields:
    - username, password, email (inherited)
    - first_name: User's first name
    - last_name: User's last name
    - gender: User's gender
    - telephone: Unique phone number for the user
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default=NONE
    )
    telephone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class MaintenanceIntervention(models.Model):
    """
    Model for storing information about a maintenance intervention.
    Fields:
    - device: Device that received the maintenance intervention
    - description: Description of the maintenance intervention
    - date: Date of the maintenance intervention
    """
    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
        related_name='maintenance_interventions'
    )
    description = models.TextField()
    date_intervention = models.DateField()
    technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='maintenance_interventions',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.device} - {self.date_intervention}"


class Device(models.Model):
    """
    Model for storing information about a user's device.
    Fields:
    - user: User that owns the device
    - device_id: Unique identifier for the device
    - brand: Brand of the device
    - serial_number: Serial number of the device
    - status: Status of the device (Active, On Maintenance, Inactive)
    - purchase_date: Date of purchase of the device
    - assigned_to: User to whom the device is assigned
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True
    )
    brand = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50,
        choices=STATUS_DEVICE_CHOICES,
        default=ACTIVE
    )
    purchase_date = models.DateField()
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assigned_devices',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.brand} - {self.serial_number} - {self.status}"


class Supplier(models.Model):
    """
    Model for storing information about a supplier.
    Fields:
    - name: Name of the supplier
    - telephone: Unique phone number for the supplier
    """
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Software(models.Model):
    """
    Model for storing information about a software.
    Fields:
    - name: Name of the software
    - version: Version of the software
    - supplier: Supplier of the software
    - license_key: License key for the software
    - expire_date: Expiration date of the software
    - installed_on: List of devices on which the software is installed
    - max_installations: Maximum number of installations allowed for the software
    """
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='softwares'
    )
    license_key = models.CharField(max_length=50)
    expire_date = models.DateField()
    installed_on = models.ManyToManyField(
        Device,
        related_name='softwares',
        blank=True
    )
    max_installations = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.version}"
