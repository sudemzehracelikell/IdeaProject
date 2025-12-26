from django.db import models


class TeamMember(models.Model):
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.userName

class Team(models.Model):
    teamName = models.CharField(max_length=100)
    teamMember = models.ManyToManyField(TeamMember)

    def __str__(self):
        return self.teamName