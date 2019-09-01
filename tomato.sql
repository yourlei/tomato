-- MySQL dump 10.16  Distrib 10.3.10-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tomato
-- ------------------------------------------------------
-- Server version	10.3.10-MariaDB-1:10.3.10+maria~bionic-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('571d97ca50c0');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_article`
--

DROP TABLE IF EXISTS `tomato_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_article` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `title` varchar(128) NOT NULL COMMENT '标题',
  `content` text DEFAULT NULL COMMENT '文章内容',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL,
  `author` varchar(32) NOT NULL COMMENT '作者',
  `cid` char(16) DEFAULT NULL COMMENT '分类ID',
  `status` int(11) DEFAULT NULL COMMENT '文章状态1:已发布, 2:存为草稿',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_article`
--

LOCK TABLES `tomato_article` WRITE;
/*!40000 ALTER TABLE `tomato_article` DISABLE KEYS */;
INSERT INTO `tomato_article` VALUES ('259de04e0e9c8960','知青年代','<p>知青年代</p>','2019-08-24 14:55:00',NULL,'0000-01-01 00:00:00','tomato','kjfdflsjfldsj',1),('4682075a57b34813','linux防火墙','kljsjdfjdkjdkj','2019-07-28 13:47:44',NULL,'0000-01-01 00:00:00','tomato','6c25cd76877c2',NULL),('7026303e1bab0a94','tomato blog','<p>要做的事, 现在就得开始</p>','2019-08-21 15:29:17',NULL,'0000-01-01 00:00:00','tomato','kjfdflsjfldsj',1),('78a3b6f6f28aad23','彩虹','<p>遇见彩虹啊</p>','2019-08-29 10:40:51',NULL,'0000-01-01 00:00:00','tomato','kjfdflsjfldsj',0),('dfd48c8ee5107e8a','知青年代','<p>知青年代知青年代知青年代知青年代知青年代知青年代</p>','2019-08-25 10:34:10',NULL,'0000-01-01 00:00:00','tomato','kjfdflsjfldsj',0),('ea0994126e64964f','python 开发','kljsjdfjdkjdkj','2019-07-28 13:37:59','2019-08-18 11:35:21','2019-08-18 11:35:20','tomato','6c25cd76877c2462',NULL);
/*!40000 ALTER TABLE `tomato_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_category`
--

DROP TABLE IF EXISTS `tomato_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_category` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `name` varchar(32) NOT NULL COMMENT '类名',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_category`
--

LOCK TABLES `tomato_category` WRITE;
/*!40000 ALTER TABLE `tomato_category` DISABLE KEYS */;
INSERT INTO `tomato_category` VALUES ('6c25cd76877c2462','python','2019-07-28 08:19:30','2019-07-28 08:19:30','0000-01-01 00:00:00'),('ea72244adf8bb255','Linux','2019-07-28 03:36:42','2019-07-28 03:36:42','0000-01-01 00:00:00');
/*!40000 ALTER TABLE `tomato_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_comments`
--

DROP TABLE IF EXISTS `tomato_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_comments` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `comments` varchar(256) NOT NULL COMMENT '评论',
  `article_id` char(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `article_id` (`article_id`),
  CONSTRAINT `tomato_comments_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `tomato_article` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_comments`
--

LOCK TABLES `tomato_comments` WRITE;
/*!40000 ALTER TABLE `tomato_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `tomato_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_menu`
--

DROP TABLE IF EXISTS `tomato_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_menu` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `name` varchar(64) NOT NULL COMMENT '资源名',
  `url` varchar(128) NOT NULL COMMENT '页面路由',
  `sort` int(11) DEFAULT NULL COMMENT '菜单排序',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_menu`
--

LOCK TABLES `tomato_menu` WRITE;
/*!40000 ALTER TABLE `tomato_menu` DISABLE KEYS */;
/*!40000 ALTER TABLE `tomato_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_role`
--

DROP TABLE IF EXISTS `tomato_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_role` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `name` varchar(64) NOT NULL COMMENT '角色名称',
  `tag` int(11) NOT NULL COMMENT '角色类别',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_role`
--

LOCK TABLES `tomato_role` WRITE;
/*!40000 ALTER TABLE `tomato_role` DISABLE KEYS */;
INSERT INTO `tomato_role` VALUES ('20459894aee58f78','admin',1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `tomato_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_role_relationship`
--

DROP TABLE IF EXISTS `tomato_role_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_role_relationship` (
  `id` char(16) NOT NULL COMMENT '主键',
  `role_id` char(16) NOT NULL COMMENT '角色ID',
  `resource_id` int(11) NOT NULL COMMENT '资源ID',
  `from_id` int(11) NOT NULL COMMENT '区别资源类型,1菜单资源',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_role_relationship`
--

LOCK TABLES `tomato_role_relationship` WRITE;
/*!40000 ALTER TABLE `tomato_role_relationship` DISABLE KEYS */;
/*!40000 ALTER TABLE `tomato_role_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_tag`
--

DROP TABLE IF EXISTS `tomato_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_tag` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `name` varchar(32) NOT NULL COMMENT '标签名',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `deleted_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_tag`
--

LOCK TABLES `tomato_tag` WRITE;
/*!40000 ALTER TABLE `tomato_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tomato_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_tag_relationship`
--

DROP TABLE IF EXISTS `tomato_tag_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_tag_relationship` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `tid` char(16) NOT NULL COMMENT 'tag id',
  `aid` char(16) NOT NULL COMMENT 'article id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_tag_relationship`
--

LOCK TABLES `tomato_tag_relationship` WRITE;
/*!40000 ALTER TABLE `tomato_tag_relationship` DISABLE KEYS */;
/*!40000 ALTER TABLE `tomato_tag_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tomato_user`
--

DROP TABLE IF EXISTS `tomato_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tomato_user` (
  `id` char(16) NOT NULL COMMENT '唯一id',
  `role_id` char(16) NOT NULL,
  `name` varchar(64) NOT NULL COMMENT '用户名称',
  `email` varchar(64) NOT NULL COMMENT '注册邮箱',
  `password` varchar(128) NOT NULL COMMENT '账户密码',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `tomato_user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `tomato_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tomato_user`
--

LOCK TABLES `tomato_user` WRITE;
/*!40000 ALTER TABLE `tomato_user` DISABLE KEYS */;
INSERT INTO `tomato_user` VALUES ('80643aba3978c58e','20459894aee58f78','devp','dev@dev.com','$2b$10$c1J.gybx2C1NeDu3xYT6tOckuaTuAWaDRUBBefbyFaiAv.nZTo6vy','2019-07-27 11:34:31','2019-07-27 12:59:51','0000-01-01 00:00:00'),('84320f86496fdcbb','20459894aee58f78','tomato','tomato@qq.com','$2b$10$hM5egHKfXS.LAv6lw1CG5u.OvXxpLFeDVZ./x8e146/f7v8nDWPtO','2019-07-21 09:32:54','2019-07-27 10:07:54','0000-01-01 00:00:00');
/*!40000 ALTER TABLE `tomato_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-30 16:42:32
