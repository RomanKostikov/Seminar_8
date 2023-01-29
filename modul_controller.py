"""Doc."""
import modul_user_interface as mui
import modul_working_data as mwd
import modul_log_generate as mlg
import time
import shutil


data_workers = {}
data_departments = {}


def program_start():
    """Doc."""
    mlg.write_log('Начало работы программы: ' +
                  time.strftime('%d.%m.%y %H:%M:%S') + ';')
    global data_workers
    global data_departments
    user_choice = mui.user_choose()  # Получаем выбор пользователя
    if user_choice == '9':  # Если получена команда "9" - выходим из программы
        print('Работа программы завершена')
        mlg.write_log('Завершение работы программы: ' +
                      time.strftime('%d.%m.%y %H:%M:%S') + ';')
        exit()

    # Импортируем базу данных СОТРУДНИКОВ из файла
    with open('data_workes.txt', encoding='utf=8') as dw_file:
        for line in dw_file:
            data_workers[line[0]] = [
                el.rstrip('\n') for el in line[1:].split('*') if len(el) > 0]
    mlg.write_log('База сотрудников выгружена из файла data_workes.txt')
    # Резервная копия базы сотрудников
    shutil.copy('data_workes.txt', 'data_workes_backup.txt')
    mlg.write_log(
        'Резервная копия базы сотрудников сохранена в data_workes_backup.txt')

    # Импортируем базу данных ОТДЕЛОВ из файла
    with open('data_department.txt', encoding='utf=8') as dd_file:
        for line in dd_file:
            data_departments[line[0]] = [
                el.rstrip('\n') for el in line[1:].split('*') if len(el) > 0]
            data_departments[line[0]].append(
                data_departments[line[0]].pop().split('%'))
    mlg.write_log('База отделов выгружена из файла data_department.txt')
    # Резервная копия базы отделов
    shutil.copy('data_department.txt', 'data_department_backup.txt')
    mlg.write_log(
        'Резервная копия базы отделов сохранена в data_department_backup.txt')

    while True:  # Цикл пока не будет задействован elif == "9"

        if user_choice == '1':  # Добавить сотрудника
            data_workers, data_departments = mwd.add_worker(
                data_workers, data_departments)
            mlg.write_log('Запись сотрудника добавлена')

        elif user_choice == '2':  # Добавить отдел
            data_departments = mwd.add_department(data_departments)
            mlg.write_log('Запись отдела добавлена')

        elif user_choice == '3':  # Редактировать сотрудника
            data_workers, data_departments = mwd.edit_worker(
                data_workers, data_departments)
            mlg.write_log('Запись сотрудника отредактирована')

        elif user_choice == '4':  # Редактировать отдел
            data_departments = mwd.edit_department(data_departments)
            mlg.write_log('Запись отдела отредактирована')

        elif user_choice == '5':  # Удалить сотрудника
            data_workers, data_departments = mwd.del_worker(
                data_workers, data_departments)
            mlg.write_log('Запись сотрудника удалена')

        elif user_choice == '6':  # Удалить отдел
            data_workers, data_departments = mwd.del_department(
                data_workers, data_departments)
            mlg.write_log('Запись отдела удалена')

        elif user_choice == '7':  # Вывести в консоль
            print('База сотрудников:')
            for key in data_workers:
                print(key + ' - ', end='')
                print(*data_workers[key], sep='; ', end=';\n')
            print('\nБаза отделов')
            for key in data_departments:
                print(key + ' - ', end='')
                print(*data_departments[key], sep='; ', end=';\n')
            print()
            mlg.write_log('Вывод в консоль выполнен')

        elif user_choice == '8':  # Экспорт
            print('Выберите вариант экспорта:\n'
                  '1. Данные на одной строке;\n'
                  '2. Данные построчно.')
            choice = input('Введите цифру: ')
            while choice not in ('1', '2'):
                print('Не корректный ввод!')
                choice = input('Введите цифру: ')
            if choice == '1':  # Экспорт по 1 правилу
                with open('export_1.csv', 'w', encoding='utf=8') as export_1:
                    export_1.write('База сотрудников:\n\n')
                    for key_base in data_workers:
                        export_1.write(
                            '; '.join(data_workers[key_base]) + '\n')
                    export_1.write('\n\n')
                    export_1.write('База отделов:\n\n')
                    for key_base in data_departments:
                        export_1.write(
                            '; '.join(
                                el if type(el) != list else '; '.join(el)
                                for el in data_departments[key_base]
                            ) + '\n'
                        )
                    export_1.write('\n')
                print('Экспорт по 1 правилу завершен.\n')
                mlg.write_log(
                    'Экспорт по 1 правилу выполнен, данные сохранены в файл '
                    'export_1.csv')
            elif choice == '2':  # Экспорт по 2 правилу
                with open('export_2.csv', 'w', encoding='utf=8') as export_2:
                    export_2.write('База сотрудников:\n\n')
                    for key_base in data_workers:
                        export_2.write(';\n'.join(
                            data_workers[key_base]) + '\n')
                        export_2.write('\n')
                    export_2.write('\n\n')
                    export_2.write('База отделов:\n\n')
                    for key_base in data_departments:
                        export_2.write(
                            ';\n'.join(
                                el if type(el) != list else ';\n'.join(el)
                                for el in data_departments[key_base]
                            ) + '\n'
                        )
                        export_2.write('\n')
                    export_2.write('\n')
                print('Экспорт по 2 правилу завершен.\n')
                mlg.write_log('Экспорт по 2 правилу выполнен, '
                              'данные сохранены в файл export_2.csv')

        elif user_choice == '9':  # Выход
            # Сохраняем базу СОТРУДНИКОВ в файл
            with open('data_workes.txt', 'w', encoding='utf=8') as file_w:
                for key in data_workers:
                    file_w.write(str(key) + '*' +
                                 '*'.join(data_workers[key]) + '\n')
            mlg.write_log('База сотрудников сохранена в файл data_workes.txt')
            # Сохраняем базу ОТДЕЛОВ в файл
            with open('data_department.txt', 'w', encoding='utf=8') as file_d:
                for key in data_departments:
                    file_d.write(str(key) + '*' + '*'.join
                                 (
                        el if type(el) != list else '%'.join(el)
                        for el in data_departments[key]
                    ) + '\n')
            mlg.write_log('База отделов сохранена в файл data_department.txt')
            print('Работа программы завершена!')
            mlg.write_log('Завершение работы программы: ' +
                          time.strftime('%d.%m.%y %H:%M:%S') + ';')
            exit()
        user_choice = mui.user_choose()
