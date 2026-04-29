from enum import StrEnum


class HTTPRoutes(StrEnum):
    USERS = "/api/v1/users"
    FILES = "/api/v1/files"
    COURSES = "/api/v1/courses"
    EXERCISES = "/api/v1/exercises"
    AUTHENTICATION = "/api/v1/authentication"
