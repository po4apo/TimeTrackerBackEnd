from django.contrib.auth.models import User
from django.db import models


class ProjectModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class TaskModel(models.Model):
    STATUS = [
        ('Active', 0),
        ('Done', 1),
        ('Hide', 2)
    ]

    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=6,
                              choices=STATUS,
                              default='Active', )

    def __str__(self):
        return str(self.name)


class FrameModel(models.Model):
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE)
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'task_name: {self.task} \nstart_time:{self.start} \nstop_time:{self.stop}'
