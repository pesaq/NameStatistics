from name_statistics import NameStatistics

ns = NameStatistics(language='ru', auto_slug_cyrillic=True)

search_result = ns.get_forename_description('Илья')
print(search_result)