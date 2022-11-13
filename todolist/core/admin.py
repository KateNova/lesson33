from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    exclude = ('password',)
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, UserAdmin)
