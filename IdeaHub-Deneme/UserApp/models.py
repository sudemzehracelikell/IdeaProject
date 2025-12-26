from enum import Enum
from django.db import models

class Roles(models.IntegerChoices):
    ADMIN = 1, 'Admin'
    PARTICIPANT = 2, 'Partipicant'
    TEAMLEADER = 3, 'Team Leader'
    JUDGE = 4, 'Judge'

class User(models.Model):
    userName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    role = models.IntegerField(choices=Roles.choices, default=Roles.PARTICIPANT, verbose_name='User Role')

    def __str__(self):
        return self.userName
    