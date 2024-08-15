from django import forms
from core.models import Recipe, RecipeIngredients, Ingredients


class RecipeAddForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['photo', 'name', 'description', 'how_to', 'cooking_time', 'prep_time', 'categories', 'special_types',
                  'tags', 'meal_types', 'diet_types', 'calorie', 'serving_size']


class RecipeAddIngredientsForm(forms.ModelForm):
    custom_ingredient = forms.CharField(max_length=100, required=False, label="Malzeme", help_text="patates")

    class Meta:
        model = RecipeIngredients
        fields = ['unit', 'quantity']





    def save(self, commit=True):
        instance = super(RecipeAddIngredientsForm, self).save(commit=False)
        custom_ingredient = self.cleaned_data.get('custom_ingredient')
        if custom_ingredient:
            ingredient, created = Ingredients.objects.get_or_create(name=custom_ingredient)
            instance.ingredients = ingredient
        if commit:
            instance.save()
        return instance
