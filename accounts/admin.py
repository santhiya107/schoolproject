from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from accounts.models import User,Profile
from rest_framework.authtoken.models import TokenProxy as DRFToken
# Register your models here.

class UserAdmin(UserAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.user_type == 'is_staff':
            return False       

    list_display = ('register_number','email','phone','user_type')
    filter_horizontal = ()
    ordering = ('register_number',)
    search_fields = ['register_number']
    list_filter = ('user_type','email')
    fieldsets = (
       (None, {'fields': ('email', 'mobile_number','register_number')}),
       ('Permissions', {'fields': ('user_type',)}),
   )
    add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': ('register_number','email','phone','is_active','user_type'),
       }),
   )

class ProfileAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.user_type == 'is_staff':
            return False

        
class TokenAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.user_type == 'is_staff':
            return False
        if request.user.user_type == 'is_admin':
            return True

            
class GroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.user_type == 'is_staff':
            return False
        if request.user.user_type == 'is_admin':
            return True



admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.site_header = "School Administration"
admin.site.unregister(Group)
admin.site.register(Group,GroupAdmin)
admin.site.unregister(DRFToken)
admin.site.register(DRFToken,TokenAdmin)