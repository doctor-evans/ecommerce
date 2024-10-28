from django.contrib import admin

from userauth.models import User, ContactUs


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'bio'
    ]

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
