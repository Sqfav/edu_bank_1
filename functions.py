# этот вариант на доработке, нужно обработать случай, когда это первое добавление - сейчас срезается лишнее
# def add_trans(new_transaction): # дописывает транзакцию в конец json
#     # идея в обрезании закрывающих скобок и их восстановлении вместе с добавленным блоком
#     with open(acc_path, 'a', encoding='utf-8') as file:
#         file.seek(0, 2)
#         end_pos = file.tell()
#         file.truncate(file.seek(end_pos - 10))
#         string_to_add = f''',
#         {{
#             "value": {new_transaction.get('value')},
#             "comment": "{new_transaction.get('comment')}",
#             "applied": false
#         }}
#     ]
# }}'''
#         file.write(string_to_add)

import json

# Для проверки, что строки для приведения к int
# содержат только цифры и также будут неотрицательны
def numbers_only(sample):
    while not sample.isnumeric():
        sample = input('Для ввода допустимы только цифры. Пожалуйста, повторите ввод: ')
    return int(sample)


def can_topup(amount, balance, limit):  # проверка возможности пополнения или применения транзакции
     return True if limit is None else balance + amount <= limit


def password_checked(password):  # Для сверки пароля
    entered_password = input('Для продолжения введите пароль: ')
    while entered_password != password:
        print('Ошибка верификации пароля, повторите ввод (0 - для выхода в предыдущее меню)')
        entered_password = input('Пароль: ')
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
