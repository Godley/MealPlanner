# MealPlanner
Small django application intended to manage stock and recipes. Use case:
- go to /meals/menu and get 2 weeks of recipes
- go to /meals/menu/ingredients and get 2 weeks of shopping as a collated list, excluding anything that's already in stock.
- go to /meals/<num> and press "cooked" when done. Stock is updated.
- rinse and repeat.

## Usage
This is just django, so run `pip3 install -r requirements.txt` then run `python3 manage.py runserver`
