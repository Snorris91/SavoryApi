from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from SavorySketch_api.models import Recipe, Comment, SavoryUser
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
    
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        
        user = SavoryUser.objects.get(pk=request.user.id)
        recipe = Recipe.objects.get(pk=request.data['recipe'])
        comment = Comment.objects.create(
            user=user,
            recipe=recipe,
            content=request.data.get('content')
        )

        serializer = CommentSerializer(comment, many=False)
        try:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)