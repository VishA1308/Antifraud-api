import pytest
import sys
import os
sys.path.insert(0, '/app/src')

from antifraud_service.models import UserCreate, Loan_history
from datetime import date
import json

def test_loan_history_amount():
    """Тест корректного сохранения суммы займа"""
    loan = Loan_history(
        amount=10000,
        loan_data="01.01.2023",
        is_closed=True
    )
    assert loan.amount == 10000


def test_loan_history_loan_data():
    """Тест корректного сохранения даты займа"""
    loan = Loan_history(
        amount=10000,
        loan_data="01.01.2023",
        is_closed=True
    )
    assert loan.loan_data == "01.01.2023"

def test_loan_history_is_closed():
    """Тест корректного сохранения статуса закрытия займа"""
    loan = Loan_history(
        amount=10000,
        loan_data="01.01.2023",
        is_closed=True
    )
    assert loan.is_closed is True

def test_loan_history_invalid_format():
    """Тест валидации неверного формата даты займа"""
    with pytest.raises(Exception) as exc_info:
        Loan_history(
            amount=10000,
            loan_data="2023-01-01",  # Неправильный формат (YYYY-MM-DD вместо DD.MM.YYYY)
            is_closed=True
        )
    assert "Дата займа должна быть в формате DD.MM.YYYY" in str(exc_info.value)

def test_loan_history_future_date():
    """Тест валидации будущей даты займа"""
    year_test = date.today().year + 1
    future_date = date.today().replace(year=year_test)
    
    with pytest.raises(Exception) as exc_info:
        Loan_history(
            amount=10000,
            loan_data=future_date.strftime("%d.%m.%Y"),
            is_closed=True
        )
    assert "Дата займа не может быть в будущем" in str(exc_info.value)

def test_user_create_birth_date():
    """Тест корректного сохранения даты рождения пользователя"""
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.birth_date == "15.05.1990"


def test_user_create_phone_number():
    """Тест корректного сохранения номера телефона"""
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.phone_number == "+79161234567"

def test_user_create_loan_history():
    """Тест корректного сохранения истории займов"""
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[Loan_history(amount=10000, loan_data="01.01.2023", is_closed=True)]
    )
    assert len(user.loans_history) == 1

def test_user_create_invalid_birth_date_format():
    """Тест валидации неверного формата даты рождения"""
    with pytest.raises(Exception) as exc_info:
        UserCreate(
            birth_date="1990-05-15",  # Неправильный формат (YYYY-MM-DD вместо DD.MM.YYYY)
            phone_number="+79161234567",
            loans_history=[]
        )
    assert "Дата рождения должна быть в формате DD.MM.YYYY" in str(exc_info.value)

def test_user_create_future_birth_date():
    """Тест валидации будущей даты рождения"""
    year_test = date.today().year + 1
    future_date = date.today().replace(year=year_test)
    
    with pytest.raises(Exception) as exc_info:
        UserCreate(
            birth_date=future_date.strftime("%d.%m.%Y"),
            phone_number="+79161234567",
            loans_history=[]
        )
    assert "Дата рождения не может быть в будущем" in str(exc_info.value)

    
def test_is_under_18_adult():
    """Тест проверки возраста для взрослого пользователя (30 лет)"""
    year_test = date.today().year - 30  
    thirty_years = date.today().replace(year=year_test) 
    user = UserCreate(
        birth_date=thirty_years.strftime("%d.%m.%Y"),
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.is_under_18() is False


def test_is_under_18_18():
    """Тест проверки возраста для пользователя ровно 18 лет"""
    year_test = date.today().year - 18  
    eighteen_years = date.today().replace(year=year_test) 
    user = UserCreate(
        birth_date=eighteen_years.strftime("%d.%m.%Y"),
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.is_under_18() is False


def test_is_under_18_child():
    """Тест проверки возраста для ребенка (10 лет)"""
    year_test = date.today().year - 10  
    ten_years = date.today().replace(year=year_test) 
    user = UserCreate(
        birth_date=ten_years.strftime("%d.%m.%Y"),
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.is_under_18() is True

def test_has_open_loans_no_loans():
    """Тест проверки открытых займов при пустой истории"""
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.has_open_loans() is False


def test_has_open_loans_closed():
    """Тест проверки открытых займов при всех закрытых займах"""
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[
            Loan_history(amount=10000, loan_data="01.01.2023", is_closed=True),
            Loan_history(amount=20000, loan_data="15.06.2023", is_closed=True),
            Loan_history(amount=15000, loan_data="01.09.2023", is_closed=True)
        ]
    )
    assert user.has_open_loans() is False


def test_has_open_loans_open():
    """Тест проверки открытых займов при наличии хотя бы одного незакрытого"""
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[
            Loan_history(amount=10000, loan_data="01.01.2023", is_closed=True),
            Loan_history(amount=20000, loan_data="15.06.2023", is_closed=False),  # Открытый займ
            Loan_history(amount=15000, loan_data="01.09.2023", is_closed=True)
        ]
    )
    assert user.has_open_loans() is True


@pytest.mark.parametrize(
    "phone_number, expected_result",
    [
        ("+79831324066", False),  
        ("+79072016666", False),                     
        ("++79161234567", True),  
        ("+", True),  
        ("89831324066", False),  
        ("+89831324066", True),  
        ("79161234567", True),  
        ("+375123456789", True),  
        ("", True), 
        ("  ", True),  
    ]
)
def test_is_not_rus_phone_russian_numbers(phone_number, expected_result):
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number=phone_number,
        loans_history=[]
    )
    assert user.is_not_rus_phone() == expected_result