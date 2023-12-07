from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from SavorySketch_api.models import Ingredient, RecipeIngredient, Measurement, Recipe
from SavorySketch_api.views import IngredientSerializer, MeasurementSerializer

class SimpleRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False)
    measurement = MeasurementSerializer(many=False)
    recipe = SimpleRecipeSerializer(many=False)
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'measurement', 'recipe']

class RecipeIngredientView(ViewSet):
    def list(self, request):
        recipe_ingredients = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(recipe_ingredients, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        try:
            recipe_ingredients = RecipeIngredient.objects.get(pk=pk)
            serializer = RecipeIngredientSerializer(recipe_ingredients, many=False, context={'request': request})
            return Response(serializer.data)
        except RecipeIngredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        recipe = Recipe.objects.get(pk=request.data['recipe'])
        measurement = Measurement.objects.get(pk=request.data['measurement'])
        ingredient = Ingredient.objects.get(pk=request.data['ingredient'])
        
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe = recipe,
            measurement =  measurement,
            ingredient = ingredient
        )
        recipe_ingredient.save()
        
        try:
            serializer = RecipeIngredientSerializer(recipe_ingredient, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(None, status=status.HTTP_4)