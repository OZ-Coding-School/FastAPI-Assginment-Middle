from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, Query, APIRouter, status, Depends, UploadFile, Path
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.expressions import Subquery

from src.models.users import User, Follow
from src.schemas.users import UserUpdateRequest, UserCreateRequest, UserSearchParams, Token, UserResponse, \
	FollowResponse, FollowingUserResponse, FollowerUserResponse
from src.utils.auth import authenticate, get_current_user, hash_password
from src.utils.file import validate_image_extension, delete_file, upload_file
from src.utils.jwt import create_access_token

user_router = APIRouter(prefix='/users', tags=["users"])


@user_router.post('')
async def create_user(data: UserCreateRequest):
	data = data.model_dump()
	data['hashed_password'] = hash_password(data.pop('password'))
	user = await User.create(**data)
	return user.id


@user_router.get('')
async def get_all_users() -> list[UserResponse]:
	result = await User.filter().all()
	if not result:
		raise HTTPException(status_code=404)
	return result


@user_router.post('/login', response_model=Token)
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	user = await authenticate(data.username, data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token = create_access_token(data={"user_id": user.id})
	user.last_login = datetime.now()
	await user.save()
	return Token(access_token=access_token, token_type="bearer")


@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]) -> list[UserResponse]:
	valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
	filtered_users = await User.filter(**valid_query).all()
	if not filtered_users:
		raise HTTPException(status_code=404)
	return filtered_users


@user_router.get('/me')
async def get_user(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
	return UserResponse(id=user.id, username=user.username, age=user.age, gender=user.gender)


@user_router.patch('/me')
async def update_user(
	user: Annotated[User, Depends(get_current_user)],
	data: UserUpdateRequest,
) -> UserResponse:
	update_data = {key: value for key, value in data.model_dump().items() if value is not None}
	if 'password' in update_data.keys():
		update_data['hashed_password'] = hash_password(update_data.pop('password'))
	user = await user.update_from_dict(data=update_data)
	await user.save()
	return UserResponse(id=user.id, username=user.username, age=user.age, gender=user.gender)


@user_router.delete('/me')
async def delete_user(user: Annotated[User, Depends(get_current_user)]):
	await user.delete()
	return {'detail': 'Successfully Deleted.'}


@user_router.post("/me/profile_image", status_code=200)
async def register_profile_image(image: UploadFile, user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
	validate_image_extension(image)
	prev_image_url = user.profile_image_url
	try:
		image_url = await upload_file(image, "users/profile_images")
		user.profile_image_url = image_url
		await user.save()
		
		if prev_image_url is not None:
			delete_file(prev_image_url)

		return UserResponse(
			id=user.id,
			username=user.username,
			age=user.age,
			gender=user.gender,
			profile_image_url=user.profile_image_url
		)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@user_router.post("/{user_id}/follow", status_code=200)
async def following_user(
	user: Annotated[User, Depends(get_current_user)],
	user_id: int = Path(gt=0)
) -> FollowResponse:
	follow, _ = await Follow.get_or_create(follower_id=user.id, following_id=user_id)
	
	if not follow.is_following:
		follow.is_following = True
		await follow.save()
	
	return FollowResponse(
		follower_id=follow.follower_id,
		following_id=follow.following_id,
		is_following=follow.is_following
	)


@user_router.post("/{user_id}/unfollow", status_code=200)
async def unfollowing_user(
	user: Annotated[User, Depends(get_current_user)],
	user_id: int = Path(gt=0)
) -> FollowResponse:
	follow = await Follow.filter(follower_id=user.id, following_id=user_id).first()
	
	if not follow:
		FollowResponse(
			follower_id=user.id,
			following_id=user_id,
			is_following=False
		)
	
	if follow.is_following:
		follow.is_following = False
		await follow.save()
		
	return FollowResponse(
		follower_id=follow.follower_id,
		following_id=follow.following_id, 
		is_following=follow.is_following
	)


@user_router.get("/me/followings", status_code=200)
async def get_my_followings(user: Annotated[User, Depends(get_current_user)]) -> list[FollowingUserResponse]:
	following_users = await User.filter(
		id__in=Subquery(Follow.filter(follower_id=user.id, is_following=True).values("following_id"))
	).all()
	
	return [
		FollowingUserResponse(
			following_id=user.id,
			username=user.username,
			profile_image_url=user.profile_image_url
		) for user in following_users
	]


@user_router.get("/me/followers", status_code=200)
async def get_my_followers(user: Annotated[User, Depends(get_current_user)]) -> list[FollowerUserResponse]:
	following_users = await User.filter(
		id__in=Subquery(Follow.filter(following_id=user.id, is_following=True).values("following_id"))
	).all()
	
	return [
		FollowerUserResponse(
			follower_id=user.id,
			username=user.username,
			profile_image_url=user.profile_image_url
		) for user in following_users
	]
