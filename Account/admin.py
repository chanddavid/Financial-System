from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id','username','phone_number','email']
    list_display_links = ['id','username',]
    list_filter = ['username','email','phone_number']
    search_fields = ['email','username','phone_number']


    
    user_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ( 'email','phone_number','date_of_birth','citizenship_number','address')}),
        (_('Permissions'), {
            'fields': ('is_active','is_superuser','user_permissions'),
        }),
        (_('Group'), {'fields': ( 'groups',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','phone_number', 'password1', 'password2','is_staff'),
        }),
    )
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        else:
            if not obj.is_staff:
                return self.user_fieldsets
            return super().get_fieldsets(request, obj)
    