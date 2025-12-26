
from django.db import models

from TeamApp.models import Team

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    
class Status(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Public', 'Public'),
        ('Closed', 'Closed'),
    ]
    name = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    
    def __str__(self):
        return self.name

class Media(models.Model):
    MEDIA_TYPES = [
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Document', 'Document'),
    ]
    MediaID = models.AutoField(primary_key=True)
    MediaPath = models.FileField(upload_to='media/')
    MediaType = models.CharField(max_length=20, choices=MEDIA_TYPES)
    IdeaID = models.ForeignKey('Idea', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.MediaType} for {self.IdeaID.Title}"
    
class Tag(models.Model):
    TagID = models.AutoField(primary_key=True)
    TagName = models.CharField(max_length=100)

    def __str__(self):
        return self.TagName

class Idea(models.Model):
    Title = models.CharField(max_length=200)
    Description = models.TextField()
    ShortDescription = models.TextField() #CharField(max_length=500) de olabilir.
    CreateDate = models.DateTimeField(auto_now_add=True)
    VotesCount = models.IntegerField(default=0)
    IdeaID = models.AutoField(primary_key=True)
    CreaterID = models.ForeignKey('UserApp.User', on_delete=models.CASCADE)
    StatusID = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    CategoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    TeamID = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    Tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.Title

class Update(models.Model):
    class State(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "Devam Ediyor"
        COMPLETED = "COMPLETED", "Tamamlandı"
        WAITING = "WAITING", "Beklemede"
        CANCELLED = "CANCELLED", "İptal Edildi"

    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name="updates")
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="updates")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.idea.title}"
