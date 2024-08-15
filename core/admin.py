from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(RecipeIngredients)
admin.site.register(Ingredients)
admin.site.register(Unit)
admin.site.register(ShoppingList)
admin.site.register(ShoppingListItem)
admin.site.register(DietProgram)
admin.site.register(DietProgramItem)
admin.site.register(MealType)
admin.site.register(DietType)
admin.site.register(Category)
admin.site.register(Special_types)
admin.site.register(AboutUs)
admin.site.register(Feedback)

