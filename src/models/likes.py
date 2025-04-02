from enum import StrEnum

from tortoise import Model, fields

from src.models.base import BaseModel


class ReviewLike(BaseModel, Model):
	user = fields.ForeignKeyField("models.User", related_name="review_likes")
	review = fields.ForeignKeyField("models.Review", related_name="likes")
	is_liked = fields.BooleanField(default=True)
	
	class Meta:
		table = "review_likes"
		unique_together = (("user", "review"),)


class ReactionTypeEnum(StrEnum):
	LIKE = "like"
	DISLIKE = "dislike"


class MovieReaction(BaseModel, Model):
	user = fields.ForeignKeyField("models.User", related_name="movie_reactions")
	movie = fields.ForeignKeyField("models.Movie", related_name="reactions")
	type = fields.CharEnumField(ReactionTypeEnum, default=ReactionTypeEnum.LIKE)
	
	class Meta:
		table = "movie_reactions"
		unique_together = (("user", "movie"),)
