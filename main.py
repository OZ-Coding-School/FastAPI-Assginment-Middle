from fastapi import FastAPI

from src.configs.database import initialize_tortoise
from src.routers.movies import movie_router
from src.routers.likes import like_router
from src.routers.notifications import notification_router
from src.routers.reviews import review_router
from src.routers.users import user_router
import src.signals

app = FastAPI()


app.include_router(user_router)
app.include_router(movie_router)
app.include_router(review_router)
app.include_router(like_router)
app.include_router(notification_router)

initialize_tortoise(app=app)

if __name__ == '__main__':
	import uvicorn
	
	uvicorn.run(app, host='0.0.0.0', port=8000)
