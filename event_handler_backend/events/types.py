from .models import *
import strawberry_django
from strawberry import auto
import strawberry
from typing import Optional

@strawberry_django.type(TimeTable)
class TimeTableType:
    name : auto
    createdAt : auto
    dueDate : auto
    startTime :auto
    endTime : auto
    user : "User"
    details : auto

@strawberry_django.type(User)
class UserType:
    id: auto
    email: auto
    username: auto
    role: auto


@strawberry.type
class ResponseType:
    message: str
    status: str

@strawberry.type
class fetchAllUsersResp:
    status: str
    message: str
    users: Optional[list[UserType]] = None