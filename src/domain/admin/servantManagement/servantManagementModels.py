from pydantic import BaseModel,Field,EmailStr
from python_random_strings import random_strings

class AddPelayananServantCategory(BaseModel) :
    id : str = str(random_strings.random_digits(6))
    name : str

class UpdatePelayananServantCategory(BaseModel) :
    id : str = str(random_strings.random_digits(6))
    name : str

class ResponsePelayananServantCategory(BaseModel) :
    id : str = str(random_strings.random_digits(6))
    name : str