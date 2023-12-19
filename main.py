# Напишите программу, которая будет получать информацию о вакансиях с разных платформ в России,
# сохранять ее в файл и позволять удобно работать с ней (добавлять, фильтровать, удалять).
from src.interface import interaction, what_doing
if __name__ == '__main__':
    interaction()


# Реализовать классы, наследующиеся от абстрактного класса, для работы с конкретными платформами.
# Классы должны уметь подключаться к API и получать вакансии.
# Создать класс для работы с вакансиями. В этом классе самостоятельно определить атрибуты,
# такие как название вакансии, ссылка на вакансию, зарплата, краткое описание или требования и т. п. (не менее четырех).
# Класс должен поддерживать методы сравнения вакансий между собой по зарплате и валидировать данные,
# которыми инициализируются его атрибуты.
# Определить абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
# получения данных из файла по указанным критериям и удаления информации о вакансиях.
# Создать класс для сохранения информации о вакансиях в JSON-файл. Дополнительно (по желанию) можно реализовать классы
# для работы с другими форматами, например с CSV-, Excel- или TXT-файлом.
# Создать функцию для взаимодействия с пользователем. Функция должна взаимодействовать с пользователем через консоль.
# Самостоятельно придумать сценарии и возможности взаимодействия с пользователем.
# Например, позволять пользователю указывать, с каких платформ он хочет получить вакансии, ввести поисковый запрос,
# получить топ-N вакансий по зарплате, получить вакансии в отсортированном виде, получить вакансии,
# в описании которых есть определенные ключевые слова, например postgres, и т. п.
# Объединить все классы и функции в единую программу.
