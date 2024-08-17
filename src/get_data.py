import requests

bangalore_coordinates_string : str = '''"Point(77.55273 12.98313)"'''

with open('queries/bangalore_query.sparql', 'r') as f:
    query = f.read()
print(query)

