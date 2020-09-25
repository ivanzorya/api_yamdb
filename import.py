import csv
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from api.models import Category, Genre

data_mapping = {
    'data/category.csv': Category,
    'data/genre.csv': Genre,
}
for i in data_mapping:
    with open(i, 'r', encoding="utf-8", newline='') as csvfile:
        filedata = csv.reader(csvfile, delimiter=',')
        for row in filedata:
            data_to_model = data_mapping[i](
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            try:
                data_to_model.save()
            except:
                print('something wrong with row', row)
