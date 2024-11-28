import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .permissions import IsActiveAndVerified
from .models import (
    Department,
    User,
    MaintenanceIntervention,
    Device,
    Supplier,
    Software
)
from .serializers import (
    DepartmentSerializer,
    UserSerializer,
    MaintenanceInterventionSerializer,
    DeviceSerializer,
    SupplierSerializer,
    SoftwareSerializer
)

# Configure a logger for this module
logger = logging.getLogger(__name__)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing departments.
    Allows all authenticated users to perform CRUD operations.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsActiveAndVerified]

    def perform_create(self, serializer):
        """
        Log department creation.
        """
        department = serializer.save()
        logger.info(f"Department created: {department.name} by user {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log department update.
        """
        department = serializer.save()
        logger.info(f"Department updated: {department.name} by user {self.request.user.username}")

    def perform_destroy(self, instance):
        """
        Log department deletion.
        """
        logger.info(f"Department deleted: {instance.name} by user {self.request.user.username}")
        instance.delete()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    - Admin users can create, update, and delete users.
    - Regular authenticated users can view user information.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsActiveAndVerified]

    def get_permissions(self):
        """
        Assign permissions based on action.
        - 'create', 'update', 'partial_update', 'destroy' require admin privileges.
        - 'list', 'retrieve' require authenticated users with IsActiveAndVerified.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser, IsActiveAndVerified]
        else:
            permission_classes = [IsAuthenticated, IsActiveAndVerified]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Optionally restricts the returned users to active users only.
        Admins see all users; others see only their user.
        """
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):
        """
        Log user creation.
        """
        user = serializer.save()
        logger.info(f"User created: {user.username} by admin {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log user update.
        """
        user = serializer.save()
        logger.info(f"User updated: {user.username} by user {self.request.user.username}")

    def perform_destroy(self, instance):
        """
        Log user deactivation.
        """
        instance.is_active = False
        instance.save()
        logger.info(f"User deactivated: {instance.username} by user {self.request.user.username}")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser, IsActiveAndVerified])
    def activate(self, request, pk=None):
        """
        Custom action to activate a user.
        Only accessible by admin users.
        """
        try:
            user = self.get_object()
            user.is_active = True
            user.save()
            logger.info(f"User activated: {user.username} by admin {request.user.username}")
            return Response({'status': 'User activated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error activating user {pk}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceInterventionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing maintenance interventions.
    - Admin users can view all interventions.
    - Regular users can view only their own interventions.
    """
    queryset = MaintenanceIntervention.objects.all()
    serializer_class = MaintenanceInterventionSerializer
    permission_classes = [IsAuthenticated, IsActiveAndVerified]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MaintenanceIntervention.objects.all()
        # Regular users see only interventions where they are the technician.
        return MaintenanceIntervention.objects.filter(technician=user)

    def perform_create(self, serializer):
        """
        Assign the current user as the technician if none is provided and log the creation.
        """
        technician = serializer.validated_data.get('technician', self.request.user)
        intervention = serializer.save(technician=technician)
        logger.info(f"Maintenance Intervention created: {intervention.id} by user {self.request.user.username}")


class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing devices.
    - Admin users can view and manage all devices.
    - Regular users can view only devices assigned to them.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsActiveAndVerified]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Device.objects.all()
        # Regular users see only devices assigned to them.
        return Device.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        """
        Log device creation.
        """
        device = serializer.save()
        logger.info(f"Device created: {device.serial_number} by user {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log device update.
        """
        device = serializer.save()
        logger.info(f"Device updated: {device.serial_number} by user {self.request.user.username}")

    def perform_destroy(self, instance):
        """
        Log device deletion.
        """
        logger.info(f"Device deleted: {instance.serial_number} by user {self.request.user.username}")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser, IsActiveAndVerified])
    def assign(self, request, pk=None):
        """
        Custom action to assign a device to a user.
        Only accessible by admin users.
        """
        device = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            logger.warning(f"Assign device failed: No user_id provided by user {request.user.username}")
            return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            device.assigned_to = user
            device.save()
            logger.info(f"Device {device.serial_number} assigned to user {user.username} by admin {request.user.username}")
            return Response({'status': 'Device assigned successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.warning(f"Assign device failed: User ID {user_id} does not exist (requested by user {request.user.username})")
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing suppliers.
    Allows all authenticated users to perform CRUD operations.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsActiveAndVerified]

    def perform_create(self, serializer):
        """
        Log supplier creation.
        """
        supplier = serializer.save()
        logger.info(f"Supplier created: {supplier.name} by user {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log supplier update.
        """
        supplier = serializer.save()
        logger.info(f"Supplier updated: {supplier.name} by user {self.request.user.username}")

    def perform_destroy(self, instance):
        """
        Log supplier deletion.
        """
        logger.info(f"Supplier deleted: {instance.name} by user {self.request.user.username}")
        instance.delete()


class SoftwareViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing software.
    - Admin users can view and manage all software.
    - Regular users can view only software installed on their devices.
    """
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = [IsAuthenticated, IsActiveAndVerified]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Software.objects.all()
        # Regular users see only software installed on their devices.
        return Software.objects.filter(installed_on__assigned_to=user).distinct()

    def perform_create(self, serializer):
        """
        Log software creation.
        """
        software = serializer.save()
        logger.info(f"Software created: {software.name} by user {self.request.user.username}")

    def perform_update(self, serializer):
        """
        Log software update.
        """
        software = serializer.save()
        logger.info(f"Software updated: {software.name} by user {self.request.user.username}")

    def perform_destroy(self, instance):
        """
        Log software deletion.
        """
        logger.info(f"Software deleted: {instance.name} by user {self.request.user.username}")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser, IsActiveAndVerified])
    def install(self, request, pk=None):
        """
        Custom action to install software on a device.
        Only accessible by admin users.
        """
        software = self.get_object()
        device_id = request.data.get('device_id')
        if not device_id:
            logger.warning(f"Install software failed: No device_id provided by user {request.user.username}")
            return Response({'error': 'Device ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(pk=device_id)
            if software.installed_on.count() >= software.max_installations:
                logger.warning(f"Install software failed: Maximum installations reached for software {software.name} by user {request.user.username}")
                return Response({'error': 'Maximum number of installations reached.'},
                                status=status.HTTP_400_BAD_REQUEST)

            software.installed_on.add(device)
            logger.info(f"Software {software.name} installed on device {device.serial_number} by admin {request.user.username}")
            return Response({'status': 'Software installed on device successfully.'}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            logger.warning(f"Install software failed: Device ID {device_id} does not exist (requested by user {request.user.username})")
            return Response({'error': 'Device does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
