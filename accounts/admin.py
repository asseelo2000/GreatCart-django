from django.contrib import admin
from .models import Account
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountsAdmin(UserAdmin):
    # Fields to display in the detail view of a user
    readonly_fields = ('password', 'is_active')  # Make the password field read-only
    list_display_links = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your model with the customized admin
admin.site.register(Account, AccountsAdmin)
