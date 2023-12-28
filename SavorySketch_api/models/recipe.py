from django.db import models

class Recipe(models.Model):
    user = models.ForeignKey("SavoryUser", on_delete=models.CASCADE, related_name="recipe_by_user")
    cuisine = models.ForeignKey("Cuisine", on_delete=models.CASCADE, related_name="recipe_cuisine")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    publication_date = models.DateField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    directions = models.CharField(max_length=2000)
    number_of_likes = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(
        "Ingredient",
        through='RecipeIngredient',
        related_name="recipe_ingredients"
    )
    measurements = models.ManyToManyField(
        "Measurement",
        through='RecipeIngredient',
        related_name="recipe_measurements"
    )