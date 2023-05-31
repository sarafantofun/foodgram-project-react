from django.contrib import admin

from .models import (
    Favorite, Tag, Recipe, ShoppingCart, Ingredient, RecipeIngredient
)
from users.models import User


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)


class RecipeIngredientAdmin(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'text',
        'cooking_time',
        'pub_date',)
    inlines = (RecipeIngredientAdmin, )
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ('favorites',)

    def favorites(self, obj):
        result = User.objects.filter(fan__recipe=obj).count()
        return result


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
