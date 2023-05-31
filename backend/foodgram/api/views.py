from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from recipes.models import (Ingredient, Favorite, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from users.models import User, Subscription

from api.filters import RecipeFilter
from .permissions import (IsAuthorOrReadOnly)
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipeNotGetSerializer,
                          RecipeShortSerializer, MeUserSerializer,
                          SubscriptionSerializer)


class MeUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MeUserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(following__user=user)
        serializer = SubscriptionSerializer(
            subscriptions,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        methods=['post', 'delete', ],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author or Subscription.objects.filter(
                user=user,
                author=author
            ).exists():
                return Response({'detail': 'Ошибка подписки!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Subscription.objects.filter(user=user, author=author).exists():
                subscription = Subscription.objects.filter(
                    user=user,
                    author=author
                )
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'detail': 'Вы не подписаны на данного пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeGetSerializer
        return RecipeNotGetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete', ],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже есть в избранном!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                favorite = Favorite.objects.filter(user=user, recipe=recipe)
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': 'Данного рецепта нет в избранном!'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'delete', ],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'detail': 'Рецепт уже есть в списке покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                shopping = ShoppingCart.objects.filter(
                    user=user,
                    recipe=recipe
                )
                shopping.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'detail': 'Данного рецепта нет в списке покупок!'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_carts__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(amount=Sum('amount'))
        text = ''
        for ingredient in ingredients:
            text += (
                f'•  {ingredient["ingredient__name"]}'
                f'({ingredient["ingredient__measurement_unit"]})'
                f'— {ingredient["amount"]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        response.headers[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.txt"'
        return response


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
