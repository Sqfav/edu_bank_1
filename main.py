from datetime import datetime  # для получения инфо о текущем годе
import json  # для хранения информации об аккаунте в файле
from functions import (password_checked, numbers_only, can_topup,
                       acc_write_file, acc_load_file, transaction_walker)

acc_path = 'account.txt'

list_of_operations = '''
Выберите операцию:
1 - создать аккаунт
2 - положить деньги на счет
3 - снять деньги
4 - вывести баланс на экран
5 - установить макс.лимит по счету
6 - добавить транзакцию (ожид. пополнение)
7 - применить ожид. транзакции
8 - статистика ожид. транзакций
9 - фильтр транзакций
10 - выйти из программы
'''

# для проверки существования аккаунта, отсутствие баланса == аккаунт еще не создан
acc_dict = {
    'balance': None
}

print('*** Банк "ВЕСЕЛЫЙ ПИТОН" ***')

while True:  # стартовое меню
    print('1 - Загрузить базу из файла', '2 - Начать сначала', sep='\n')
    start = input('Введите код операции: ')
    if start == '1':
        try:
            acc_dict = acc_load_file(acc_path)
            if password_checked(acc_dict.get('password')):
                print('\n', 'Пароль принят, приступаем!', sep='')
                break
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            n = input('Отсутствует или повреждена база данных. 0 для завершения, любой ввод для продолжения: ')
            if n == '0':
                exit()
            break

    elif start == '2':
        break
    else:
        print('\n', 'Введите корректный код', sep='')

while True:  # основное меню
    print(list_of_operations)
    operation = input('Введите код операции: ')
    if operation == '1':
        acc_dict = {
            'full_name': input('Введите ФИО: '),
            'birth_year': numbers_only(input('Введите год рождения: ')),
            'password': input('Введите пароль: '),
            'balance': 0,
            'limit': None,
            'transactions': []
        }

        acc_write_file(acc_path, acc_dict)

        print(f"Создан аккаунт: {acc_dict.get('full_name')} Возраст: {datetime.now().year - acc_dict.get('birth_year')}")
        input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation in '2, 3, 4, 5, 6, 7, 8, 9' and acc_dict.get('balance') is None:
        print('Пожалуйста, сперва создайте аккаунт!')
        input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '2':  # пополнение
        amount = numbers_only(input('Введите сумму пополнения или 0 для нулевой операции и возврата: '))
        if can_topup(amount, acc_dict.get('balance'), acc_dict.get('limit')):
            acc_dict['balance'] += amount

            acc_write_file(acc_path, acc_dict)

            print('Счет успешно пополнен. Ваш баланс:', acc_dict.get('balance'))
        else:
            print('Будет превышен максимальный лимит, пополнение невозможно')
        input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '3':  # снятие
        if password_checked(acc_dict.get('password')):
            withdraw = numbers_only(input('Введите сумму списания или 0 для нулевой операции и возврата: '))
            while acc_dict.get('balance') < withdraw:
                print('Списание превышает доступный остаток. Ваш баланс:', acc_dict.get('balance'))
                withdraw = numbers_only(input('Введите сумму списания или 0 для нулевого снятия и возврата: '))
            else:
                acc_dict['balance'] -= withdraw

                acc_write_file(acc_path, acc_dict)

                print('Списание успешно проведено, ваш баланс:', acc_dict.get('balance'))
                input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '4':  # баланс
        if password_checked(acc_dict.get('password')):
            print('Ваш баланс:', acc_dict.get('balance'))
            input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '5':  # лимит по счету
        if password_checked(acc_dict.get('password')):
            print('Текущий лимит:', acc_dict.get('limit'))
            limit = numbers_only(input('Введите значение лимита (либо 0 для возврата, 1 для сброса лимита: '))
            if limit == 0:
                continue
            elif limit == 1:
                acc_dict['limit'] = None
            else:
                acc_dict['limit'] = limit

            acc_write_file(acc_path, acc_dict)

            print(f"Установлен лимит: {acc_dict.get('limit')} Баланс: {acc_dict.get('balance')}")
            input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '6':  # добавить транзакцию
        new_transaction = {
            'value': numbers_only(input('Сумма будущего пополнения: ')),
            'comment': input('Комментарий: '),
            'applied': False
        }
        acc_dict['transactions'].append(new_transaction)

        # add_trans(new_transaction)
        acc_write_file(acc_path, acc_dict)  # аналог строки выше, но для полной перезаписи файла

        print(f"Добавлена транзакиция: Сумма: {new_transaction.get('value')} Назначение: {new_transaction.get('comment')}")
        print('Количество пополнений в очереди:',
              sum(1 for t in acc_dict.get('transactions') if t.get('applied') is False))
        input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '7':  # применить транзакции
        print('Попытка применения транзакций: ')
        if len(acc_dict.get('transactions')) == 0:
            print('Ожидающие транзакции отсутствуют')
        else:
            for transaction in acc_dict.get('transactions'):
                not_applied = transaction.get('applied') is False
                if can_topup(transaction.get('value'), acc_dict.get('balance'), acc_dict.get('limit')) and not_applied:
                    acc_dict['balance'] += transaction.get('value')
                    transaction['applied'] = True

                    acc_write_file(acc_path, acc_dict)

                    print(f'Транзакция "{transaction.get("comment")}" на сумму {transaction.get("value")} успешно применена')

                elif not_applied:
                    print(f'Транзакция "{transaction.get("comment")}" на сумму {transaction.get("value")} не может быть применена (превышен лимит)')

        input('\n' + 'Для продолжения нажмите любую клавишу')

    elif operation == '8':  # статистика транзакций
        if len([1 for t in acc_dict.get('transactions') if t.get('applied') is False]):
            transactions_stats = {}
            for t in acc_dict.get('transactions'):
                if t.get('applied') is False:
                    transactions_stats[t.get('value')] = transactions_stats.get(t.get('value'), 0) + 1
            for key, value in transactions_stats.items():
                print(key, 'руб.:', value, 'платеж(а)')
        else:
            print('Ожидающие транзакции отсутствуют')
        input('\n' + 'Для продолжения нажмите любую клавишу')
    elif operation == '9':  # фильтр транзакций
        threshold = numbers_only(input('Покажем транзакции размером БОЛЬШЕ введенной суммы (при наличии): '))

        for value, comment, applied in transaction_walker(acc_dict.get('transactions')):
            if not applied and value > threshold:
                print(f'Сумма: {value}; Комментарий: {comment};')

    elif operation == '10':  # выход
        print('До свидания! "Веселый питон" благодарит вас за доверие.')
        break
    else:
        print('Несуществующий код операции. Повторите ввод.')
