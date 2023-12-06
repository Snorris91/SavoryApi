from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from SavorySketch_api.models import Recipe, Comment
from SavorySketch_api.views.savoryusers import SavoryUserSerializer
from SavorySketch_api.views.recipes import SimpleRecipeSerializer


# class CommentSavoryUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id', 'user']

class CommentSerializer(serializers.ModelSerializer):
    recipe = SimpleRecipeSerializer(many=False)
    user = SavoryUserSerializer(many=False)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'recipe', 'content']


class CommentView(ViewSet):
    def retrieve(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True, context={'request': request})
        return Response(serializer.data)