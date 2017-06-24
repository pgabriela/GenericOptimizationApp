from django.contrib import admin
from .models import GroupUser, ProjectGroup, Topic, ProjectHost,\
    ProjectInvitee, Question, Answer, TopicDatabase, Preference


admin.site.register(GroupUser)
admin.site.register(ProjectGroup)
admin.site.register(Topic)
admin.site.register(ProjectHost)
admin.site.register(ProjectInvitee)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TopicDatabase)
admin.site.register(Preference)
