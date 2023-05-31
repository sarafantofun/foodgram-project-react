from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
