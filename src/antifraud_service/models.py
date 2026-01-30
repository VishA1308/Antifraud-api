from pydantic import BaseModel,field_validator,ValidationError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta



class Loan_history(BaseModel):
    amount: int
    loan_data: str
    is_closed: bool = False

    @field_validator('loan_data')
    @classmethod
    def validate_loan_date(cls, value) ->str:
        try:
            loan_data = datetime.strptime(value, "%d.%m.%Y")
            if loan_data.date() > date.today():
                raise ValueError("Дата займа не может быть в будущем")
            return value
        except ValueError as e:
            error_msg = str(e)
            if "Дата займа не может быть в будущем" in error_msg:
                raise ValueError("Дата займа не может быть в будущем") from e
            else:
                raise ValueError("Дата займа должна быть в формате DD.MM.YYYY")

class UserCreate(BaseModel):
    birth_date: str
    phone_number: str
    loans_history:list[Loan_history] = []

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, value) -> str:
        try:
            birth_date = datetime.strptime(value, "%d.%m.%Y")
            if birth_date.date() > date.today():
                raise ValueError("Дата рождения не может быть в будущем")
            return value
        except ValueError as e:
            error_msg = str(e)
            if "Дата рождения не может быть в будущем" in error_msg:
                raise ValueError("Дата рождения не может быть в будущем") from e
            else:
                raise ValueError("Дата рождения должна быть в формате DD.MM.YYYY")


    def is_under_18(self)->bool:
        birth_date = datetime.strptime(self.birth_date, "%d.%m.%Y").date()
        date_now = date.today()
        diff = relativedelta(date_now,birth_date)
        if diff.years < 18:
            return True
        else:
            return False
    def is_not_rus_phone(self) -> bool:
        phone_num = self.phone_number
        clean_text = ""  
        
        for char in phone_num:
            if char.isdigit() or char == '+':
                clean_text += char
        
        phone_num = clean_text
        
        if not phone_num or len(phone_num) < 11:
            return True
        
        phone_num_0 = phone_num[0]
        if phone_num_0 == '+':
            phone_num_1 = phone_num[1]
            if phone_num_1 == '7':
                return False
            else:
                return True
        elif phone_num_0 == '8':
            return False
        else:
            return True
    def has_open_loans(self) ->bool:
        for loan in self.loans_history:
            if not loan.is_closed:
                return True
        return False