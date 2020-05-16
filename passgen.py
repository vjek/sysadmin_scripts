#!/usr/bin/env python3
import random,sys
# use combination of color, animal, vegetable, mineral, specials, number
# to create some passwords that are reasonably strong
# 20190213 by me. updated 20200320 with more entries in each category
# 20200516 updated to have case changing/randomization
def randomcase(my_str):
    randomcase_str = ''.join(random.choice((str.upper, str.lower))(c) for c in my_str)
    return randomcase_str

specials = ['!','#','^','&','(',')','@','$','%','*','-','_','=','+','{','}','[',']','<','>','/','\\']

colors = ['Aqua','Aquamarine','Azure','Beige','Black','Blue','Brown','Chartreuse',
    'Chocolate','Coral','Crimson','Cyan','Fuchsia','Gold','Gray','Grey','Green',
    'Indigo','Ivory','Khaki','Lavender','Lime','Magenta','Maroon','Navy','Olive',
    'Orange','Orchid','Pink','Plum','Purple','Red','Sienna','Silver','Tan','Teal',
    'Turquoise','Violet','White','Yellow']

animals = ['Bird','Cat','Chicken','Dog','Duck','Fish','Frog','Cow','Hamster',
    'Horse','Mouse','Pig','Rabbit','Sheep','Turtle','Fox','Goat','Squirrel',
    'Monkey','Kangaroo','Giraffe','Panda','Lion','Tiger','Elephant','Snake',
    'Alligator','Koala','Bear','Zebra','Hippo','Rhino','Seal','Whale','Shark',
    'Walrus','Penguin','Octopus','Pangolin','Aardvark','Snail','Crocodile',
    'Badger','Gorilla','Tortoise','Parrot','Crow','Raven','Magpie']

vegetables = ['Beet','Broccoli','Carrot','Celery','Cilantro','Parsley','Radish',
    'Lettuce','Spinach','Apple','Blueberry','Melon','Papaya','Peach','Pear',
    'Pineapple','Plum','Raspberry','Strawberry','Potato','Corn','Lemon',
    'Tangerine','Grapefruit','Eggplant','Cucumber','Cabbage','Pumpkin',
    'Tomato','Asparagus','Garlic','Leek','Onion','Ginger']

minerals = ['Agate','Amber','Amethyst','Azurite','Beryl','Carnelian','Citrine',
    'Diamond','Emerald','Garnet','Jade','Jasper','Obsidian','Onyx','Opal',
    'Peridot','Pyrite','Quartz','Crystal','Ruby','Sapphire','Spinel','Topaz',
    'Zircon','Moonstone','Hematite','Aventurine','Rhodonite','Sunstone',
    'Fluorite','Calcite','Bloodstone','Ammolite','Pearl','Tourmaline']

order = [1,2,3,4,5,6]

count = 4
if sys.argv[1:]:
    count = int(sys.argv[1])

for x in range(0,count):
    random.shuffle(animals)
    random.shuffle(vegetables)
    random.shuffle(minerals)
    random.shuffle(colors)
    random.shuffle(specials)
    random.shuffle(order)
#assignments
    random_animal = randomcase(random.choice(animals))
    random_vegetable = randomcase(random.choice(vegetables))
    random_mineral = randomcase(random.choice(minerals))
    random_color = randomcase(random.choice(colors))
    random_special = random.choice(specials)
    random_digits = random.randint(0, 9999)
#output
    pswd=""
    for y in order:
        if y == 1:
            pswd += random_animal
        if y == 2:
            pswd += random_vegetable
        if y == 3:
            pswd += random_mineral
        if y == 4:
            pswd += random_color
        if y == 5:
            pswd += str('{0:04d}'.format(random_digits))
        if y == 6:
            pswd += random_special
    print(pswd)
