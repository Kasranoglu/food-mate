from django.urls import path
from web import views

urlpatterns = [
    path('about-us', views.about_us, name="about us"),
    path('add-recipe', views.add_recipe, name="add recipe"),
    path('add-recipe-ingredients/<slug:slug>/', views.add_recipe_ingredients, name="add recipe ingredients"),
    path('home',views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('diet', views.diet, name="diet"),
    path('profile-page', views.profile_page, name="profile page"),
    path('recipe-details/<slug:slug>/', views.recipe_details, name="recipe details"),
    path('recipes', views.recipes, name="recipes"),
    path('shopping-list', views.shopping_list, name="shopping list"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('feedback', views.feedback, name="feedback_message"),
    path('add_to_shopping_list/<slug:slug>/', views.add_to_shopping_list, name="add to shopping list"),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),  # Burada edit-item URL'si tanımlanıyor

]
