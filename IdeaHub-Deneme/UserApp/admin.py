from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'userName', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('userName', 'email')
    ordering = ('id',)
