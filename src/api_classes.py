from abc import ABC, abstractmethod
import json
import requests
import isodate
import datetime


class ApiWork(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, word):
        """Подключаться к API и получает вакансии"""
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
        for page in range(5):
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
    api_key = 'v3.r.138018641.3c02e4f5c8465896c09352c8162e18be30844f2b.c115a86975848929a4b26ce62e07ee3c85d686c8'

    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.headers = {
            'X-Api-App-Id': self.api_key,
        }
        self.payload = {}

    def get_vacancies(self, word, area=1, period=30):
        payload = {
            'keyword': word,
            'town': area,
            'no_agreement': 1,
            'page': 0,
            'period': period,
        }
        response = requests.get(self.url, headers=self.headers, params=self.payload)
        print(response)
        response.raise_for_status()
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


class Vacancy:
    """Класс для работы с вакансиями"""
    all = []
    all_json = []

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

        self.data = {
            'id_вакансии': self.vacancy_id,
            'название вакансии': self.vacancy_title,
            'название компании': self.company_name,
            'ссылка на вакансию': self.vacancy_url,
            'дата публикации': self.published,
            'зарплата от': self.salary_from,
            'зарплата до': self.salary_to
        }
        self.__class__.all.append(self)
        self.__class__.all_json.append(self.data)

    def __repr__(self):
        return (f"ID: {self.vacancy_id}\nTitle: {self.vacancy_title}\nCompany: {self.company_name}\n"
                f"URL: {self.vacancy_url}\nSalary: {self.salary_from} - {self.salary_to} руб\n"
                f"Опубликовано {self.published}\n")

    def __len__(self):
        return len(self.all)


class Saver:
    def __init__(self, name, list_of_vacancy):
        self.name = name + '.json'
        self.list_of_vacancy = list_of_vacancy

    def saver_to_json(self):
        with open(self.name, 'a', encoding='utf-8') as file:
            json.dump(self.list_of_vacancy, file, ensure_ascii=False, indent=4, default=str)

    def sorted_list(self):
        """Метод для сортировки"""
        try:
            sorted_list = sorted(self.list_of_vacancy, key=lambda x: x['зарплата до'], reverse=True)
        except TypeError:
            sorted_list = sorted(self.list_of_vacancy, key=lambda x: x.salary_to, reverse=True)
        return sorted_list

    def delete_item(self, key):
        pass

    def top_n(self, n):
        list_sort = self.sorted_list()
        return list_sort[0:n]
