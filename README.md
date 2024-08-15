# FoodMate

FoodMate is a web application built using Django Rest Framework and Python. The app allows users to browse and add recipes, manage a shopping cart, and manually add items to a shopping list.

## Features

- **User Registration and Login:**
  - Users can register and log in to the system.
  
- **Recipes:**
  - Users can view existing recipes.
  - Users can add and share their own recipes.
  
- **Shopping Cart:**
  - Recipe ingredients can be automatically added to the shopping cart.
  - Users can manually add items to the shopping list.

- **Admin Panel:**
  - Admin can use admin panel which django provides, so you can manually manipulate everything from there.


## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/foodmate.git
   cd foodmate


python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
