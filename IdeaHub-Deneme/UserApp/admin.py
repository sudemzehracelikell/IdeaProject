from django.contrib import admin
from .models import User, Roles

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Panelde hangi kolonlar görünecek?
    list_display = ('id', 'userName', 'email', 'get_role_display')
    
    # Sağ tarafta filtreleme seçenekleri
    list_filter = ('role',)
    
    # Arama çubuğu hangi alanlarda arama yapacak?
    search_fields = ('userName', 'email')
    
    # Sıralama (ID'ye göre sondan başa)
    ordering = ('-id',)

    # Rol isminin düzgün görünmesi için yardımcı fonksiyon
    def get_role_display(self, obj):
        return obj.get_role_display()
    get_role_display.short_description = 'User Role'