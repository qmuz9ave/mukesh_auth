import pydantic

class UserModel(pydantic.BaseModel):
    id: int = None
    name: str = None
    mobile_number: int = None
    password: str = None
    dob:str = None
