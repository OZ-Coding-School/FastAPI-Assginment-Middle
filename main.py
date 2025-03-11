from typing import Annotated

from fastapi import FastAPI, Path, HTTPException, Query

from src.models.users import UserModel

from src.schemas.users import UserCreateRequest, UserUpdateRequest, UserSearchParams

app = FastAPI()

UserModel.create_dummy()


@app.post('/users')
async def create_user(data: UserCreateRequest):
	user = UserModel(**data.model_dump())
	return user.id


@app.get('/users')
async def get_all_users():
	result = UserModel.all()
	if not result:
		raise HTTPException(status_code=404)
	return result

	
@app.get('/users/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
	valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
	filtered_users = UserModel.filter(**valid_query)
	if not filtered_users:
		raise HTTPException(status_code=404)
	return 	filtered_users


@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	return user


@app.patch('/users/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	user.update(**data.model_dump())
	return user


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	user.delete()

	return {'detail': f'User: {user_id}, Successfully Deleted.'}

	
if __name__ == '__main__':
	import uvicorn
	
	uvicorn.run(app, host='0.0.0.0', port=8000)
