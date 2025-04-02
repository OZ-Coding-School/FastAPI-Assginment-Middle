from enum import StrEnum

from tortoise import fields, Model

from src.models.base import BaseModel


class GenderEnum(StrEnum):
    MALE = "male"
    FEMALE = "female"


class User(BaseModel, Model):
    username = fields.CharField(unique=True, max_length=50, index=True)  
    hashed_password = fields.CharField(max_length=128)
    age = fields.IntField()
    gender = fields.CharEnumField(GenderEnum)
    profile_image_url = fields.CharField(max_length=255, null=True)
    last_login = fields.DatetimeField(null=True)

    class Meta:
        table = 'users'


class Follow(BaseModel, Model):
    follower = fields.ForeignKeyField('models.User', related_name='followers')
    following = fields.ForeignKeyField('models.User', related_name='following')
    is_following = fields.BooleanField(default=True)
    
    class Meta:
        table = 'follows'
        unique_together = (('follower', 'following'),)
