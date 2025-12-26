from django.db import models

from IdeaApp.models import Idea


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    idea = models.ForeignKey('IdeaApp.Idea', on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.user.userName} - {self.text[:20]}"



class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name="votes")
    value = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.userName} voted {self.value} on {self.idea.Title}"


