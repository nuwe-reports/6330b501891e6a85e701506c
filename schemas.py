from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class JobPost(BaseModel):
    name: str
    company_name: Optional[str]
    job_description: Optional[str]
    skills: Optional[str]
    job_type: Optional[str]
    locations: Optional[str]
    comments: Optional[str]


class JobPostUpdate(BaseModel):
    name: Optional[str]
    company_name: Optional[str]
    job_description: Optional[str]
    skills: Optional[str]
    job_type: Optional[str]
    locations: Optional[str]
    comments: Optional[str]


class UserBase(BaseModel):
    email: EmailStr = Field(
        # ...,
        example="myemail@cosasdedevs.com"
    )
    username: str = Field(
        # ...,
        min_length=3,
        max_length=50,
        example="MyTypicalUsername",
    )
    # subscribed: bool


class User(UserBase):
    id: str = Field(
        # ...,
        # example="5"
    )


class UserRegister(UserBase):
    password: str = Field(min_length=8, max_length=64, example="strongpass")
