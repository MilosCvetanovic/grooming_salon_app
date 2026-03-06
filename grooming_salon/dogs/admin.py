from django.contrib import admin
from grooming_salon.dogs.models import Dog, Note

# Register your models here.
#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_of_birth', 'breed', 'slug', 'user']
    ordering = ['id']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['condition']