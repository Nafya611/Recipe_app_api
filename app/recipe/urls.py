from django.urls  import path,include
from .views import recipe_list

urlpatterns=[
    path('recipes/', recipe_list, name='recipe-list')
]