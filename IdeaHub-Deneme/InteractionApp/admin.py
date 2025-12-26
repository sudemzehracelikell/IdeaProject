from django.contrib import admin
from .models import Comment, Vote

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'idea', 'user', 'comment_date')
    list_filter = ('comment_date',)
    search_fields = ('text', 'user__userName')
    ordering = ('-comment_date',)
    readonly_fields = ('comment_date',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'idea', 'user', 'value')
    list_filter = ('value',)
    search_fields = ('user__userName',)
    ordering = ('id',)
