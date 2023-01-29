"""Doc."""


def find_department(department_base):  # Поиск отдела в базе отделов
    """Doc."""
    print('База отделов:')
    for key in department_base:
        print(key + ' - ', end='')
        print(*department_base[key], sep='; ', end=';\n')
    print()
    find_key = input('Введите ключ отдела: ')
    # Проверка на корректность ввода
    while find_key not in department_base.keys():
        print('Не корректный ввод!')
        find_key = input('Введите ключ отдела: ')
    return find_key


def find_worker(workers_base):  # Поиск сотрудника в базе сотрудников
    """Doc."""
    print('База сотрудников:')
    for key in workers_base:
        print(key + ' - ', end='')
        print(*workers_base[key], sep='; ', end=';\n')
    print()
    find_key = input('Введите ключ сотрудника: ')
    while find_key not in workers_base.keys():
        print('Не корректный ввод!')
        find_key = input('Введите ключ отдела: ')
    return find_key


def del_department(workers_base: dict, department_base):  # Удаление отдела
    """Doc."""
    edit_key = find_department(department_base)  # Функция поиска отдела
    for key in workers_base:
        if edit_key in workers_base[key][-1]:
            # Удаляем id отдела в базе сотрудников (должности не удалял)
            # раскоментировать для удаления должностей
            # workers_base[key].pop(-2)
            workers_base[key][-1] = 'нет назначения'
    del department_base[edit_key]
    print('Запись отдела удалена.\n')
    return workers_base, department_base


def del_worker(base_workers, base_department):
    """Doc."""
    # Вызов функции поиска сотрудника в базе
    edit_key = find_worker(base_workers)
    for key in base_department:
        if edit_key in base_department[key][2]:
            # Удаляем сотрудника из базы отделов
            base_department[key][2].remove(edit_key)
            # Меняем кол-во сотрудников в отделе
            base_department[key][1] = str(len(base_department[key][2]))
    del base_workers[edit_key]
    print('Сотрудник удален из базы.\n')
    return base_workers, base_department


def edit_department(department_base):  # Редактирование наименования отдела
    """Doc."""
    edit_key = find_department(department_base)  # Вызов функции поиска отдела
    edit_name = input('Введите новое название отдела: ').strip().capitalize()
    department_base[edit_key][0] = edit_name
    print('Отдел переименован.\n')
    return department_base


# Редактирование сотрудников и перевод в другой отдел
def edit_worker(base_workers, base_department):
    """Doc."""
    edit_key = find_worker(base_workers)
    surname = input('Введите фамилию сотрудника: ').strip().capitalize()
    name = input('Введите имя сотрудника: ').strip().capitalize()
    patronymic = input('Введите отчество сотрудника: ').strip().capitalize()
    telephone = input('Введите телефон сотрудника: ').strip()
    address = input('Введите адрес проживания сотрудника: ').strip()
    position = input('Введите должность сотрудника: ').strip()
    print('Выберите отдел из списка и введите ключ, чтобы '
          'создать новый отдел - введите "n".')
    for key in base_department:  # Выводим отделы пользователю
        print(f'{key} - {base_department[key][0]}')
    department = input('Введите отдел: ').strip().lower()

    # Проверка на корректность ввода
    while department not in [el for el in base_department.keys()] + ['n']:
        print('Не корректный ввод!')
        department = input('Введите отдел: ')

    if department == 'n':  # Если пользователь решил создать новый отдел
        base_department = add_department(base_department)
        department = str(len(base_department))

    if department != base_workers[edit_key][-1]:  # Если изменился отдел
        # Удаляем сотрудника из старого отдела в базе отделов
        base_department[base_workers[edit_key][-1]][2].remove(edit_key)
        # Меняем кол-во сотрудников в старом отделе
        base_department[base_workers[edit_key][-1]
                        ][1] = str(
                            len(base_department[base_workers[edit_key][-1]][2])
        )
        # Добавляем сотрудника в новый отдел
        base_department[department][2].append(edit_key)
        # Меняем кол-во сотрудников новом отделе
        base_department[department][1] = str(
            len(base_department[department][2]))
    base_workers[edit_key] = [surname, name, patronymic,
                              telephone, address, position, department]
    print('Запись сотрудника изменена.\n')
    return base_workers, base_department


def add_department(department_base: dict):  # Создание нового отдела
    """Doc."""
    name_department = input('Введите название отдела: ').strip().capitalize()
    department_base[str(len(department_base) + 1)] = [name_department, '', []]
    print('Отдел создан.\n')
    return department_base


def add_worker(base_workers: dict, base_department: dict):
    """Функция добавления работника."""
    surname = input('Введите фамилию сотрудника: ').strip().capitalize()
    name = input('Введите имя сотрудника: ').strip().capitalize()
    patronymic = input('Введите отчество сотрудника: ').strip().capitalize()
    telephone = input('Введите телефон сотрудника: ').strip()
    address = input('Введите адрес проживания сотрудника: ').strip()
    position = input('Введите должность сотрудника: ').strip()

    print('Выберите отдел из списка и введите ключ, '
          'что-бы создать новый отдел - введите "n".')
    for key in base_department:  # Выводим отделы пользователю
        print(f'{key} - {base_department[key][0]}')
    department = input('Введите ключ отдела: ').strip().lower()

    # Проверка на корректность ввода
    while department not in [el for el in base_department.keys()] + ['n']:
        print('Не корректный ввод!')
        department = input('Введите ключ отдела: ').strip().lower()

    if department == 'n':  # Если пользователь решил создать новый отдел
        # Создаем новый отдел, через вызов функции создания
        base_department = add_department(base_department)
        # Получаем ключ созданного отдела
        department = str(len(base_department))

    # Заносим нового сотрудника в базу сотрудников
    base_workers[str(len(base_workers) + 1)] = [surname, name,
                                                patronymic, telephone,
                                                address, position, department]
    # Добавляем id сотрудника в базу отделов
    base_department[department][2].append(str(len(base_workers)))
    # Изменяем количество сотрудников в отделе
    base_department[department][1] = str(len(base_department[department][2]))
    print('Сотрудник внесен в базу.\n')
    return base_workers, base_department
