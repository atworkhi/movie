/*
 Navicat Premium Data Transfer

 Source Server         : Local
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : localhost:3306
 Source Schema         : movie

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 26/05/2018 22:26:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `pwd` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of admin
-- ----------------------------
BEGIN;
INSERT INTO `admin` VALUES (1, 'admin', 'pbkdf2:sha256:50000$b9dcfwqt$b601b87ac1a12a37860df9e523323f390d7a48767d2c6f0570936aa44d1bf46c', 0, 3, '2018-05-19 10:27:23');
COMMIT;

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
BEGIN;
INSERT INTO `adminlog` VALUES (1, 1, '127.0.0.1', '2018-05-22 20:17:51');
INSERT INTO `adminlog` VALUES (2, 1, '127.0.0.1', '2018-05-23 11:07:22');
INSERT INTO `adminlog` VALUES (3, 1, '127.0.0.1', '2018-05-25 00:00:18');
COMMIT;

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `url` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of auth
-- ----------------------------
BEGIN;
INSERT INTO `auth` VALUES (1, '标签管理', '/admin/tag/', '2018-05-19 10:06:54');
INSERT INTO `auth` VALUES (2, '电影管理', '/admin/movie/', '2018-05-19 10:07:33');
INSERT INTO `auth` VALUES (4, '用户管理', '/admin/user/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (5, '预告管理', '/admin/preview/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (6, '评论管理', '/admin/comment/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (7, '收藏管理', '/admin/miviecol/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (8, '角色管理', '/admin/role/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (9, '权限管理', '/admin/auth/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (10, '管理员管理', '/admin/admin/', '2018-05-19 10:27:23');
INSERT INTO `auth` VALUES (11, '日志管理', '/admin/log/', '2018-05-19 10:27:23');
COMMIT;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text COLLATE utf8mb4_bin,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of comment
-- ----------------------------
BEGIN;
INSERT INTO `comment` VALUES (4, '好看', 4, 6, '2018-05-18 20:35:12');
INSERT INTO `comment` VALUES (5, '不错', 4, 7, '2018-05-18 20:35:12');
INSERT INTO `comment` VALUES (6, '经典', 4, 8, '2018-05-18 20:35:12');
INSERT INTO `comment` VALUES (8, '难看', 4, 10, '2018-05-18 20:35:12');
INSERT INTO `comment` VALUES (9, '无聊', 4, 11, '2018-05-18 20:35:12');
INSERT INTO `comment` VALUES (10, '乏味', 4, 12, '2018-05-18 20:35:12');
INSERT INTO `comment` VALUES (11, '<p>画是中国风的电影<img src=\"http://img.baidu.com/hi/jx2/j_0002.gif\"/></p>', 4, 18, '2018-05-23 22:33:39');
INSERT INTO `comment` VALUES (12, '<p>不错支持以下</p>', 4, 18, '2018-05-23 22:47:48');
INSERT INTO `comment` VALUES (13, '<p>不错支持以下</p>', 4, 18, '2018-05-23 22:49:16');
INSERT INTO `comment` VALUES (14, '<p>我自己的评论</p>', 4, 18, '2018-05-23 22:49:37');
INSERT INTO `comment` VALUES (15, '<p>号的</p>', 4, 19, '2018-05-24 23:34:36');
INSERT INTO `comment` VALUES (16, '<p>我觉得挺不错的</p>', 4, 19, '2018-05-24 23:51:10');
COMMIT;

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `url` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `info` text COLLATE utf8mb4_bin,
  `logo` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of movie
-- ----------------------------
BEGIN;
INSERT INTO `movie` VALUES (4, '画', '201805092211190aae155638b547ad82598b0817ddd2b9.mp4', '中国画', '20180509221119e2f68ca6755b44d5b09bfb24578e01b6.png', 4, 30, 6, 3, '中国', '2018-05-07', '8', '2018-05-09 22:11:20');
INSERT INTO `movie` VALUES (5, '水墨山水', '201805231730180c7bab86b887496b82d59c5d674641aa.mp4', '水墨画', '20180523173018ca23b59e29854766bc81f1c5cd72e619.png', 3, 6, 0, 2, '中国', '2018-05-03', '6', '2018-05-23 17:30:19');
INSERT INTO `movie` VALUES (6, '我就是试试', '20180523173309da8e503712364d97b0a48e88f1df8725.mp4', '我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件我就是测试文件', '20180523173309481cebf989594944b4bd4c1e91a2d591.png', 2, 10, 0, 1, '中国', '2018-05-01', '10', '2018-05-23 17:33:10');
COMMIT;

-- ----------------------------
-- Table structure for moviecol
-- ----------------------------
DROP TABLE IF EXISTS `moviecol`;
CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of moviecol
-- ----------------------------
BEGIN;
INSERT INTO `moviecol` VALUES (2, 4, 7, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (3, 4, 8, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (4, 4, 9, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (5, 4, 10, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (6, 4, 11, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (7, 4, 12, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (8, 4, 13, '2018-05-18 21:21:36');
INSERT INTO `moviecol` VALUES (9, 4, 18, '2018-05-23 23:40:38');
INSERT INTO `moviecol` VALUES (10, 5, 18, '2018-05-23 23:42:30');
INSERT INTO `moviecol` VALUES (11, 4, 19, '2018-05-24 23:51:22');
COMMIT;

-- ----------------------------
-- Table structure for oplog
-- ----------------------------
DROP TABLE IF EXISTS `oplog`;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `reason` varchar(600) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of oplog
-- ----------------------------
BEGIN;
INSERT INTO `oplog` VALUES (1, 1, '127.0.0.1', '添加预告中国画', '2018-05-23 11:07:53');
INSERT INTO `oplog` VALUES (2, 1, '127.0.0.1', '添加预告中国水墨', '2018-05-23 11:08:25');
INSERT INTO `oplog` VALUES (3, 1, '127.0.0.1', '添加预告儿童节', '2018-05-23 15:59:10');
INSERT INTO `oplog` VALUES (4, 1, '127.0.0.1', '添加预告音乐', '2018-05-23 15:59:40');
INSERT INTO `oplog` VALUES (5, 1, '127.0.0.1', '添加预告专辑', '2018-05-23 15:59:49');
INSERT INTO `oplog` VALUES (6, 1, '127.0.0.1', '添加电影水墨山水', '2018-05-23 17:30:19');
INSERT INTO `oplog` VALUES (7, 1, '127.0.0.1', '添加电影我就是试试', '2018-05-23 17:33:10');
INSERT INTO `oplog` VALUES (8, 1, '127.0.0.1', '添加标签好莱坞', '2018-05-25 00:00:32');
INSERT INTO `oplog` VALUES (9, 1, '127.0.0.1', '修改电影我就是试试', '2018-05-25 00:00:55');
COMMIT;

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `logo` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of preview
-- ----------------------------
BEGIN;
INSERT INTO `preview` VALUES (1, '中国画', '201805231107525a896f570a79447fbf36ff2e8bcb0326.jpg', '2018-05-23 11:07:53');
INSERT INTO `preview` VALUES (2, '中国水墨', '20180523110825727536ba943446b8aabfb1e8b344c340.png', '2018-05-23 11:08:25');
INSERT INTO `preview` VALUES (3, '儿童节', '20180523155910095688e9166949b4a33ea4a7172ddb91.jpg', '2018-05-23 15:59:10');
INSERT INTO `preview` VALUES (4, '音乐', '2018052315593929d7c72830934ecfa8c6c41ab4693f2b.jpg', '2018-05-23 15:59:40');
INSERT INTO `preview` VALUES (5, '专辑', '20180523155949d16d9b2de0604db48c42b9cdaafccb47.jpg', '2018-05-23 15:59:49');
COMMIT;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `auths` varchar(600) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES (1, '标签管理员', '1,2', '2018-05-19 16:42:07');
INSERT INTO `role` VALUES (2, '测试人员', '4', '2018-05-19 16:42:27');
INSERT INTO `role` VALUES (3, '系统管理员', '1,2,3,4,5,6,7,8,9,10,11', '2018-05-20 16:42:27');
COMMIT;

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of tag
-- ----------------------------
BEGIN;
INSERT INTO `tag` VALUES (1, '动作', '2018-05-08 22:05:59');
INSERT INTO `tag` VALUES (2, '青春', '2018-05-08 22:48:50');
INSERT INTO `tag` VALUES (3, '中国风', '2018-05-09 21:31:28');
INSERT INTO `tag` VALUES (4, '好莱坞', '2018-05-24 23:58:06');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `pwd` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `email` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `phone` varchar(11) COLLATE utf8mb4_bin DEFAULT NULL,
  `info` text COLLATE utf8mb4_bin,
  `face` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (6, '鼠', '1231', '1231@123.com', '13888888881', '鼠', '1f401.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc0');
INSERT INTO `user` VALUES (7, '牛', '1232', '1232@123.com', '13888888882', '牛', '1f402.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc1');
INSERT INTO `user` VALUES (8, '虎', '1233', '1233@123.com', '13888888883', '虎', '1f405.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc2');
INSERT INTO `user` VALUES (9, '兔', '1234', '1234@123.com', '13888888884', '兔', '1f407.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc3');
INSERT INTO `user` VALUES (10, '龙', '1235', '1235@123.com', '13888888885', '龙', '1f409.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc4');
INSERT INTO `user` VALUES (11, '蛇', '1236', '1236@123.com', '13888888886', '蛇', '1f40d.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc5');
INSERT INTO `user` VALUES (12, '马', '1237', '1237@123.com', '13888888887', '马', '1f434.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc6');
INSERT INTO `user` VALUES (13, '羊', '1238', '1238@123.com', '13888888888', '羊', '1f411.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc7');
INSERT INTO `user` VALUES (14, '猴', '1239', '1239@123.com', '13888888889', '猴', '1f412.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc8');
INSERT INTO `user` VALUES (15, '鸡', '1240', '1240@123.com', '13888888891', '鸡', '1f413.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fc9');
INSERT INTO `user` VALUES (16, '狗', '1241', '1241@123.com', '13888888892', '狗', '1f415.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fd0');
INSERT INTO `user` VALUES (17, '猪', '1242', '1242@123.com', '13888888893', '猪', '1f416.png', '2018-05-18 20:30:22', 'd32a72bdac524478b7e4f6dfc8394fd1');
INSERT INTO `user` VALUES (18, 'hanxx', 'pbkdf2:sha256:50000$QGdW9vJL$4225cad8cc9e3541568e46bf12bfd1a9ef77a2b1f7692f86eec5445ad0b729c0', '361967890@qq.com', '15510164680', '好人', '20180523095141ee10f61d0be54727a734fb8c0d6d86db.jpg', '2018-05-22 20:25:49', '0604a51d316547ac9a190a4efec41477');
INSERT INTO `user` VALUES (19, 'java', 'pbkdf2:sha256:50000$uZ255sne$225066a53bf68fe56bb2fcb368e1038f260119e290513c985c036b753615fa36', 'java@java.com', '15510101010', '', '201805242358416b9b24b019144421bea112cc6eaa0fea.png', '2018-05-24 23:33:34', '7b5de44d375e411690f23c74d0cf265c');
COMMIT;

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(12) COLLATE utf8mb4_bin DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of userlog
-- ----------------------------
BEGIN;
INSERT INTO `userlog` VALUES (1, 18, '127.0.0.1', '2018-05-22 20:33:02');
INSERT INTO `userlog` VALUES (2, 18, '127.0.0.1', '2018-05-22 22:26:20');
INSERT INTO `userlog` VALUES (3, 18, '127.0.0.1', '2018-05-23 09:43:22');
INSERT INTO `userlog` VALUES (4, 18, '127.0.0.1', '2018-05-23 10:28:40');
INSERT INTO `userlog` VALUES (5, 18, '127.0.0.1', '2018-05-23 22:21:00');
INSERT INTO `userlog` VALUES (6, 19, '127.0.0.1', '2018-05-24 23:33:34');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
