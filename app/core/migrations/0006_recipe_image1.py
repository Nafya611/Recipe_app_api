# Generated by Django 4.2.20 on 2025-04-09 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image1',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
