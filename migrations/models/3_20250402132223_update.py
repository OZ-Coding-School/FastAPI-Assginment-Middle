from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `following` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `is_following` BOOL NOT NULL  DEFAULT 1,
    `follower_id` BIGINT NOT NULL,
    `following_id` BIGINT NOT NULL,
    UNIQUE KEY `uid_following_followe_b41b68` (`follower_id`, `following_id`),
    CONSTRAINT `fk_followin_users_ed42ad0c` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_followin_users_f58bd8f4` FOREIGN KEY (`following_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        DROP TABLE IF EXISTS `review_likes`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `following`;"""
