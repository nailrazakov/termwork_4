from src.api_classes import HeadHunterApi, SuperJobApi, Saver, Vacancy


def interaction():
    print("Здравствуйте, данная программа получает информацию о вакансиях с известных платформ в России.\n"
          "сохраняет её в файл и позволит удобно работать с ней (добавлять, фильтровать, удалять).")
    while True:
        user_input_1 = input("Выберете платформу: 1 - HeadHunters\n\t\t\t\t\t2 - SuperJob\n\t\t\t\t\t"
                             "3 - Обе платформы\n\t\t\t\t\t4 - Выход\n>>>")
        if user_input_1 == "1":
            hh_1 = HeadHunterApi()
            hh_1_word = input("Введите название вакансии\n>>>")
            hh_1.get_vacancies(hh_1_word)
            js = Saver(hh_1_word, Vacancy.all)
            for i in range(len(js.list_of_vacancy)):
                print(js.list_of_vacancy[i])
            print(f"Найдено {len(Vacancy.all)} вакансий")
            what_doing(js)
        elif user_input_1 == "2":
            sj_1 = SuperJobApi()
            sj_1_word = input("Введите название вакансии\n>>>")
            sj_1.get_vacancies(sj_1_word)
            js = Saver(sj_1_word, Vacancy.all)
            print(f"Найдено {len(Vacancy.all)} вакансий")
            what_doing(js)
            break
        elif user_input_1 == "3":
            hh_1 = HeadHunterApi()
            sj_1 = SuperJobApi()
            word = input("Введите название вакансии\n>>>")
            sj_1.get_vacancies(word)
            hh_1.get_vacancies(word)
            hs = Saver(word, Vacancy.all)
            what_doing(js)
            break
        elif user_input_1 == "4":
            print("GoodBye")
            break
        else:
            print("Выберете номер соответствующего пункта и нажмите Enter")


def what_doing(class_object):
    while True:
        print("Выберете возможные действия")
        user_input = input(f"\t\t\t\t\t1 - удалить элементы\n\t\t\t\t\t2 - сортировать список\n"
                           f"\t\t\t\t\t3 - сохранить в файл\n\t\t\t\t\t4 - выход\n>>>")
        if user_input == "1":
            print("Выберете режим удаления")
            input_del = input(f"1 - удалить по ID_вакансии(по другим ключам)\n2 - убрать нулевые значения по зарплате\n"
                              "3 - оставить результаты в диапазоне зарплаты\n4 - возврат в предыдущее меню\n>>>")
            while True:
                if input_del == "1":
                    input_del_id = input("Введите id_вакансии\n>>>")
                    class_object.delete_item('id_вакансии', input_del_id)
                    for item in class_object.all:
                        print(item, len(class_object.all))
                    break
                elif input_del == "2":
                    class_object.delete_item()
                    for item in class_object.list_of_vacancy:
                        print(item)
                    print(f"После удаления осталось {len(class_object.list_of_vacancy)}")
                    break
                elif input_del == "3":
                    pass
                elif input_del == "4":
                    break
                else:
                    print("Выберете номер соответствующего пункта и нажмите Enter")
        elif user_input == "2":
            print("Выберете режим сортировки")
            input_sort = input(f"1 - сортировать по зарплате\n2 - сортировать по дате\n"
                               "3 - показать ТОП 5\n4 - возврат в предыдущее меню\n>>>")
            while True:
                if input_sort == "1":
                    for i in range(len(class_object.sorted_list())):
                        print(class_object.sorted_list()[i])
                    break
                elif input_sort == "2":
                    pass
                elif input_sort == "3":
                    class_object.top_5()
                    for i in range(len(class_object.top_5())):
                        print(class_object.top_5()[i])
                    break
                elif input_sort == "4":
                    break
                else:
                    print("Выберете номер соответствующего пункта и нажмите Enter")

        elif user_input == "3":
            print("Сохранение в файл")
            class_object.list_format()
            class_object.saver_to_json()
            break
        elif user_input == "4":
            print("Досвидания!")
            break
        else:
            print("Выберете номер соответствующего пункта и нажмите Enter")
