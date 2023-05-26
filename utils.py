import os
import names
import random
import datetime
import json
output = []
crimes = [{'crime': 'Murder', 'description': 'The act of intentionally killing another person.'}, {'crime': 'Thief', 'description': "A person who steals another person's property."}, {'crime': 'Racist', 'description': 'The act of discriminating or showing prejudice towards people of a certain race.'}, {'crime': 'Burglary', 'description': 'The illegal entry into a building with the intent to commit a crime, usually theft.'}, {'crime': 'Robbery',
                                                                                                                                                                                                                                                                                                                                                                                                                                             'description': "The act of taking someone else's property by force or threat of force."}, {'crime': 'Assault', 'description': 'The intentional act of causing physical harm or injury to another person.'}, {'crime': 'Vandalism', 'description': 'The intentional destruction or damage of property belonging to another person or entity.'}, {'crime': 'Theft', 'description': "The act of taking someone else's property without their permission."}]
countries = ['Afghanistan', 'Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'Egypt', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Iraq', 'Italy', 'Japan', 'Mexico',
             'Nigeria', 'Pakistan', 'Philippines', 'Russia', 'Saudi Arabia', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Thailand', 'Turkey', 'Ukraine', 'United Kingdom', 'United States']


print(names.get_full_name())
for file in os.listdir('./persons'):
    name = names.get_full_name()
    crime = random.choice(crimes)
    crime_name = crime['crime']
    crime_description = crime['description']
    year = random.randint(1900, 2023)
    month = random.randint(1, 11)
    print(year, month)
    days_in_month = (datetime.date(year, month + 1, 1) -
                     datetime.date(year, month, 1)).days
    print(days_in_month)
    day = random.randint(1, 31)
    date = f'{year}-{month}-{day}'
    country = random.choice(countries)
    output.append({
        'name': name,
        'crime': crime_name,
        'description': crime_description,
        'date': date,
        'country': country,
        'image': file
    })


# store the data in a json file
with open('data.json', 'w') as f:
    json.dump(output, f)
