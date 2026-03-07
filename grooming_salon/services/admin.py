from django.contrib import admin
from grooming_salon.services.models import Groomer, Service, Appointment


# Register your models here.
#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Groomer)
class GroomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture',)
    search_fields = ('name',)
    ordering = ('id',)

#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture',)
    search_fields = ('name',)
    ordering = ('id',)

#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_services', 'date', 'time', 'groomer', 'dog', 'created_at', 'status',)
    search_fields = ('id',)
    ordering = ('status', 'date', 'time',)

    # Zbog ManyToMany relacije, moramo napraviti metodu koja ce nam dovuci sve servise
    def get_services(self, obj):
        return ', '.join([service.name for service in obj.services.all()])

    # Postavljamo naziv kolone u Django Adminu
    get_services.short_description = 'Services'

#-----------------------------------------------------------------------------------------------------------------------
