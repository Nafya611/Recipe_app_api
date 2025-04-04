from django.urls  import path

from .views import create_user,create_token,manage_user

# app_name= 'user'

urlpatterns= [
    path('create/', create_user,name= 'create'),
    path('token/',create_token,name='token'),
    path('me/',manage_user,name= 'me')

]

