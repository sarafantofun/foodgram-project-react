import base64

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework.serializers import (CharField, ImageField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from rest_framework.validators import UniqueValidator

from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            Tag)
from users.models import User
from users.validators import validate_username


class RecipeIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.ingredient.id
        return data


class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredient


class TagSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug',)
        model = Tag


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class MeUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    username = CharField(
        required=True,
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()


class RecipeGetSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = MeUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        many=True,
        source='recipeingredient'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.fan.filter(recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.carts.filter(recipe=obj.id).exists()


class RecipeNotGetSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        model = Recipe

    @transaction.atomic
    def create_ingredients(self, ingredients, recipe):
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.get('tags', instance.tags)
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeGetSerializer(
            instance,
            context={'request': request}
        ).data


class RecipeShortSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'name', 'image', 'cooking_time',
        )
        model = Recipe


class SubscriptionSerializer(MeUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = IntegerField(source='recipes.count', read_only=True)

    class Meta(MeUserSerializer.Meta):
        fields = MeUserSerializer.Meta.fields + (
            'recipes', 'recipes_count',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name',)

    def validate(self, data):
        author_id = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('id')
        author = get_object_or_404(User, id=author_id)
        user = self.context.get('request').user
        if user == author or user.follower.filter(author=author).exists():
            raise ValidationError('Ошибка подписки!')
        return data

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeShortSerializer(recipes, many=True)
        return serializer.data


class FavoriteSerializer(RecipeShortSerializer):

    class Meta(RecipeShortSerializer.Meta):
        fields = RecipeShortSerializer.Meta.fields

    def validate(self, data):
        recipe_pk = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        user = self.context.get('request').user
        if user.fan.filter(recipe=recipe).exists():
            raise ValidationError('Рецепт уже есть в избранном!')
        return data


class ShoppingCartSerializer(RecipeShortSerializer):

    class Meta(RecipeShortSerializer.Meta):
        fields = RecipeShortSerializer.Meta.fields

    def validate(self, data):
        recipe_pk = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        user = self.context.get('request').user
        if user.carts.filter(recipe=recipe).exists():
            raise ValidationError('Рецепт уже есть в списке покупок!')
        return data
