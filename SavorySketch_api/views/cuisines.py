from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from SavorySketch_api.models import Cuisine

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']
        
class CuisineViewSet(viewsets.ViewSet):
    
    def list(self, request):
        cuisine = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisine, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            cuisine = Cuisine.objects.get(pk=pk)
            serializer = CuisineSerializer(cuisine)
            return Response(serializer.data)
        except Cuisine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        name = request.data.get('name')
        cuisine = Cuisine.objects.create(
            name=name
        )
        serializer = CuisineSerializer(cuisine, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        try:
            cuisine = Cuisine.objects.get(pk=pk)
            self.check_object_permissions(request, cuisine)
            cuisine.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Cuisine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)