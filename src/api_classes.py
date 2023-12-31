from abc import ABC, abstractmethod
import json
import requests
import isodate
import datetime
import os
from dotenv import load_dotenv


class ApiWork(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, word):
        """Подключаться к API и получает вакансии"""
        pass


class Saver(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def saver_to_file(self):
        pass

    @abstractmethod
    def sorted_list(self):
        pass

    @abstractmethod
    def delete_item(self, value):
        pass


class HeadHunterApi(ApiWork):
    """
    Класс для работы с Api HeadHunter
    """

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"  # ссылка для работы с Api по поиску и просмотру вакансий
        self.headers = {
            "User-Agent": "User Agent",  # HH requires User-Agent or HH-User-Agen
        }
        self.params = {}

    def get_vacancies(self, word, area=113, period=30):
        print("Сбор данных")
        for page in range(20):
            self.params = {
                "text": word,
                "area": area,  # Specify the desired area ID (1 is Moscow)
                "page": page,
                "per_page": 40,  # Number of vacancies per page
                "period": period,  # дней назад опубликовано
            }
            response = requests.get(self.url, params=self.params, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                vacancies = data.get("items", [])
                for vacancy in vacancies:
                    vacancy_id = vacancy.get("id")
                    vacancy_title = vacancy.get("name")
                    vacancy_url = vacancy.get("alternate_url")
                    company_name = vacancy.get("employer", {}).get("name")
                    published_iso = vacancy.get("published_at")
                    published = isodate.parse_datetime(published_iso)
                    responsibility = vacancy.get('snippet', {}).get('responsibility')
                    try:
                        if vacancy.get("salary", {}).get("from") != None:
                            salary_from = vacancy.get("salary", {}).get("from")
                        else:
                            salary_from = 0
                    except AttributeError:
                        salary_from = 0
                    try:
                        if vacancy.get("salary", {}).get("to") != None:
                            salary_to = vacancy.get("salary", {}).get("to")
                        else:
                            salary_to = 0
                    except AttributeError:
                        salary_to = 0
                    Vacancy(vacancy_id, vacancy_title, vacancy_url, company_name, published, [salary_from, salary_to])
            else:
                print(f"Request failed with status code: {response.status_code}")


class SuperJobApi(ApiWork):
    """
    Класс для работы с Api SuperJob
    """
    load_dotenv()
    api_key = os.getenv('API_KEY_SJ')

    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.headers = {
            'X-Api-App-Id': self.api_key,
        }
        self.payload = {}

    def get_vacancies(self, word, area=1, period=7):
        self.payload = {
            'keyword': word,
            # 'town': area,
            'no_agreement': 1,
            # 'page': None,
            # 'period': period,
        }
        response = requests.get(self.url, headers=self.headers, params=self.payload)
        # response.raise_for_status()
        page_data = response.json()
        vacancies = page_data.get("objects", [])
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id")
            vacancy_title = vacancy.get('profession')
            vacancy_url = vacancy.get("client", {}).get("link")
            company_name = vacancy.get("client", {}).get('title')
            published_from = vacancy.get("date_published")
            published = datetime.datetime.fromtimestamp(published_from)
            salary_from = vacancy.get('payment_from', {})
            salary_to = vacancy.get('payment_to', {})
            Vacancy(vacancy_id, vacancy_title, vacancy_url, company_name, published, [salary_from, salary_to])


class FromFile(ApiWork):
    def get_vacancies(self, word):
        file_name = str(word) + '.json'
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                vacancy_id = item['id_вакансии']
                vacancy_title = item['название вакансии']
                company_name = item['название компании']
                vacancy_url = item['ссылка на вакансию']
                salary_from = item['зарплата от']
                salary_to = item['зарплата до']
                published = item['дата публикации']
                Vacancy(vacancy_id, vacancy_title, vacancy_url, company_name, published, [salary_from, salary_to])


class Vacancy:
    """Класс для работы с вакансиями"""
    all = []

    def __init__(self, vacancy_id, vacancy_title, vacancy_url, company_name, published, salary):
        self.vacancy_id = vacancy_id
        self.vacancy_title = vacancy_title
        self.vacancy_url = vacancy_url
        self.company_name = company_name
        self.published = published
        if salary[1] > salary[0]:
            self.salary_from = salary[0]
            self.salary_to = salary[1]
        else:
            self.salary_to = salary[0]
            self.salary_from = salary[1]
        self.__class__.all.append(self)

    def __repr__(self):
        return (f"id_вакансии: {self.vacancy_id}\nназвание вакансии: {self.vacancy_title}\n"
                f"название компании: {self.company_name}\nссылка на вакансию: {self.vacancy_url}\n"
                f"зарплата от - до: {self.salary_from} - {self.salary_to} руб\n"
                f"дата публикации: {self.published}\n")

    def __len__(self):
        return len(self.all)


class SaverJson(Saver):
    def __init__(self, name, list_of_vacancy):
        self.name = name + '.json'
        self.list_of_vacancy = list_of_vacancy
        self.json_format = []

    def list_format(self):
        for items in self.list_of_vacancy:
            data = {
                'id_вакансии': items.vacancy_id,
                'название вакансии': items.vacancy_title,
                'название компании': items.company_name,
                'ссылка на вакансию': items.vacancy_url,
                'зарплата от': items.salary_from,
                'зарплата до': items.salary_to,
                'дата публикации': items.published
            }
            self.json_format.append(data)

    def saver_to_file(self):
        """Метод для сохранения"""
        with open(self.name, 'w', encoding='utf-8') as file:
            json.dump(self.json_format, file, ensure_ascii=False, indent=4, default=str)

    def sorted_list(self):
        """Метод для сортировки по зарплате как для объекта так и для списка"""
        try:
            sorted_list = sorted(self.list_of_vacancy, key=lambda x: x['зарплата до'], reverse=True)
        except TypeError:
            sorted_list = sorted(self.list_of_vacancy, key=lambda x: x.salary_to, reverse=True)
        return sorted_list

    def delete_item(self, value):
        """
        Удаляет элементы списка если они не соответствуют условиям
        """
        new_list = []
        if value == 0:
            for item in self.list_of_vacancy:
                if item.salary_to != 0:
                    new_list.append(item)
        else:
            for item in self.list_of_vacancy:
                if item.vacancy_id != value:
                    new_list.append(item)
        self.list_of_vacancy = new_list

    def top_5(self):
        """
        Метод возвращает топ 5
        """
        list_sort = self.sorted_list()
        return list_sort[0:5]
