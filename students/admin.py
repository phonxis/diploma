from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile


admin.site.unregister(User)

class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline,]

admin.site.register(User, UserAdmin)
