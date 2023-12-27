from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from SavorySketch_api.models import Ingredient, Measurement, SavoryUser, Recipe, Cuisine, RecipeIngredient
from SavorySketch_api.views.savoryusers import SavoryUserSerializer, SavoryUserUserSerializer
from SavorySketch_api.views import IngredientSerializer, MeasurementSerializer


class RecipeCuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id','name']
        
class RecipeIngredientMeasurementSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False)
    measurement = MeasurementSerializer(many=False)
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'measurement']

class RecipeSavoryUserSerializer(serializers.ModelSerializer):
    user = SavoryUserUserSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'user']
    
class UpdatedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'number_of_likes']
    

class RecipeSerializer(serializers.ModelSerializer):
    user = RecipeSavoryUserSerializer(many=False)
    cuisine = RecipeCuisineSerializer(many=False)
    recipe_ingredients = RecipeIngredientMeasurementSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'publication_date', 'image', 'directions', 'number_of_likes', 'cuisine', 'recipe_ingredients' ]
        
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
    
    def destroy(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            self.check_object_permissions(request, recipe)
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        user = SavoryUser.objects.get(pk=request.user.id)
        cuisine = Cuisine.objects.get(pk=request.data['cuisine'])
        recipe = Recipe.objects.create(
            user=user,
            cuisine=cuisine,
            title=request.data.get('title'),
            description=request.data.get('description'),
            image=request.data.get('image'),
            directions=request.data.get('directions')
        )
        
        ingredients = request.data.get('ingredients', [])
        measurements = request.data.get('measurements', [])
        for ingredient_id, measurement_id in zip(ingredients, measurements):
            ingredient_instance = Ingredient.objects.get(pk=ingredient_id)
            measurement_instance = Measurement.objects.get(pk=measurement_id)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_instance,
                measurement=measurement_instance
            )
        
        serializer = RecipeSerializer(recipe, context={'request': request})
        try:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = UpdatedRecipeSerializer(data=request.data)
            if serializer.is_valid():
                recipe.number_of_likes = serializer.validated_data['number_of_likes']
                recipe.save()
                serializer = UpdatedRecipeSerializer(recipe, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)