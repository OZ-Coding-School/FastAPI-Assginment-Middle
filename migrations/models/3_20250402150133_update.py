from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `movie_reactions` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `type` VARCHAR(7) NOT NULL  COMMENT 'LIKE: like\nDISLIKE: dislike' DEFAULT 'like',
    `movie_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    UNIQUE KEY `uid_movie_react_user_id_19ad8d` (`user_id`, `movie_id`),
    CONSTRAINT `fk_movie_re_movies_68679e90` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_movie_re_users_ce8163a3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `follow` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `is_following` BOOL NOT NULL  DEFAULT 1,
    `follower_id` BIGINT NOT NULL,
    `following_id` BIGINT NOT NULL,
    UNIQUE KEY `uid_following_followe_b41b68` (`follower_id`, `following_id`),
    CONSTRAINT `fk_followin_users_ed42ad0c` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_followin_users_f58bd8f4` FOREIGN KEY (`following_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """DROP TABLE IF EXISTS `movie_reactions`;
    DROP TABLE IF EXISTS `follow`;"""
