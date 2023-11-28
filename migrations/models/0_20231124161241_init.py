from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `ingredient` (
    `ingredient_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `chinese_name` VARCHAR(255) NOT NULL UNIQUE COMMENT '中文名',
    `ping_yin` VARCHAR(255)   COMMENT '拼音',
    `english_name` VARCHAR(255) NOT NULL UNIQUE COMMENT '英文名',
    `introduction` LONGTEXT NOT NULL  COMMENT '简介',
    `effects` LONGTEXT NOT NULL  COMMENT '功效',
    `rating` DOUBLE NOT NULL  COMMENT '评分',
    `potential_risk_people` VARCHAR(255)   COMMENT '潜在风险人群',
    `daily_intake_recommendation` LONGTEXT NOT NULL  COMMENT '每日建议摄入量'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(15) NOT NULL,
    `openid` VARCHAR(128) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `favorites` (
    `favorites_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '收藏夹id',
    `note` VARCHAR(255) NOT NULL  COMMENT '备注' DEFAULT '这是一条历史记录',
    `user_id` INT NOT NULL COMMENT '用户id',
    CONSTRAINT `fk_favorite_user_cbcf4157` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `history` (
    `image_url` VARCHAR(256) NOT NULL  COMMENT '图片url',
    `history_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '收藏夹id',
    `date` DATE NOT NULL  COMMENT '历史记录的时间',
    `user_id` INT NOT NULL COMMENT '用户id',
    CONSTRAINT `fk_history_user_afeab6d0` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `favorites_ingredient` (
    `favorites_id` INT NOT NULL,
    `ingredient_id` INT NOT NULL,
    FOREIGN KEY (`favorites_id`) REFERENCES `favorites` (`favorites_id`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `history_ingredient` (
    `history_id` INT NOT NULL,
    `ingredient_id` INT NOT NULL,
    FOREIGN KEY (`history_id`) REFERENCES `history` (`history_id`) ON DELETE CASCADE,
    FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
