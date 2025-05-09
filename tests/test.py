from name_statistics import NameStatistics

ns = NameStatistics(language='ru')

search_result = ns.get_forename_stats('maksim')
print(search_result)