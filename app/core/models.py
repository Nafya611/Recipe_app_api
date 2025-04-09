"""Database models"""

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,

)

from app import settings


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self,email,password=None, **extra_field):
        if not email:
            raise ValueError('user must have an email addres.')
        user=self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        user= self.create_user(email,password)
        user.is_staff= True
        user.is_superuser= True
        user.save(using=self._db)

        return user





class User(AbstractBaseUser,PermissionsMixin):
    """user in the system"""
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects= UserManager()

class Recipe(models.Model):
    """Recipe object"""
    user= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    title= models.CharField(max_length=255)
    description= models.TextField(blank=True)
    time_minutes= models.IntegerField()
    price= models.DecimalField(max_digits=5,decimal_places=2)
    link= models.CharField(max_length=255,blank=True)
    tags=models.ManyToManyField('Tag')
    ingredients=models.ManyToManyField('Ingredient')
    image1=models.ImageField(null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes"""
    name=models.CharField(max_length=255)
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredients for recipes"""
    name=models.CharField(max_length=255)
    user= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE

    )

    def __str__(self):
        return self.name








