# Generated by Django 4.2.8 on 2023-12-08 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SavorySketch_api', '0002_recipe_ingredients_alter_savoryuser_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='measurements',
            field=models.ManyToManyField(related_name='recipe', through='SavorySketch_api.RecipeIngredient', to='SavorySketch_api.measurement'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_on', to='SavorySketch_api.ingredient'),
        ),
    ]
