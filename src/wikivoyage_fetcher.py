import requests
import wikitextparser as wtp


place_name = 'leipzig'
url = f'https://en.wikivoyage.org/w/api.php?action=parse&format=json&page={place_name}&prop=sections&disabletoc=1'

response = requests.get(url)
r = response.json()


naive_number_to_tag_dict = dict()
number_to_index_dict = dict()

response_list_sections = r['parse']['sections']
index_to_name_tag_dict = dict()


number_to_whole_item_dict = dict()
for index, item in enumerate(response_list_sections):
    number_to_whole_item_dict[item['number']] = item

for list_index,item in enumerate(response_list_sections):
    number : str = item['number']
    while '.' in number:
        to_add_number = (number.rsplit('.',1))[0]
        to_add_string = number_to_whole_item_dict[to_add_number]['line']
        response_list_sections[list_index]['line'] = to_add_string + response_list_sections[list_index]['line']
        number = to_add_number

print([x['line'] for x in response_list_sections])


    


print(index_to_name_tag_dict)
# print(response.text)


url_2 = 'https://en.wikivoyage.org/w/api.php'
'https://en.wikipedia.org/wiki/Special:ApiSandbox#action=parse&format=json&page=house&prop=wikitext&section=3&disabletoc=1'
response = requests.get(url_2, params={
                        'action': 'parse', 'format': 'json',
                         'page': place_name, 'prop': 'wikitext',
                           'section' : '33', 'disabletoc' : '1' })
# print(response.json()['parse']['wikitext']['*'])
parsed = wtp.parse(response.json()['parse']['wikitext']['*'])
print(parsed.get_lists()[0])
# print(len(parsed.templates))
# print(parsed.templates[0])
# # for item in parsed.templates:
# #     print(item)
# print(parsed.sections[0].templates)
# print('a')
# for item in parsed.sections:
#     print(item.title)
#     print(len(item.get_lists()))



# print(parsed.sections[2].get_lists())