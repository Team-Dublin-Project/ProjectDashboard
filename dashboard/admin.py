from django.contrib import admin
from .models import UserFile
# Register your models here.


# Register your models here.

class UserFileAdmin(admin.ModelAdmin):
    model = UserFile
    list_display = ('name', 'file_loc', 'created')
    list_filter = ['created', 'user']
admin.site.register(UserFile, UserFileAdmin)