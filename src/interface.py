from src.api_classes import HeadHunterApi, SuperJobApi, Saver, Vacancy


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
                print(f"Найдено {len(Vacancy.all)} вакансий")
                js = Saver(hh_1_word, Vacancy.all)
                while True:
                    user_input_1 = input("Выберете дальнейшие действия: \n1 - показать результаты\n"
                                         "2 - показать топ 5 по зарплате\n3 - показать отсортированный список\n"
                                         "4 - записать в файл\n5 - удалить вакансию\n>>>")
                    if user_input_1 == '1':
                        for i in range(len(js.list_of_vacancy)):
                            print(js.list_of_vacancy[i])
                    elif user_input_1 == '2':
                        for i in range(len(js.top_n(5))):
                            print(js.top_n(5)[i])
                    elif user_input_1 == '3':
                        for i in range(len(js.sorted_list())):
                            print(js.sorted_list()[i])
                    elif user_input_1 == '4':
                        js.saver_to_json()
                        break
                    elif user_input_1 == '5':
                        print("Данный пункт в разработке")
                    else:
                        print("Введите ответ")
                break
            elif user_input == "2":
                self.platform = "superjobs"
                sj_1 = SuperJobApi()
                sj_1_word = input("Введите название вакансии\n>>>")
                sj_1.get_vacancies(sj_1_word)
                js = Saver(sj_1_word, Vacancy.all)

                break
            elif user_input == "3":
                self.platform = ("headhunters", "superjobs",)
                hh_1 = HeadHunterApi()
                sj_1 = SuperJobApi()
                word = input("Введите название вакансии\n>>>")
                sj_1.get_vacancies(word)
                hh_1.get_vacancies(word)
                hs = Saver(word, Vacancy.all)
                hs.top_n()
                break
            elif user_input == "4":
                print("GoodBye")
                break
            else:
                print("Выберете номер соответствующего пункта и нажмите Enter")
