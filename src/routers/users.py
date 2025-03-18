from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, Query, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.models.users import UserModel
from src.schemas.users import UserUpdateRequest, UserCreateRequest, UserSearchParams, Token
from src.utils.jwt import create_access_token, get_current_user

user_router = APIRouter(prefix='/users', tags=["users"])


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


@user_router.post('/login', response_model=Token)
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	user = UserModel.authenticate(data.username, data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token = create_access_token(data={"user_id": user.id})
	user.update(last_login=datetime.now())
	return Token(access_token=access_token, token_type="bearer")


@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
	valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
	filtered_users = UserModel.filter(**valid_query)
	if not filtered_users:
		raise HTTPException(status_code=404)
	return filtered_users


@user_router.get('/me')
async def get_user(user: Annotated[UserModel, Depends(get_current_user)]):
	return user


@user_router.patch('/me')
async def update_user(
	user: Annotated[UserModel, Depends(get_current_user)],
	data: UserUpdateRequest,
):
	if user is None:
		raise HTTPException(status_code=404)
	user.update(**data.model_dump())
	return user


@user_router.delete('/me')
async def delete_user(user: Annotated[UserModel, Depends(get_current_user)],):
	user.delete()
	return {'detail': 'Successfully Deleted.'}
