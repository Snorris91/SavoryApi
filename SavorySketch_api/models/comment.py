from django.db import models

class Comment(models.Model):
    user = models.ForeignKey("SavoryUser", on_delete=models.CASCADE, related_name="user_comments")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_comments")
    content = models.CharField(max_length=500)
    created_on = models.DateField(auto_now=True)
