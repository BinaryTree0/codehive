from django.contrib import admin

from .models import Post, Profile, ProfileSkill, Skill, Company

# Register your models here.
admin.site.register(Post, admin.ModelAdmin)
admin.site.register(Profile, admin.ModelAdmin)
admin.site.register(Skill, admin.ModelAdmin)
admin.site.register(ProfileSkill, admin.ModelAdmin)
admin.site.register(Company, admin.ModelAdmin)
