import csv
import os

import django
from django.shortcuts import get_object_or_404

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from api.models import Category, Genre, Title

# data_mapping = {
#     'data/category.csv': Category,
#     'data/genre.csv': Genre,
# }
# for i in data_mapping:
#     with open(i, 'r', encoding="utf-8", newline='') as csvfile:
#         filedata = csv.reader(csvfile, delimiter=',')
#         for row in filedata:
#             data_to_model = data_mapping[i](
#                 id=row[0],
#                 name=row[1],
#                 slug=row[2],
#             )
#             try:
#                 data_to_model.save()
#             except:
#                 print('something wrong with row', row)
with open('data/titles.csv', 'r', encoding="utf-8", newline='') as csvfile:
    filedata = csv.reader(csvfile, delimiter=',')
    for row in filedata:
        data_to_model = Title(
            id=row[0],
            name=row[1],
            year=row[2],
            category=get_object_or_404(Category, id=row[3])
        )
        data_to_model.save()

