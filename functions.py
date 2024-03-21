import json
import math
import os


def find_all_accs(path):
    acc_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            acc_files.append(file)
    return acc_files


def check_login_exists(login, path):
    return login + '.txt' in find_all_accs(path)

# в идеале должно рекурсивно обновлять данные в файлах других аккаунтов
def apply_delayed_transfers(curr_acc, acc_path):
    used_acc = set()
    for i in range(len(curr_acc.get('delayed_transfers'))):
        if curr_acc.get('balance') >= curr_acc.get('delayed_transfers')[0].get('amount'):
            if check_login_exists(curr_acc.get('delayed_transfers')[0].get('destination'), acc_path):
                curr_acc['balance'] -= curr_acc.get('delayed_transfers')[0].get('amount')
                dest_acc = acc_load_file(acc_path + curr_acc.get('delayed_transfers')[0].get('destination') + '.txt')
                dest_acc['balance'] += curr_acc.get('delayed_transfers')[0].get('amount')

                used_acc.add(curr_acc.get('delayed_transfers')[0].get('destination'))

                acc_write_file(acc_path + dest_acc.get('login') + '.txt', dest_acc)

                curr_acc['delayed_transfers'].pop(0)

                print('Исполнен ожидающий перевод')

                acc_write_file(acc_path + curr_acc.get('login') + '.txt', curr_acc)

    for acc in used_acc:
        apply_delayed_transfers(acc_load_file(acc_path + acc + '.txt'), acc_path)


def passhash(password):
    sumord = sum(ord(p) for p in password) % 1234001651
    prodord = math.prod(ord(p) for p in password) % 1234001651
    pass_hash = sumord + prodord
    return pass_hash


# Для проверки, что строки для приведения к int
# содержат только цифры и также будут неотрицательны
def numbers_only(sample):
    while not sample.isnumeric():
        sample = input('Для ввода допустимы только цифры. Пожалуйста, повторите ввод: ')
    return int(sample)


def can_topup(amount, balance, limit):  # проверка возможности пополнения или применения транзакции
    return True if limit is None else balance + amount <= limit


def password_checked(password):  # Для сверки пароля
    entered_password = passhash(input('Для продолжения введите пароль: '))
    while entered_password != password:
        print('Ошибка верификации пароля, повторите ввод (0 - для выхода в предыдущее меню)')
        entered_password = passhash(input('Пароль: '))
        if entered_password == '0':
            return False
    return True


# сброс всех используемых данных в файл
def acc_write_file(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))


def acc_load_file(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def transaction_walker(list_of_dicts):
    for t in list_of_dicts:
        yield t.get('value'), t.get('comment'), t.get('applied')
