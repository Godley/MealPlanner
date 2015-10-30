from nltk import word_tokenize, pos_tag
from inflect import engine
from bs4 import BeautifulSoup
import sqlite3

db = sqlite3.connect('/Users/charlottegodley/PycharmProjects/MealPlanner/DjangoMeals/db.sqlite3')
query = 'SELECT original FROM meals_stock_recipes as m WHERE NOT EXISTS (SELECT * FROM meals_stock_recipes WHERE m.stock_id = stock_id AND m.id <> id)'
cursor = db.cursor()
cursor.execute(query)
dataset = cursor.fetchall()

def parse_stock_name(stockname):
        p = engine()
        souped = BeautifulSoup(stockname, "lxml")
        stock = souped.get_text()
        instruction_set = stock.split(',')
        word_list = instruction_set[0].split(' ')
        index = 0
        categories_ignored = ['RB', 'TO', 'CD', 'IN']
        tokens = word_tokenize(instruction_set[0])
        tags = pos_tag(tokens)
        i=0
        while i < len(tags):
            if tags[i][1] in categories_ignored or tags[i] == 'tbsp' or tags[i] == 'x':
                index += 1
                i+= 1
            else:
                break

        quantity = '0'
        disallowed = ['g', 'ml', 'x', 'kg', 'cups', 'cup', 'grams', 'can', 'tbsp', 'tsp', 'tbsps', 'tsps',
                 'small', 'bunch', 'piece', 'handful', 'pack', 'chopped', 'large', 'a', 'pinch',
                 'fresh', 'dried', 'heaped', 'thick', 'slices', 'slice', 'of', 'about']
        while index < len(word_list):
            if word_list[index] not in disallowed:
                break
            else:
                index+=1
        sentence = " ".join(word_list[index:])
        tokens = word_tokenize(sentence)
        categories = pos_tag(tokens)
        words = []
        for category in categories:
            if category[1] == 'NNS':
                words.append(p.singular_noun(category[0]))
            else:
                words.append(category[0])
        word = " ".join(words)
        return quantity, word, None


sentences = ['3 garlic cloves, crushed', '2 rosemary sprigs, leaves picked and chopped',
                '1 tsp black peppercorns, crushed', '3 juniper berries, crushed',
                'about 1 tbsp olive oil', '1 whole leg of lamb about 3kg', '250ml white wine',
             '3 x 200g/7oz white chocolate bars, chopped', '200g butter', '2 eggs',
             '100g light muscovado sugar', '175g golden caster sugar', '2 tsp vanilla extract',
             '350g plain flour', '2 tsp baking powder', '1 tsp cinnamon', '100g macadamia nuts, chopped',
             '100g dried cranberries']

for sentence in sentences:
    quantity, name, direction = parse_stock_name(sentence)
    print(name)

