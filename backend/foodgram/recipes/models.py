from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.TextField(
        unique=True,
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(unique=True, max_length=200, verbose_name='Слаг')
    color = models.CharField(
        max_length=7,
        default="#ffffff",
        unique=True,
        verbose_name='Цвет'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        blank=True
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(720)],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fan',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'recipe')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ('user', 'recipe')


class Ingredient(models.Model):
    name = models.TextField(max_length=200, verbose_name='Название')
    measurement_unit = models.TextField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    amount = models.IntegerField(
        validators=(MinValueValidator(1), ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'РецептИнгредиент'
        verbose_name_plural = 'РецептыИнгредиенты'
