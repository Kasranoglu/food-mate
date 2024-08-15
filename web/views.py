import random

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from core import settings
from core.constants import STATUS_PUBLISHED, STATUS_ACTIVE
from core.models import User, Recipe, RecipeIngredients, AboutUs, Feedback, Category, Special_types, MealType, DietType, \
    Unit, Ingredients, ShoppingList, ShoppingListItem
from web.forms import RecipeAddForm, RecipeAddIngredientsForm


def home(request):
    popular_recipes = list(Recipe.objects.filter(chef_popular=STATUS_ACTIVE))
    chef_recipes = list(Recipe.objects.filter(chef_choice=STATUS_ACTIVE))

    if chef_recipes:
        random_recipe2 = random.choice(chef_recipes)
        chef_recipes.remove(random_recipe2)
    else:
        random_recipe2 = None

    chef_column = chef_recipes[:4]

    # Rastgele bir tarif seç
    if popular_recipes:
        random_recipe = random.choice(popular_recipes)
        popular_recipes.remove(random_recipe)
    else:
        random_recipe = None

    popular_column = popular_recipes[:2]

    for recipe in popular_column:
        popular_recipes.remove(recipe)

    popular_column2 = popular_recipes[:2]

    return render(request, 'index.html', {
        'r_recipe': random_recipe,
        'p_recipes': popular_column,
        'p_recipes2': popular_column2,
        'c_recipes': chef_column,
        'r_recipe2': random_recipe2,


    })


def about_us(request):
    current_time = timezone.now().strftime("<span>%d %B %Y</span>")
    content = AboutUs.objects.get(status='active')
    recipes_list = Recipe.objects.filter(author__username='ahmetali', status=STATUS_PUBLISHED)
    return render(request, 'about-us.html', {
        'current_time': current_time,
        'content': content,
        'recipes': recipes_list
    })


@login_required(login_url='signin')
def add_recipe(request):
    form = RecipeAddForm
    categories = Category.objects.all()
    special_types = Special_types.objects.all()
    meal_types = MealType.objects.all()
    diet_types = DietType.objects.all()
    if request.method == 'POST':
        form = RecipeAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            post = form.save()
            return redirect('add recipe ingredients', slug=post.slug)
        else:
            return render(request, 'add-recipe.html', {
            })
    else:
        return render(
            request,
            'add-recipe.html', {
                'form': form,
                'categories': categories,
                'special_types': special_types,
                'meal_types': meal_types,
                'diet_types': diet_types,
            }
        )


@login_required(login_url='signin')
def add_recipe_ingredients(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
    unit = Unit.objects.all()

    if request.method == 'POST':
        if 'sil' in request.POST:
            ingredient_id = request.POST.get('ingredient_id')
            try:
                ingredient = RecipeIngredients.objects.get(pk=ingredient_id)
                ingredient.delete()
                messages.success(request, 'Malzeme başarıyla silindi.')
            except Ingredients.DoesNotExist:
                messages.error(request, 'Silinmek istenen malzeme bulunamadı.')
            return redirect('add recipe ingredients', slug=slug)
        else:
            form = RecipeAddIngredientsForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.recipe = recipe
                form.save()
                messages.success(request, 'Malzeme başarıyla eklendi.')
                return redirect('add recipe ingredients', slug=slug)
            else:
                messages.error(request, 'Form geçersiz. Lütfen girdiğiniz bilgileri kontrol edin.')
    else:
        form = RecipeAddIngredientsForm()
        return render(
            request,
            'add-recipe-ingredients.html',
            {'form': form,
             'ingredients': ingredients,
             'unit': unit,
             'recipe': recipe,
             }
        )


def contact(request):
    return render(request, 'contact.html')


def diet(request):
    return render(request, 'diet.html')


def profile_page(request):
    return render(request, 'profile-page.html')


def recipe_details(request, slug):
    chosen_recipe = get_object_or_404(Recipe, slug=slug)
    chosen_recipe_ingredients = RecipeIngredients.objects.filter(recipe=chosen_recipe)
    recipe = Recipe.objects.all()
    ingredients_counter = chosen_recipe_ingredients.first()
    return render(
        request,
        'recipe-details.html',
        {
            'recipes': recipe,
            'c_recipe': chosen_recipe,
            'c_ingredients': chosen_recipe_ingredients,
            'i_counter': ingredients_counter,
        }
    )


def recipes(request):
    recipe_objs = Recipe.objects.filter(status=STATUS_PUBLISHED)
    paginator = Paginator(recipe_objs, 9)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    return render(request, 'recipes.html', {
        'recipes': recipe_objs,
        'items': items
    })


@login_required(login_url='signin')
def add_to_shopping_list(request, slug):
    chosen_recipe = get_object_or_404(Recipe, slug=slug)
    chosen_recipe_ingredients = RecipeIngredients.objects.filter(recipe=chosen_recipe)

    # Aktif alışveriş listesini al veya yeni oluştur
    shopping_list, created = ShoppingList.objects.get_or_create(
        user=request.user,
        status=1  # aktif alışveriş listesi
    )

    # Recipe ingredients öğelerini alışveriş listesine ekle
    for ingredient in chosen_recipe_ingredients:
        formatted_quantity = "{:.1f}".format(ingredient.quantity).rstrip('0').rstrip('.')
        ShoppingListItem.objects.create(
            shopping_list=shopping_list,
            content=f" {formatted_quantity} {ingredient.unit.name} {ingredient.ingredients.name}"
        )

    # İşlem tamamlandıktan sonra tarife geri yönlendir
    return redirect('recipe details', slug=slug)


@login_required(login_url='signin')
def shopping_list(request):
    # Kullanıcının aktif alışveriş listesini al
    shopping_list, created = ShoppingList.objects.get_or_create(user=request.user, status=1)
    shopping_list_items = ShoppingListItem.objects.filter(shopping_list=shopping_list)

    if request.method == 'POST':
        # Formdan gelen veriyi işle
        new_item_content = request.POST.get('new_item')
        if new_item_content:
            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                content=new_item_content,
                status=1,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return redirect('shopping list')

    return render(request, 'shopping-list.html', {
        'shopping_list_items': shopping_list_items,
    })


def feedback(request):
    fullname = request.POST['fullname']
    email = request.POST['email']
    subject = request.POST['subject']
    content = request.POST['content']

    Feedback.objects.create(
        fullname=fullname,
        email=email,
        subject=subject,
        content=content
    )
    return redirect('contact')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, 'Succes LOGIN!!!')
            return redirect('home')

        else:
            messages.error(request, 'Wrong password or ID')

    return render(request, 'signin.html')


def signup(request):
    if request.method == "POST":  # bu neden oluyor???
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist!')
            return redirect('signin')

        if len(username) > 15:
            messages.error(request, 'Max 15 char at Username!')
            return redirect('signin')

        if not username.isalnum():
            messages.error(request, 'Username must be alpha numeric!')
            return redirect('signin')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already exist!')
            return redirect('signin')

        if len(pass1) < 10:
            messages.error(request, 'Min 10 char at Password!')
            return redirect('signin')

        if pass1 != pass2:
            messages.error(request, 'NOT MATCH PASSWORDS!')
            return redirect('signin')

        myuser = User.objects.create_user(
            username=username,
            email=email,
            password=pass1,
            first_name=fname,
            last_name=lname
        )

        messages.success(request, 'Successfully Created!')

        # Welcome Email

        subject = 'Welcome to Testing World'
        message = f'Hello {myuser.first_name}! Welcome to Testing World'
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'logged out :(')
    return redirect('home')


@login_required(login_url='signin')
def remove_item(request, item_id):
    # Silinecek alışveriş listesi öğesini al
    shopping_list_item = get_object_or_404(ShoppingListItem, id=item_id)

    # Kullanıcının alışveriş listesinden öğeyi kaldır
    shopping_list_item.delete()

    # Kullanıcıyı alışveriş listesi sayfasına yönlendir
    return redirect('shopping list')


@login_required(login_url='signin')
def edit_item(request, item_id):
    # Düzenlenecek alışveriş listesi öğesini al
    shopping_list_item = get_object_or_404(ShoppingListItem, id=item_id)

    if request.method == 'POST':
        # Formdan gelen veriyi işle
        edited_content = request.POST.get('edit_item_content')
        if edited_content:
            # Öğe içeriğini güncelle
            shopping_list_item.content = edited_content
            shopping_list_item.save()
            return redirect('shopping list')

    return redirect('shopping list')

