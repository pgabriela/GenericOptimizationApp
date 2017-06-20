from django.db import models


class Topic(models.Model):
    topicName = models.CharField(max_length=100)

    def __str__(self):
        return self.topicName


class Question(models.Model):
    text = models.CharField(max_length=200)
    forTopic = models.ForeignKey(Topic, null=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=200)
    forQuestion = models.ForeignKey(Question, null=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ProjectGroup(models.Model):
    projectname = models.CharField(max_length=100)
    inTopic = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.projectname


class GroupUser(models.Model):
    groupUsername = models.ForeignKey('auth.User')
    ingroup = models.ForeignKey(ProjectGroup, null=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return "%s in %s" % (self.groupUsername, self.ingroup)


class TopicDatabase(models.Model):
    result = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.result


class Preference(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    groupUser = models.ForeignKey(GroupUser, null=True,
                                  on_delete=models.CASCADE)
    forTopicDatabase = models.ForeignKey(TopicDatabase, null=True,
                                         on_delete=models.CASCADE)


class ProjectHost(models.Model):
    forProject = models.ForeignKey(ProjectGroup, null=True,
                                   on_delete=models.CASCADE)
    host = models.ForeignKey('auth.User')

    def __str__(self):
        return "%s, host: %s" % (self.forProject, self.host)


class ProjectInvitee(models.Model):
    host = models.ForeignKey(ProjectHost, on_delete=models.CASCADE)
    invitee = models.ForeignKey('auth.User')

    def __str__(self):
        return "%s invites %s" % (self.host, self.invitee)
