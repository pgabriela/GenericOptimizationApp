from django.db import models


class LoginData(models.Model):
    Username = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)

    def __str__(self):
        return self.Username
