from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def get_profile_image_path(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_profile_image_filename(self):
    path = self.profile_image
    name_start_from = path.index(f'profile_images/{self.pk}/')
    extract_file_name = path[name_start_from:]
    return extract_file_name

def get_default_profile_image():
    return f'default_avatar.jpg'

class AccountManager(BaseUserManager):
    # Custom user model manager where email is the unique identifiers
    # for authentication instead of usernames.
    def create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password.
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    email                  = models.EmailField(verbose_name='email', max_length=255, unique=True, help_text='enter your email')
    username               = models.CharField(max_length=50)
    date_joined            = models.DateTimeField(auto_now_add=True, verbose_name='date_joined')
    last_login             = models.DateTimeField(auto_now=True, verbose_name='last_login')
    profile_image          = models.ImageField(upload_to=get_profile_image_path, max_length=255, null=True, blank=True, default=get_default_profile_image)
    hide_email             = models.BooleanField(default=True)

    # для AbstractBaseUser
    is_admin               = models.BooleanField(default=False)
    is_active              = models.BooleanField(default=True)
    is_staff               = models.BooleanField(default=False)
    is_superuser           = models.BooleanField(default=False)

    # указать кастомный аккаунт менеджер для создания юзеров
    objects = AccountManager()

    # поле, которое замещает стандартное поле username
    USERNAME_FIELD = 'email'

    # необходимые поля для заполнения
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
