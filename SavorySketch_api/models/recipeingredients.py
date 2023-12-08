from django.db import models

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE, related_name="ingredient_on", null=True)
    measurement = models.ForeignKey("Measurement", on_delete=models.CASCADE, related_name="measurement_on", null=True)