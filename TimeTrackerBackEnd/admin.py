from django.contrib import admin

from .models import ProjectModel, TaskModel, FrameModel

@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'project')

@admin.register(FrameModel)
class FrameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'task', 'start', 'stop')
