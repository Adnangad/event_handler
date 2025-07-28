import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from .types import UserType, ResponseType, fetchAllUsersResp
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from strawberry.types import Info
from django.http import HttpRequest
import datetime
from dotenv import load_dotenv
from os import getenv
import jwt
load_dotenv()

def get_current_user(request: HttpRequest):
    token = request.COOKIES.get('token')
    if not token:
        return None
    try:
        decoded = jwt.decode(token, getenv("JWT_SECRET"), algorithms=[getenv("JWT_ALGORITHM")])
        return decoded
    except Exception as e:
        print("AN ERROR OCCURED WHILE TRYING TO DECODE TOKEN:: ", e)
        return None

@strawberry.type
class Query:
    @strawberry.field
    def all_users(self, info: Info) -> fetchAllUsersResp:
        try:
            print("Fetching users...")
            current_user = get_current_user(info.context.request)
            if current_user is None:
                return fetchAllUsersResp(status="Error", message="Kindly log in to continue")
            if current_user['role'] != 'Admin':
                return fetchAllUsersResp(status="Error", message="Only Admins are authorized to access such data", users=None)
            users = User.objects.all()             
            return fetchAllUsersResp(status="Success", message="Users fetched successfully", users=users)
        except Exception as e:
            print("An error occured....")
            print("Error:: ", e)
            return fetchAllUsersResp(status="Error", message="Unable to fetch data at this time, please try again later", users=None)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str, password: str, role: str) -> ResponseType:
        try:
            user_exists = await sync_to_async(lambda: User.objects.filter(email=email).exists())()
            print(user_exists)
            if user_exists:
                return ResponseType(status="Error", message=f"A user with the email {email} already exists")
            await sync_to_async(User.objects.create)(username=name, email=email, password=make_password(password), role=role)
            return ResponseType(status="Success", message="You have successfully signed up")
        except Exception as e:
            print("An error occurred...")
            print(e)
            return ResponseType(status="Error", message="Unable to sign you up at this time")
    
    @strawberry.mutation
    async def login(self, info: Info, email: str, password: str) -> ResponseType:
        try:
            print("Logging in....")
            user_exists = await sync_to_async(lambda: User.objects.filter(email=email).exists())()
            if not user_exists:
                return ResponseType(status="Error", message=f"No user with the email: {email} exists in the system")
            user = await sync_to_async(lambda: User.objects.filter(email=email).first())()
            print("User is:: ", user)
            if not check_password(password, user.password):
                return ResponseType(status="Error", message="Invalid Password")
            payload = {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=(60 * 60 * 24 * 7))
            }            
            token = jwt.encode(payload, getenv("JWT_SECRET"), algorithm=getenv("JWT_ALGORITHM"))    
            response = info.context.response
            response.set_cookie(
                "token",
                token,
                httponly=True,
                max_age=60 * 60 * 24 * 7
            )
            return ResponseType(status="Success", message="You have successfully loggedin")
        except Exception as e:
            print("An error occured...", e)
            return ResponseType(status="Error", message="Unable to log you in at this time, kindly try again later")