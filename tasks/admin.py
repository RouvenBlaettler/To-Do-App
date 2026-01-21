from django.contrib import admin

from .models import NormalTask, ContinuousTask

# Register your models here.
admin.site.register(NormalTask)
admin.site.register(ContinuousTask)