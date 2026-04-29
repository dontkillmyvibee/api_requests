from pydantic import BaseModel, HttpUrl, FilePath, Field

from tools.fakers import fake


class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl


class CreateFileRequestSchema(BaseModel):
    filename: str = Field(default_factory=lambda: f"{fake.uuid4()}.png")
    directory: str = Field(default="tests")
    upload_file: FilePath


class CreateFileResponseSchema(BaseModel):
    file: FileSchema


class GetFileResponseSchema(BaseModel):
    file: FileSchema
