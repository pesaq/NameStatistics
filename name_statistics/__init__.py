import requests
from typing import Dict, Union
from bs4 import BeautifulSoup
from .exc import RequestFailedError, ParseError, IncorrectSearchName
from .utils.user_agent import get_random_user_agent

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
        parser: str = 'lxml'
    ):
        """
        :param language: Язык, на котором будет прилагаться описание (для функций get_forename_description, get_surname_description)
        :param parser Парсер для BeautifulSoup ('lxml', 'html.parser', ...). По умолчанию 'lxml'.
        """
        self.language: str = language
        self.parser: str = parser
        self.base_url: str = 'https://forebears.io'
        self.headers: Dict[str, str] = {
            'User-Agent': get_random_user_agent()
        }
        self.session = requests.Session()
    
    def _make_request(
        self,
        url: str
    ):
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise RequestFailedError(f'Request failed: {str(e)}')

    def _validate_name_slug(self, name_slug: str) -> bool:
        if not name_slug.isalpha():
            raise ValueError("Name slug should contain only letters")

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
        
        if not name_slug.isalpha():
            raise ValueError(
                f"Invalid name_slug '{name_slug}'."
                "Should contain only lowercase letters (a-z) without spaces/special chars"
            )

        if self.language != 'en':
            return f'{self.base_url}/{self.language}/forenames/{name_slug.lower()}'
        return f'{self.base_url}/forenames/{name_slug.lower()}'
    
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

            most_prevalent_title = info_block.find('div', {'class': 'statistic-single'}).text
            count_info_title = info_block.find('p', {'class': 'text-center'}).text
        except AttributeError as e:
            raise IncorrectSearchName(f'Search Failed: {str(e)}')

        return f'Name {name_slug} {most_prevalent_title}\n{count_info_title}'

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

            most_prevalent_country = info_block.find('div', {'class': 'detail'}).text
            count = int(info_block.find('span', {'class': 'accent'}).text.replace(',', ''))
        except AttributeError as e:
            raise IncorrectSearchName(name_slug)

        return {
            'name': name_slug,
            'count-in-world': count,
            'most-prevalent-country': most_prevalent_country
        }