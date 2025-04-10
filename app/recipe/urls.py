from django.urls  import path,include
from .views import recipe_detail,tag_list,tag_detail,ingredient_list,ingredient_detail,upload_recipe_photos_view,filter_recipes,create_recipe

urlpatterns=[

    path('recipes/',filter_recipes,name='filter_recipes'),
    path('recipe/',  create_recipe, name='recipe-list'),
    path('recipes/<int:pk>', recipe_detail, name= 'recipe-detail'),
    path('recipes/<int:recipe_id>/upload-photos/',upload_recipe_photos_view, name='upload_recipe_photos'),
    path('tags/', tag_list, name='tag-list'),
    path('tags/<str:name>',tag_detail,name='tag-detail'),
    path('ingredients/',ingredient_list, name= 'ingredient_list'),
    path('ingredients/<str:name>',ingredient_detail,name='ingredient_detail'),


]