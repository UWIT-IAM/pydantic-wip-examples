from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field
from inflection import camelize


def to_camel(val: str) -> str:
    """
    I prefer non-capitalized, except for class names, so I use the inflection
    library to perform this operation. You do you, boo.
    """
    return camelize(val, uppercase_first_letter=False)


class ORMProxyBase(BaseModel):
    """A simple base model to house configuration that we will reuse."""
    class Config:
        orm_mode = True  # Set values from object fields
        allow_population_by_field_name = True  # Allow setting with snake_case or camelCase
        alias_generator = to_camel  # When using `by_alias=True`, turns "snake_case" into "camelCase"
        extra = Extra.ignore  # If we receive values not declared on our models, just ignore them.


class UserSettingsBase(ORMProxyBase):
    """
    Contains a user's profile settings. In this base class, we don't require any
    values to be set, so that request models can be built and used even if there
    isn't a corresponding database model yet; for instance.
    """
    email_subscription: bool = False
    private_profile: bool = True
    email_address: Optional[EmailStr]


class UserBase(ORMProxyBase):
    """
    Contains basic fields you might find on a User table.
    """
    user_id: Optional[int]
    username: Optional[str] = Field(None, min_length=6, max_length=24)
    settings: Optional[UserSettingsBase]


class CreateUserInput(UserBase):
    """Here we inherit from UserBase, but re-declare fields we want to require for
    this use case. When we create a user, we require them to provide a username and an
    email address. Notice that the email address is _not_ part of the UserBase model, but
    is instead in the UserSettingsBase model.

    Because we have declared the use case in the class name: "It's the input model for creating a user."
    You'll see below how we handle value that exists here, but needs to be "moved" to the settings class
    during the request.
    """
    username: str
    email_address: EmailStr


class CreateUserOutput(UserBase):
    """Here we inherit again from UserBase, but this time we set some different requirements.
    We now require user_id (because it necessarily must exist after creating the user in the database),
    as well as settings, because they are created during the creation process. Now, for instance, the
    front-end can allow a user to toggle their default profile settings, which will include the email
    address they passed in CreateUserInput.
    """
    username: str
    user_id: int
    settings: UserSettingsBase
