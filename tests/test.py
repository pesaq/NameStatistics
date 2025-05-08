from name_statistics import NameStatistics

ns = NameStatistics(language='ru', parser='lxml')

search_result = ns.get_forename_stats('maksim')
print(search_result)