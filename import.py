import csv
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from api.models import Category

with open('data/category.csv', 'r', encoding="utf-8", newline='') as csvfile:
    filedata = csv.reader(csvfile, delimiter=',')
    for row in filedata:
        category = Category(
            id=row[0],
            name=row[1],
            slug=row[2],
        )
        try:
            category.save()
        except:
            print('something wrong with row', row)
