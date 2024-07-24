from pydantic import BaseModel
from pydantic import Field
from python_random_strings import random_strings

class AddUpdateTujuanUserCategory(BaseModel) :
    id : str = str(random_strings.random_digits(6))
    name : str = Field(max_length=255)

class ResponseTujuanUserCategory(BaseModel) :
    id : str
    name : str = Field(max_length=255)