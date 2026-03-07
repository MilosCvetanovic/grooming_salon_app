from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from grooming_salon.accounts.models import Profile
from grooming_salon.accounts.forms import AppUserCreationForm, AppUserChangeForm

UserModel = get_user_model()

# Register your models here.
#-----------------------------------------------------------------------------------------------------------------------
@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser',)
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}
        )
    )

#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'picture',)

#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ('session_key', '_session_data', 'expire_date',)
    readonly_fields = ('_session_data',)

#-----------------------------------------------------------------------------------------------------------------------
