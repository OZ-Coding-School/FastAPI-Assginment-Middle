from datetime import timedelta
from typing import Annotated

from fastapi import Path, HTTPException, Query, APIRouter, status

from src.models.users import UserModel
from src.schemas.users import UserUpdateRequest, UserCreateRequest, UserSearchParams, UserLoginRequest, \
	UserLoginResponse, Token
from src.utils.jwt import create_access_token

user_router = APIRouter(prefix='/users', tags=["users"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@user_router.post('')
async def create_user(data: UserCreateRequest):
	user = UserModel.create(**data.model_dump())
	return user.id


@user_router.get('')
async def get_all_users():
	result = UserModel.all()
	if not result:
		raise HTTPException(status_code=404)
	return result


@user_router.post('/login', response_model=UserLoginResponse)
async def login_user(data: UserLoginRequest):
	user = UserModel.authenticate(data.username, data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)
	return UserLoginResponse(id=user.id, access_token=Token(access_token=access_token, token_type="bearer"))


@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
	valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
	filtered_users = UserModel.filter(**valid_query)
	if not filtered_users:
		raise HTTPException(status_code=404)
	return filtered_users


@user_router.get('/{user_id}')
async def get_user(user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	return user


@user_router.patch('/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	user.update(**data.model_dump())
	return user


@user_router.delete('/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	user.delete()
	
	return {'detail': f'User: {user_id}, Successfully Deleted.'}
