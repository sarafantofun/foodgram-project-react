import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework.serializers import (
    BooleanField, CharField, ImageField, IntegerField,
    ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField,
    ReadOnlyField
)
from rest_framework.validators import UniqueValidator
from recipes.models import (
    Tag, Recipe, RecipeIngredient, ShoppingCart, Ingredient, Favorite
)
from users.models import User, Subscription
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
        max_length=150,
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
        return Subscription.objects.filter(user=user, author=obj).exists()


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
        return Favorite.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj.id).exists()


class RecipeNotGetSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        model = Recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient = ingredient['id']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get('tags', instance.tags)
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()
            for ingredient in ingredients:
                current_ingredient = ingredient['id']
                amount = ingredient['amount']
                recipe = instance
                RecipeIngredient.objects.update_or_create(
                    ingredient=current_ingredient,
                    recipe=recipe,
                    defaults={'amount': amount}
                )
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


class SubscriptionSerializer(ModelSerializer):
    is_subscribed = BooleanField(default=True)
    recipes = SerializerMethodField()
    recipes_count = IntegerField(source='recipes.count', read_only=True)

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        model = User

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeShortSerializer(recipes, many=True)
        return serializer.data
