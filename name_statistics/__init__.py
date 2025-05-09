import requests
from typing import Dict, Union
from bs4 import BeautifulSoup
from .exc import RequestFailedError, ParseError, IncorrectSearchName
from .utils.user_agent import get_random_user_agent
from .utils.slugify import slugify_rus_to_eng

class NameStatistics:
    """
    Класс для получения статистики по именам с https://forebears.io

    Позволяет получить:
    - Общее количество людей с заданным именем в мире
    - Страну, где имя наиболее распространено
    """
    def __init__(
        self,
        language: str = 'en',
        parser: str = 'lxml',
        auto_slug_cyrillic: bool = False
    ) -> None:
        """
        :param language: Язык, на котором будет прилагаться описание (для функций get_forename_description, get_surname_description)
        :param parser: Парсер для BeautifulSoup ('lxml', 'html.parser', ...). По умолчанию 'lxml'.
        :param auto_slug: Укажите True для автоматического преобразования имени с кириллицы на slug под формат forebears.io. Например, переданное имя "Ярослав" будет переведено в "yaroslav"
        """
        self.language: str = language
        self.parser: str = parser
        self.auto_slug_cyrillic: bool = auto_slug_cyrillic
        self._base_url: str = 'https://forebears.io'
        self._headers: Dict[str, str] = {
            'User-Agent': get_random_user_agent()
        }
        self.session = requests.Session()
    
    def _make_request(
        self,
        url: str
    ) -> str:
        """Возвращает содержимое страницы с информацией по имени"""
        try:
            response = self.session.get(url, headers=self._headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise RequestFailedError(f'Request failed: {str(e)}')

    def _validate_name_slug(
        self,
        name_slug: str
    ) -> bool:
        """Проверка name_slug на корректность"""
        if not name_slug.isalpha():
            return False
        return True

    def _parse_html(
        self,
        content: str
    ) -> BeautifulSoup:
        try:
            return BeautifulSoup(content, 'lxml')
        except Exception as e:
            raise ParseError(f'HTML parsing failed: {str(e)}')

    def _build_url(
        self,
        name_slug: str
    ) -> str:
        """Возвращает url адрес на страницу с информацией по имени"""

        if not self._validate_name_slug(name_slug):
            raise ValueError(
                f"Invalid name_slug '{name_slug}'."
                "Should contain only lowercase letters (a-z) without spaces/special chars"
            )
    
        if self.auto_slug_cyrillic:
            name_slug = slugify_rus_to_eng(name_slug)

        if self.language != 'en':
            return f'{self._base_url}/{self.language}/forenames/{name_slug.lower()}'
        return f'{self._base_url}/forenames/{name_slug.lower()}'
    
    def get_forename_description(
        self,
        name_slug: str
    ) -> str:
        """
        Возвращает строку с информацией по имени на выбранном языке (self.language)

        :param name_slug: slug имени, для которого применяется функция (т.е "Максим" -> "maksim")
        """

        url = self._build_url(name_slug)
        content = self._make_request(url)
        soup = self._parse_html(content)

        try:
            info_block = soup.find('div', {'class': 'content-box-content medium-text tablet-slim'})
            info_block2 = soup.find('div', {'class': 'content-box-content tablet-slim'})
            statistic_title, statistic_subtitle = soup.find('div', {'class': 'statistic-title'}).text, soup.find('div', {'class': 'statistic-subtitle'}).text

            most_prevalent_title = info_block.find('div', {'class': 'statistic-single'}).text
            most_сommon_name_in_the_world_title = info_block2.find('div', {'class': 'statistic-number'}).text
            count_info_title = info_block.find('p', {'class': 'text-center'}).text
        except AttributeError as e:
            raise IncorrectSearchName(f'Search Failed: {str(e)}')

        return f'{name_slug}\n{most_prevalent_title}\n{count_info_title}\n{most_сommon_name_in_the_world_title} {statistic_title} {statistic_subtitle}'

    def get_forename_stats(
        self,
        name_slug: str
    ) -> Dict[str, Union[str, int]]:
        """
        Возвращает словарь с информацией по имени
        
        :param name_slug: slug имени, для которого применяется функция (т.е "Максим" -> "maksim")
        """

        url = self._build_url(name_slug)
        content = self._make_request(url)
        soup = self._parse_html(content)

        try:
            info_block = soup.find('div', {'class': 'content-box-content medium-text tablet-slim'})
            info_block2 = soup.find('div', {'class': 'content-box-content tablet-slim'})

            most_prevalent_country = info_block.find('div', {'class': 'detail'}).text
            most_сommon_name_in_the_world = int(info_block2.find('div', {'class': 'statistic-number'}).text.replace(',', ''))
            count = int(info_block.find('span', {'class': 'accent'}).text.replace(',', ''))
        except AttributeError as e:
            raise IncorrectSearchName(name_slug)

        return {
            'name': name_slug,
            'count-in-world': count,
            'most-prevalent-country': most_prevalent_country,
            'most-сommon-name-in-the-world': most_сommon_name_in_the_world
        }