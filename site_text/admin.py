from django.contrib import admin
from download import models
from .models import Text,Type

# Register your models here.
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('title','author','text_type','created_time','invisible')
    search_fields = ('title',)
    filter_horizontal = ('file',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)