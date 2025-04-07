from tortoise.signals import post_save

from src.models.users import Follow
from src.utils.websocket import manager


@post_save(Follow)
async def follow_signals(sender, instance, created, using_db, update_fields, **kwargs):
	if created or instance.is_following:
		await instance.fetch_related("follower")
		
		await manager.send_notification(
			user_id=instance.following_id, 
			message=f"{instance.follower.username}님이 팔로우 하셨습니다."
		)
