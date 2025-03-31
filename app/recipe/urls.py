from django.urls  import path,include
from .views import recipe_list,recipe_detail,tag_list,tag_detail

urlpatterns=[
    path('recipes/', recipe_list, name='recipe-list'),
    path('recipes/<int:pk>', recipe_detail, name= 'recipe-detail'),
    path('tags/', tag_list, name='tag-list'),
    path('tags/<str:name>',tag_detail,name='tag-detail'),
]