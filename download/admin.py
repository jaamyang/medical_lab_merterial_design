from django.contrib import admin
from .models import Download_file

# Register your models here.
@admin.register(Download_file)
class Download_fileAdmin(admin.ModelAdmin):
    list_display = ('id','file_name','upload_date',)
    list_display_links = ('file_name',)
    filter_horizontal = ('download_permission',)