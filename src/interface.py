from src.api_classes import HeadHunterApi


class UserInteraction:
    """
    Класс взаимодействия с пользователем
    """

    def __init__(self, platform=None):
        self.platform = platform

    def interaction(self):
        print("Здравствуйте, данная программа получает информацию о вакансиях с известных платформ в России.\n"
              "сохраняет её в файл и позволит удобно работать с ней (добавлять, фильтровать, удалять).")
        while True:
            user_input = input("Выберете платформу: 1 - HeadHunters\n\t\t\t\t\t2 - SuperJob\n\t\t\t\t\t"
                               "3 - Обе платформы\n\t\t\t\t\t4 - Выход\n>>>")
            if user_input == "1":
                self.platform = "headhunters"
                hh_1 = HeadHunterApi()
                hh_1_word = input("Введите название вакансии\n>>>")
                hh_1.get_vacancies(hh_1_word)
                break
            elif user_input == "2":
                self.platform = "superjobs"
                print("Данный пункт на разработке")
            elif user_input == "3":
                self.platform = ("headhunters", "superjobs",)
                print("Данный пункт на разработке")
            elif user_input == "4":
                print("Молодец")
                break
            else:
                print("Выберете номер соответствующего пункта и нажмите Enter")
