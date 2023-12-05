from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from SavorySketch_api.models import Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'name']
        
class MeasurementViewSet(viewsets.ViewSet):
    
    def list(self, request):
        measurement = Measurement.objects.all()
        serializer = MeasurementSerializer(measurement, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            measurement = Measurement.objects.get(pk=pk)
            serializer = MeasurementSerializer(measurement)
            return Response(serializer.data)
        except Measurement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        name = request.data.get('name')
        measurement = Measurement.objects.create(
            name=name
        )
        serializer = MeasurementSerializer(measurement, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        try:
            measurement = Measurement.objects.get(pk=pk)
            self.check_object_permissions(request, measurement)
            measurement.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Measurement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)