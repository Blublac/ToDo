from django.contrib import admin
from .models import Todo
# Register your models here.
@admin.register(Todo)

class todoadmin(admin.ModelAdmin):
    list_display=['title','body','time']
    search_fields = ['day','title']