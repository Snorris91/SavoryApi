from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from SavorySketch_api.models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'label']
        
class IngredientViewSet(viewsets.ViewSet):
    
    def list(self, request):
        ingredient = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredient, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        label = request.data.get('label')
        ingredient = Ingredient.objects.create(
            label=label
        )
        serializer = IngredientSerializer(ingredient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            self.check_object_permissions(request, ingredient)
            ingredient.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)