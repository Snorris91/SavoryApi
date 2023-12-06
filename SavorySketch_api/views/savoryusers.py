from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from SavorySketch_api.models import SavoryUser

class SavoryUserUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'date_joined']
        
class SavoryUserSerializer(serializers.ModelSerializer):
    user = SavoryUserUserSerializer(many=False)
    profile_img = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    
    def get_created_on(self, obj):
        return f'{obj.created_on.month}/{obj.created_on.day}/{obj.created_on.year}'
    
    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img
        return 'https://cdn1.iconfinder.com/data/icons/user-pictures/100/ctures/100/unknown'
    
    class Meta:
        model = SavoryUser
        fields = ['id', 'user', 'profile_img', 'biography', 'created_on']
        
class SimpleSavoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavoryUser
        fields = ['id', 'user', 'profile_img']

class SavoryUserView(ViewSet):
    
    def list(self, request):
        savory_users = SavoryUser.objects.all()
        serializer = SavoryUserSerializer( savory_users, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        try:
            savory_users = SavoryUser.objects.get(pk=pk)
            serializer = SavoryUserSerializer( savory_users, context={'request': request})
            return Response(serializer.data)
        except SavoryUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)