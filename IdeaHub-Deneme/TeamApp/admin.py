from django.contrib import admin
from .models import Team, TeamMember

class TeamMemberInline(admin.TabularInline):
    model = Team.teamMember.through
    extra = 1
    verbose_name = "Takım Üyesi"
    verbose_name_plural = "Takım Üyeleri"
    raw_id_fields = ('teammember',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teammember":
            kwargs["queryset"] = TeamMember.objects.select_related('user')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamName', 'get_member_count')
    search_fields = ('teamName',)
    inlines = [TeamMemberInline]
    exclude = ('teamMember',)
    ordering = ('teamName',)
    
    def get_member_count(self, obj):
        return obj.teamMember.count()
    get_member_count.short_description = 'Üye Sayısı'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_name', 'get_user_email')
    search_fields = ('user__userName', 'user__email')
    raw_id_fields = ('user',)
    ordering = ('id',)
    
    def get_user_name(self, obj):
        return obj.user.userName if obj.user else '-'
    get_user_name.short_description = 'Kullanıcı Adı'
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user else '-'
    get_user_email.short_description = 'E-posta'
