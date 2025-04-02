from pydantic import BaseModel

from src.models.likes import ReactionTypeEnum


class ReviewLikeResponse(BaseModel):
	id: int | None = None
	user_id: int
	review_id: int
	is_liked: bool


class ReviewLikeCountResponse(BaseModel):
	review_id: int
	like_count: int


class ReviewIsLikedResponse(ReviewLikeResponse):
	review_id: int
	user_id: int
	is_liked: bool


class MovieReactionResponse(BaseModel):
	id: int
	user_id: int
	movie_id: int
	type: ReactionTypeEnum
