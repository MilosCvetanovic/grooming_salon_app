from django.contrib import admin
from grooming_salon.reviews.models import Review

# Register your models here.
#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','appointment', 'rating', 'description', 'picture', 'created_at', 'get_user',)
    search_fields = ('id',)
    ordering = ('created_at',)

    @admin.display(description='User')
    def get_user(self, obj):
        return obj.appointment.user

#-----------------------------------------------------------------------------------------------------------------------
