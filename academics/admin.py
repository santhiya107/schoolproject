from django.contrib import admin
from .models import Grade,Subject,Chapter

# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.user_type == 'is_staff':
            return False
        
class GradeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.user_type == 'is_staff':
            return False

admin.site.register(Grade,GradeAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Chapter)