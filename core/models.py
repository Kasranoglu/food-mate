from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.template.defaultfilters import slugify

from core.constants import STATUS_CHOICES, STATUS_DRAFT, CHEF_CHOICES, STATUS_PASSIVE, DIET_STATUS_CHOICES


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


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, TimeStampMixin):
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
    allergens = models.ManyToManyField('Ingredients')
    diet_types = models.ManyToManyField('DietType')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["gender", "email"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True


class Ingredients(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class DietType(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=60)

    def get_all_categories_as_text(self):
        return ", ".join([category.name for category in self.all()])

    def __str__(self):
        return self.name


class Special_types(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class MealType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Recipe(TimeStampMixin):
    slug = models.SlugField('slug', max_length=255,
                            unique=True, null=True, blank=True,
                            )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipe_author", null=True)
    photo = models.ImageField(upload_to='recipe_photos/')
    name = models.CharField(max_length=50)
    description = models.TextField()
    how_to = models.TextField(null=True, blank=True)
    cooking_time = models.PositiveSmallIntegerField()  # Dakika cinsinden tahmini süre
    prep_time = models.PositiveSmallIntegerField(default=0)  # Dakika cinsinden tahmini süre
    categories = models.ManyToManyField('Category')
    special_types = models.ManyToManyField('Special_types')
    tags = models.CharField(max_length=100)  # Birden fazla etiket virgülle ayrılabilir
    meal_types = models.ManyToManyField('MealType')
    diet_types = models.ManyToManyField('DietType')
    calorie = models.PositiveSmallIntegerField()  # Kalori
    serving_size = models.PositiveSmallIntegerField()  # Porsiyon boyutu
    status = models.CharField(choices=STATUS_CHOICES, max_length=40, default=STATUS_DRAFT)
    chef_choice = models.CharField(choices=CHEF_CHOICES, default=STATUS_PASSIVE)  #0 passive 1 active
    chef_popular = models.CharField(choices=CHEF_CHOICES, default=STATUS_PASSIVE)  #0 passive 1 active

    def __str__(self):
        return self.name

    def get_all_categories_as_text(self):
        return ", ".join([category.name for category in self.categories.all()])

    def get_diet_type_as_text(self):
        return ", ".join([type.name for type in self.diet_types.all()])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Recipe.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super(Recipe, self).save(*args, **kwargs)


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredients = models.ForeignKey('Ingredients', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    quantity = models.FloatField(max_length=100)

    def get_ingredient_count(self):
        ingredients_in_recipe = RecipeIngredients.objects.filter(recipe=self.recipe)
        return ingredients_in_recipe.count()

    def __str__(self):
        return self.recipe.name


class ShoppingList(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list =(('1', 'Active'), ('0', 'Deactive'))
    status = models.IntegerField(choices=list, default=1)  # 1: active, 0: passive

    def __str__(self):
        return f"Shopping list for {self.user.username} - Status: {self.status}"


class ShoppingListItem(TimeStampMixin):
    shopping_list = models.ForeignKey('ShoppingList', on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    list =(('1', 'Active'), ('0', 'Deactive'))
    status = models.IntegerField(choices=list, default=1)  # 1: active, 0: passive


class DietProgram(TimeStampMixin):
    name = models.CharField(max_length=60)
    slug = models.SlugField('slug', max_length=255,
                            unique=True, null=True, blank=True,
                            )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly')], max_length=1)  # Gunluk, Haftalik
    description = models.TextField(max_length=10000)
    status = models.CharField(choices=DIET_STATUS_CHOICES, max_length=40, default=STATUS_DRAFT)# 0: taslak, 1: tamamlandi kendime 2: paylasima acik


class Feedback(TimeStampMixin):
    fullname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=128, unique=True)  # E-posta adresi, 40 karaktere kadar, benzersiz
    subject = models.TextField(max_length=300)
    content = models.TextField(max_length=3000)

    def __str__(self):
        return f'{self.fullname} - {self.subject}'

    class Meta:
        ordering = ("-updated_at",)


class DietProgramItem(TimeStampMixin):
    diet_program = models.ForeignKey('DietProgram', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    list = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5'), ('6', '6'), ('7', '7'))
    day = models.IntegerField(choices=list)
    meal_types = models.ManyToManyField('MealType')


class AboutUs(models.Model):
    main_photo = models.ImageField(upload_to='about_us_photos/')
    header_main = models.CharField(max_length=300)
    text_main = models.TextField(max_length=3000)
    list = (('active', 'Active'), ('deactive', 'Deactive'))
    status = models.CharField(choices=list, max_length=100, default="deactive")

    def __str__(self):
        return f'About us - {self.status}'

    class Meta:
        verbose_name = 'AboutUs'
        verbose_name_plural = 'AboutUs'


class Subscribe(TimeStampMixin):
    email = models.EmailField(max_length=128, unique=True)
