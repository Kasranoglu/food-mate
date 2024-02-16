from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')

        if not extra_fields.get('is_active'):
            raise ValueError('Superuser must have is_active = True')

        return self.create_user(email, password, **extra_fields)




class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Şifre, 20 karaktere kadar
    email = models.EmailField(max_length=128, unique=True)  # E-posta adresi, 40 karaktere kadar, benzersiz
    phone_number = models.CharField(max_length=17, null=True)
    first_name = models.CharField(max_length=300, null=True)  # İsim, 30 karaktere kadar
    last_name = models.CharField(max_length=300, null=True)  # Soyisim, 30 karaktere kadar
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  # Cinsiyet, seçenekler: Male, Female, Other
    age = models.PositiveSmallIntegerField(null=True)  # Yaş, pozitif küçük tamsayı
    height = models.PositiveSmallIntegerField(null=True)  # Boy, pozitif küçük tamsayı
    weight = models.PositiveSmallIntegerField(null=True)  # Kilo, pozitif küçük tamsayı
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["gender", "email"]

    object = UserManager()

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True