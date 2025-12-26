from django.contrib import admin
from .models import Idea, Category, Status, Tag, Media, Update

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('TagID', 'TagName')
    search_fields = ('TagName',)
    ordering = ('TagName',)

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('IdeaID', 'Title', 'CreaterID', 'CategoryID', 'StatusID', 'VotesCount', 'CreateDate')
    list_filter = ('StatusID', 'CategoryID', 'CreateDate')
    search_fields = ('Title', 'Description')
    filter_horizontal = ('Tags',)
    ordering = ('-CreateDate',)
    readonly_fields = ('CreateDate',)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('MediaID', 'MediaType', 'IdeaID')
    list_filter = ('MediaType',)
    ordering = ('MediaID',)

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'idea', 'description', 'state', 'created_at')
    list_filter = ('state', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
