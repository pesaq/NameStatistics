# Name Statistics

Проект для получения статистики по именам с сайта [forebears.io](https://forebears.io).

## Возможности

- Получение статистики по заданному имени:
  - Общее количество людей с этим именем в мире
  - Страна, где имя наиболее распространено
- Получение описательной информации об имени
- Поддержка разных языков для описания

## Установка

1. Python 3.7+
2. Зависимости:
   ```bash
   pip install -r requirements.txt

## Использование
```
from name_statistics import NameStatistics
```

# Инициализация (язык по умолчанию - английский)
```
ns = NameStatistics(language='ru')  # 'ru', 'it', 'de', 'es', и тд
```

# Получение статистики по имени
```
from name_statistics import NameStatistics

ns = NameStatistics(language='ru', parser='lxml')

stats = ns.get_forename_stats('maksim')
print(stats) # {'name': 'maksim', 'count-in-world': 123456, 'most-prevalent-country': 'Russia'}

description = ns.get_forename_description('maksim')
print(description)
```

# Использование кириллицы
```
ns = NameStatistics(auto_slug_cyrillic=True) # автоматическое преобразование кириллицы в slug

search_result = ns.get_forename_description('Максим') # входные данные на кириллице
print(search_result)
```