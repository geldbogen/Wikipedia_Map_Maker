import requests
import wikitextparser as wtp

place_name = 'leipzig'
url = f'https://en.wikivoyage.org/w/api.php?action=parse&format=json&page={place_name}&prop=sections&disabletoc=1'

response = requests.get(url)
r = response.json()



response_list_sections = r['parse']['sections']
index_to_name_tag_dict = dict()


for index, item in enumerate(response_list_sections):
    print(index)
    print(item)
    


print(index_to_name_tag_dict)
# print(response.text)


# url_2 = 'https://en.wikivoyage.org/w/api.php'
# 'https://en.wikipedia.org/wiki/Special:ApiSandbox#action=parse&format=json&page=house&prop=wikitext&section=3&disabletoc=1'
# response = requests.get(url_2, params={
#                         'action': 'parse', 'format': 'json',
#                          'page': place_name, 'prop': 'wikitext',
#                            'section' : '43', 'disabletoc' : '1' })
# print(response.json()['parse']['wikitext']['*'])
# parsed = wtp.parse(response.json()['parse']['wikitext']['*'])
# print(len(parsed.templates))
# print(parsed.templates[0])
# # for item in parsed.templates:
# #     print(item)
# print(parsed.sections[0].templates)
# print('a')
# for item in parsed.sections:
#     print(item.title)
#     print(len(item.get_sections()))



# print(parsed.sections[2].get_lists())