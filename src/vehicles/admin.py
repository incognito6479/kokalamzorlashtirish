from django.contrib import admin

from vehicles.models import Vehicle, VehicleTypes


class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "manufactured_date",
        "registration_plate",
        "GPS_status",
    ]


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleTypes, VehicleTypeAdmin)
