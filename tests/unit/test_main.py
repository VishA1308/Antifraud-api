import pytest
import sys
import os
sys.path.insert(0, '/app/src')

from antifraud_service.models import UserCreate, Loan_history
from datetime import date
import json
def test_loan_history_amount():
    
    loan = Loan_history(
        amount=10000,
        loan_data="01.01.2023",
        is_closed=True
    )
    assert loan.amount == 10000


def test_loan_history_loan_data():
    
    loan = Loan_history(
        amount=10000,
        loan_data="01.01.2023",
        is_closed=True
    )
    assert loan.loan_data == "01.01.2023"

def test_loan_history_is_closed():
    
    loan = Loan_history(
        amount=10000,
        loan_data="01.01.2023",
        is_closed=True
    )
    assert loan.is_closed is True

def test_loan_history_invalid_format():
    with pytest.raises(Exception) as exc_info:
        Loan_history(
            amount=10000,
            loan_data="2023-01-01",  # Неправильный формат
            is_closed=True
        )
    assert "Дата займа должна быть в формате DD.MM.YYYY" in str(exc_info.value)

def test_loan_history_future_date():
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
   
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.birth_date == "15.05.1990"


def test_user_create_phone_number():
   
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[]
    )

    assert user.phone_number == "+79161234567"

def test_user_create_loan_history():
   
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[Loan_history(amount=10000, loan_data="01.01.2023", is_closed=True)]
    )
    assert len(user.loans_history) == 1

def test_user_create_invalid_birth_date_format():
    with pytest.raises(Exception) as exc_info:
        UserCreate(
            birth_date="1990-05-15",  # Неправильный формат
            phone_number="+79161234567",
            loans_history=[]
        )
    assert "Дата рождения должна быть в формате DD.MM.YYYY" in str(exc_info.value)

def test_user_create_future_birth_date():
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
    
    year_test = date.today().year - 30  
    thirty_years = date.today().replace(year=year_test) 
    user = UserCreate(
        birth_date=thirty_years.strftime("%d.%m.%Y"),
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.is_under_18() is False


def test_is_under_18_18():

    year_test = date.today().year - 18  
    eighty_years = date.today().replace(year=year_test) 
    user = UserCreate(
        birth_date=eighty_years.strftime("%d.%m.%Y"),
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.is_under_18() is False


def test_is_under_18_child():
    
    year_test = date.today().year - 10  
    ten_years = date.today().replace(year=year_test) 
    user = UserCreate(
        birth_date=ten_years.strftime("%d.%m.%Y"),
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.is_under_18() is True

def test_has_open_loans_no_loans():
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[]
    )
    assert user.has_open_loans() is False


def test_has_open_loans_closed():
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
    
    user = UserCreate(
        birth_date="15.05.1990",
        phone_number="+79161234567",
        loans_history=[
            Loan_history(amount=10000, loan_data="01.01.2023", is_closed=True),
            Loan_history(amount=20000, loan_data="15.06.2023", is_closed=False),  
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
        ("+" , True),            
        ("89831324066" , False),             
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


