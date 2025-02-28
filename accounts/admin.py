from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, MotherTongue

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_mother_tongue', 'get_avg_ielts_score', 'get_practice_count')
    
    def get_mother_tongue(self, instance):
        return instance.profile.mother_tongue
    get_mother_tongue.short_description = 'Mother Tongue'
    
    def get_avg_ielts_score(self, instance):
        return instance.profile.avg_ielts_score
    get_avg_ielts_score.short_description = 'Avg. IELTS Score'
    
    def get_practice_count(self, instance):
        return instance.profile.practice_count
    get_practice_count.short_description = 'Practice Count'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(MotherTongue)