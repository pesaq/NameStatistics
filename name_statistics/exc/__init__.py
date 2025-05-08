class NameStatisticsError(Exception):
    """Базовое исключение для библиотеки"""
    pass

class IncorrectSearchName(Exception):
    def __init__(self, name_slug: str):
        super().__init__(f'Name "{name_slug}" not found or invalid')
        self.name_slug = name_slug

class RequestFailedError(NameStatisticsError):
    """Возникает при сбое HTTP-запроса"""
    pass

class ParseError(NameStatisticsError):
    """Возникает при неудачном парсинге"""
    pass