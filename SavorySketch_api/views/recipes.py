from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from SavorySketch_api.models import Ingredient, Measurement, SavoryUser, Recipe, Cuisine
from SavorySketch_api.views.savoryusers import SavoryUserSerializer, SavoryUserUserSerializer


class RecipeCuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['name']

class RecipeSavoryUserSerializer(serializers.ModelSerializer):
    user = SavoryUserUserSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'user']
    

class RecipeSerializer(serializers.ModelSerializer):
    user = RecipeSavoryUserSerializer(many=False)
    cuisine = RecipeCuisineSerializer(many=False)
    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'publication_date', 'image', 'directions', 'number_of_likes', 'cuisine' ]
        
class SimpleRecipeSerializer(serializers.ModelSerializer):
    user = RecipeSavoryUserSerializer(many=False)
    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'image']
        
class RecipeView(ViewSet):
    def retrieve(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        recipe = Recipe.objects.all()
        serializer = RecipeSerializer(recipe, many=True, context={'request': request})
        return Response(serializer.data)