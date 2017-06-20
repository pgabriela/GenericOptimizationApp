from django.contrib import admin
from .models import GroupUser, ProjectGroup, Topic, ProjectHost, ProjectInvitee


admin.site.register(GroupUser)
admin.site.register(ProjectGroup)
admin.site.register(Topic)
admin.site.register(ProjectHost)
admin.site.register(ProjectInvitee)
