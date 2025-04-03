from django.contrib import admin
from .models import User, MembershipInfo, AdditionalPersonalInfo, Qualification, WorkExperience

# Inline model for MembershipInfo
class MembershipInfoInline(admin.StackedInline):
    model = MembershipInfo
    can_delete = False  
    verbose_name_plural = 'Membership Info'

class AdditionalPersonalInfoInline(admin.StackedInline):
    model = AdditionalPersonalInfo
    can_delete = False
    verbose_name_plural = 'Additional Personal Info'

class QualificationInline(admin.TabularInline):  
    model = Qualification
    extra = 1  
    verbose_name_plural = 'Qualifications'

class WorkExpInline(admin.TabularInline):  
    model = WorkExperience
    extra = 1  
    verbose_name_plural = 'WorkExperiences'

# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    inlines = [MembershipInfoInline, AdditionalPersonalInfoInline, QualificationInline,WorkExpInline]
    list_display = ('first_name', 'last_name', 'email')  

# Unregister the default User admin if it's registered
# admin.site.unregister(User)

# Register the custom User admin with inlines
admin.site.register(User, UserAdmin)

# Inline model for MembershipInfo
admin.site.register(AdditionalPersonalInfo)
admin.site.register(MembershipInfo)
admin.site.register(Qualification)
admin.site.register(WorkExperience)
