from django.contrib import admin
from api.models import Project
from api.models import Task


# Register your models here.
admin.site.register(Project)
admin.site.register(Task)

