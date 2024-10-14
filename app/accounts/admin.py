from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Department,
    User,
    MaintenanceIntervention,
    Device,
    Supplier,
    Software
)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom

            # group heading of your choice;
            # set to None for a blank space instead of a header
            'Other information of the User',
            {
                'fields': (
                    'gender',
                    'telephone',
                    'department'
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(MaintenanceIntervention)
admin.site.register(Device)
admin.site.register(Supplier)
admin.site.register(Software)
