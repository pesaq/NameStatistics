from name_statistics import NameStatistics

ns = NameStatistics(language='ru', auto_slug_cyrillic=True)

stats = ns.get_forename_stats('Максим')
print(stats)

search_result = ns.get_forename_description('Максим')
print(search_result)