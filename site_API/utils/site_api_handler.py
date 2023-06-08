import logging
from datetime import datetime
from typing import Dict, Union, List

import requests

site_api_handler_logger = logging.getLogger(__name__)


def _get_response(url: str, headers: Dict,
                  *, params: Dict = None, timeout: int = 10) -> Union[Dict, int]:
    """
    Отправляет HTTP-запрос и возвращает ответ в формате JSON, если ответ успешный (статус код 200),
    в противном случае возвращает статус код.

    :param method: HTTP метод запроса (GET, POST, PUT, DELETE и т.д.).
    :param url: URL-адрес, по которому будет отправлен запрос.
    :param headers: Заголовки запроса в виде словаря.
    :param params: Дополнительные параметры запроса, передаваемые в URL-строке.
            По умолчанию None.
    :param timeout: Время ожидания ответа от сервера в секундах.
            По умолчанию 10.
    :return: Возвращает словарь, полученный из ответа в формате JSON, если ответ успешный
            (статус код 200), в противном случае возвращает статус код.
    """
    try:
        site_api_handler_logger.debug(f'Trying to access {url}')
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        status_code = response.status_code

        if status_code == requests.codes.ok:
            site_api_handler_logger.debug(f'Request succeed')
            return response.json()
        else:
            site_api_handler_logger.info(f'Request failed')
            site_api_handler_logger.error(f'Request failed with status code: {status_code}')
            return status_code
    except requests.exceptions.RequestException as e:
        site_api_handler_logger.exception(e)


def _get_genres_list(url: str, headers: Dict) -> Union[Dict, int]:
    """
    Получает список жанров фильмов с API сервера по заданному URL.
    :param url: URL-адрес сервера, на котором расположено API.
    :param headers: Заголовки запроса в виде словаря.
    :return: Возвращает словарь, содержащий список жанров, если ответ успешный (статус код 200),
            в противном случае возвращает статус код.
    """
    url = f'{url}/titles/utils/genres'
    response = _get_response(url, headers)
    return response


def _get_movies(url: str, headers: Dict, genre: Union[str, None], *, sort: str = 'decr', limit: int = 10,
                start_year: int = None,
                end_year: int = None) -> Union[Dict, int]:
    """
    Получает список фильмов с API сервера по заданным параметрам.
    :param url: URL-адрес сервера, на котором расположено API.
    :param headers: Заголовки запроса в виде словаря.
    :param genre: Жанр фильмов, по которому будет выполнен поиск.
    :param sort: Способ сортировки результата. По умолчанию 'decr' - по убыванию года выпуска.
    :param limit: Максимальное количество результатов поиска. По умолчанию 10.
    :param start_year: Год выпуска фильма, начиная с которого нужно выполнить поиск. По умолчанию None.
    :param end_year: Год выпуска фильма, заканчивая которым нужно выполнить поиск. По умолчанию None.
    :return: Возвращает словарь, содержащий список фильмов, если ответ успешный (статус код 200),
        в противном случае возвращает статус код.
    """
    url = f'{url}/titles'
    querystring = {
        'titleType': 'movie',
        'genre': genre,
        'list': 'top_rated_250',
        'sort': f'year.{sort}',
        'limit': limit,
        'endYear': end_year,
        'startYear': start_year
    }
    response = _get_response(url, headers, params=querystring)
    return response


def _get_movies_info(response: Dict) -> List[Dict[str, str]]:
    """
    Обрабатывает ответ от сервера, полученный из функции _get_movies,
    и возвращает список словарей с отфильтрованными данными.
    :param response: Ответ от сервера с информацией о фильмах в виде словаря.
    :return: Список словарей с данными о фильмах.
    """
    results = []
    if response['results']:
        for movie in response['results']:
            movie_info = {}
            try:
                movie_info['image_caption'] = movie['primaryImage']['caption']['plainText']
            except (KeyError, TypeError):
                movie_info['image_caption'] = 'Info is absent'
            try:
                movie_info['image_url'] = movie['primaryImage']['url']
            except (KeyError, TypeError):
                movie_info['image_url'] = 'Info is absent'
            try:
                movie_info['release_date'] = datetime(year=movie['releaseDate']['year'],
                                                      month=movie['releaseDate']['month'],
                                                      day=movie['releaseDate']['day']).strftime('%d %b %Y')
            except (KeyError, TypeError):
                movie_info['release_date'] = 'Info is absent'
            try:
                movie_info['title'] = movie['titleText']['text']
            except (KeyError, TypeError):
                movie_info['title'] = 'Info is absent'
            try:
                movie_info['position'] = movie['position']
            except (KeyError, TypeError):
                movie_info['position'] = 'Info is absent'
            results.append(movie_info)
    return results


class SiteApiInterface:
    """Класс для взаимодействия с API сайта."""

    def __init__(self, url: str, headers: Dict) -> None:
        self.url = url
        self.headers = headers

    def get_genres_list(self) -> Union[List, int]:
        """
        Получить список жанров фильмов.
        :return: список жанров
        """
        site_api_handler_logger.info('Getting genres list')
        response = _get_genres_list(self.url, self.headers)
        if isinstance(response, dict):
            results = ['All'] + response['results'][1:]
            site_api_handler_logger.debug('Genres list got successfully')
            return results
        return response

    def get_movies_low(self, genre: Union[str, None], limit: int) -> Union[List, int]:
        """
        Получить список фильмов отсортированных по возрастанию года выпуска фильма.

        :param genre: жанр фильмов
        :param limit: максимальное количество фильмов

        :return: список фильмов
        """
        response = _get_movies(self.url, self.headers, genre, sort='incr', limit=limit)
        if isinstance(response, dict):
            results = _get_movies_info(response)
            site_api_handler_logger.debug('Movies low got successfully')
            return results
        return response

    def get_movies_high(self, genre: Union[str, None], limit: int) -> Union[List, int]:
        """
        Получить список фильмов отсортированных по убыванию года выпуска фильма.

        :param genre: жанр фильмов
        :param limit: максимальное количество фильмов

        :return: список фильмов
        """
        response = _get_movies(self.url, self.headers, genre, limit=limit)
        if isinstance(response, dict):
            results = _get_movies_info(response)
            site_api_handler_logger.debug('Movies high got successfully')
            return results
        return response

    def get_movies_custom(self, genre: Union[str, None], limit: int, start_year: int = None,
                          end_year: int = None) -> Union[List, int]:
        """
        Получить список фильмов с пользовательскими параметрами диапазона года выпуска.

        :param genre: жанр фильмов
        :param limit: максимальное количество фильмов
        :param start_year: начальный год выпуска фильмов
        :param end_year: конечный год выпуска фильмов
        :return: список фильмов
        """
        response = _get_movies(self.url, self.headers, genre=genre, limit=limit, start_year=start_year,
                               end_year=end_year)
        if isinstance(response, dict):
            results = _get_movies_info(response)
            site_api_handler_logger.debug('Movies custom got successfully')
            return results
        return response
