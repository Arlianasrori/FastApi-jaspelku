import re
from ..error.errorHandling import HttpException

def phoneValidation(phone : str) -> str :
    if not phone :
        raise HttpException(400,"invalid number phone")
    regexPhoneValidation = r"^(\+62|62|0)8[1-9][0-9]{6,9}$"
    isPhone = re.fullmatch(regexPhoneValidation,phone)

    if not isPhone :
        raise HttpException(400,"invalid number phone")
    else :
        if "+62" in phone :
            # if number using +62 format.split phone number and return with 0 format
            phoneSplit = phone.split("+62")[1]
            return f"0{phoneSplit}"
        return phone