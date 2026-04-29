from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TokensSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    token_type: str | None = Field(default=None, alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    token: TokensSchema


class RefreshRequestSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    refresh_token: str = Field(alias="refreshToken")


class RefreshResponseSchema(LoginResponseSchema):
    ...
