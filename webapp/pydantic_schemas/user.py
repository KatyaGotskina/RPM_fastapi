from pydantic import BaseModel, ConfigDict,  PydanticUserError


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    first_name: str
    last_name: str


class UserCreateModel(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


class ID(BaseModel):
    id: int
