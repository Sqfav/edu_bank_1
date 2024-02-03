import pytest
from functions import can_topup, numbers_only, password_checked, transaction_walker


def test_topup_none_limit():
    assert can_topup(100, 0, None) is True


def test_b_a_more_limit():
    assert can_topup(1, 1, 1) is False


def test_correct_topup():
    assert can_topup(1, 0, 1) is True


def test_numbers_only_wrong_then_correct(monkeypatch):
    inputs = iter(['abc', '-1', '123'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert numbers_only("test") == 123
    # проверили, что отвергаются отрицательные числа, возвращается int и ввод идет до первого подходящего


def test_numbers_only_wrong(monkeypatch):
    inputs = iter(['abc', 'def', 'abc', 'def', '1-23', '', ' '])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        numbers_only('-10')
    # много неправильных значений

def test_password_checked_true(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'correct_password')
    assert password_checked('correct_password') == True


def test_password_error_to_wrong_pass(monkeypatch, capsys):
    inputs = iter(['wrong password', 'correct_password'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    password_checked('correct_password')
    captured = capsys.readouterr()
    assert captured.out == 'Ошибка верификации пароля, повторите ввод (0 - для выхода в предыдущее меню)\n'


def test_password_checked_endless(monkeypatch, capsys):
    inputs = iter(['abc', 'def', 'abc', 'def', '1-23', '', ' '])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        password_checked('correct_password')
    captured = capsys.readouterr() # просто забрать мусорный вывод в консоль


def test_password_checked_0(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: '0')
    password_checked('correct_password')
    assert password_checked('pass1') == False
    captured, err = capsys.readouterr()


def test_transaction_walker():
    acc_dict = {}
    acc_dict['transactions'] = [{'value': 100, 'comment': 'За обучение', 'applied': True}]
    for value, comment, applied in transaction_walker(acc_dict['transactions']):
        if applied:
            assert value == 100 and comment == 'За обучение'
