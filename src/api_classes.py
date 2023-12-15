from abc import ABC, abstractmethod
import json
import requests
import isodate


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
        self.params = {
            "text": word,
            "area": area,  # Specify the desired area ID (1 is Moscow)
            # "page": 20,
            # "per_page": 50,  # Number of vacancies per page
            "period": period,  # дней назад опубликовано
        }
        print("Сбор данных")
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
                    salary_from = vacancy.get("salary", {}).get("from")
                    salary_to = vacancy.get("salary", {}).get("to")
                    currency_s = vacancy.get("salary", {}).get("currency")
                    if currency_s == "RUR":
                        currency = "Руб"
                except AttributeError:
                    salary_from = "Заработная плата"
                    salary_to = "не"
                    currency = "указана"
                #  проверка данных
                Vacancy(vacancy_id, vacancy_title, vacancy_url, company_name, published, [salary_from, salary_to])
                print(f"ID: {vacancy_id}\nTitle: {vacancy_title}\nCompany: {company_name}\nURL: {vacancy_url}\n"
                      f"{salary_from} - {salary_to} {currency}\nопубликовано {published}\n"
                      f"{responsibility}\n")
            print(len(Vacancy.all), Vacancy.all)
        else:
            print(f"Request failed with status code: {response.status_code}")


class SuperJobApi(ApiWork):
    """
    Класс для работы с Api SuperJob
    """

    def get_vacancies(self, word):
        pass


class Vacancy:
    """Класс для работы с вакансиями"""
    all = []

    def __init__(self, vacancy_id, vacancy_title, vacancy_url, company_name, published, salary):
        self.vacancy_id = vacancy_id
        self.vacancy_title = vacancy_title
        self.vacancy_url = vacancy_url
        self.company_name = company_name
        self.published = published
        self.salary = salary

        self.data = {
            'id_вакансии': self.vacancy_id,
            'название вакансии': self.vacancy_title,
            'название компании': self.company_name,
            'ссылка на вакансию': self.vacancy_url,
            'дата публикации': self.published,
            'зарплата': self.salary,
        }
        self.__class__.all.append(self.data)


class ToJson:
    pass

    # with open(filename, 'a', encoding='utf-8') as file:
    # json.dump(data, file, ensure_ascii=False, indent=4)
