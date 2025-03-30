from django.urls  import path,include
from .views import recipe_list,recipe_detail

urlpatterns=[
    path('recipes/', recipe_list, name='recipe-list'),
    path('recipes/<int:pk>', recipe_detail, name= 'recipe-detail')
]