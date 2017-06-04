from django.db import models


class UsersProject(models.Model):
    a = 5


class ProjectGroup(models.Model):
    projectname = models.CharField(max_length=100)
    members = models.ManyToManyField(UsersProject)
