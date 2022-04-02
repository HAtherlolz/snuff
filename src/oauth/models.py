from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import get_path_upload_avatar, validate_size_image


class CustomUserManager(BaseUserManager):
    """  Custom user model manager where email is the unique identifiers  for authentication instead of usernames.  """
    def create_user(self, email, password, **extra_fields):
        """  Create and save a User with the given email and password.  """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """  Create and save a SuperUser with the given email and password.  """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    """ Model for user in platform """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @property
    def is_authenticated(self):
        """ It always return True. It's a way to know that user is authenticated """
        return True

    def __str__(self):
        return self.email


class Follower(models.Model):
    """ Follower Model """
    user = models.ForeignKey('AuthUser', on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey('AuthUser', on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} followed on {self.user}'


class SocialLink(models.Model):
    """ Model for link on user's social links """
    user = models.ForeignKey('AuthUser', on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'{self.user}'