from pydantic import BaseModel
from pydantic import Field

class AddUpdateTujuanUserCategory(BaseModel) :
    name : str = None

class ResponseTujuanUserCategory(BaseModel) :
    id : str
    name : str = Field(max_length=255)