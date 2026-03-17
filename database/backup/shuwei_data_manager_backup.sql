-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: shuwei_data_manager
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `shuwei_data_manager`
--

/*!40000 DROP DATABASE IF EXISTS `shuwei_data_manager`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `shuwei_data_manager` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `shuwei_data_manager`;

--
-- Table structure for table `channel_user_relations`
--

DROP TABLE IF EXISTS `channel_user_relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `channel_user_relations` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '?? ID',
  `channel_id` int NOT NULL COMMENT '?? ID',
  `user_id` int NOT NULL COMMENT '?? ID',
  `relation_type` enum('direct','indirect') DEFAULT 'direct' COMMENT '??????',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_channel_user` (`channel_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `channel_user_relations_ibfk_1` FOREIGN KEY (`channel_id`) REFERENCES `channels` (`id`) ON DELETE CASCADE,
  CONSTRAINT `channel_user_relations_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='???????';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel_user_relations`
--

LOCK TABLES `channel_user_relations` WRITE;
/*!40000 ALTER TABLE `channel_user_relations` DISABLE KEYS */;
INSERT INTO `channel_user_relations` VALUES (1,1,2,'direct','2026-03-12 20:30:49'),(2,2,3,'direct','2026-03-12 20:30:49');
/*!40000 ALTER TABLE `channel_user_relations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channels`
--

DROP TABLE IF EXISTS `channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `channels` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'æ¸ é“ ID',
  `channel_name` varchar(100) NOT NULL COMMENT 'æ¸ é“åç§°',
  `channel_code` varchar(20) NOT NULL COMMENT 'æŽ¨èç ï¼ˆå”¯ä¸€ï¼‰',
  `contact_person` varchar(50) DEFAULT NULL COMMENT 'è”ç³»äºº',
  `contact_phone` varchar(20) DEFAULT NULL COMMENT 'è”ç³»ç”µè¯',
  `referred_users_count` int DEFAULT '0' COMMENT 'æŽ¨èç”¨æˆ·æ€»æ•°',
  `is_active` tinyint(1) DEFAULT '1' COMMENT 'æ˜¯å¦å¯ç”¨',
  `remark` text COMMENT 'å¤‡æ³¨',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'åˆ›å»ºæ—¶é—´',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'æ›´æ–°æ—¶é—´',
  PRIMARY KEY (`id`),
  UNIQUE KEY `channel_code` (`channel_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channels`
--

LOCK TABLES `channels` WRITE;
/*!40000 ALTER TABLE `channels` DISABLE KEYS */;
INSERT INTO `channels` VALUES (1,'????','OFFICIAL','?????','13800000000',1,1,'????','2026-03-12 20:30:49','2026-03-12 20:30:49'),(2,'???? A','PARTNER_A','??','13800000001',1,1,'??????','2026-03-12 20:30:49','2026-03-12 20:30:49'),(3,'???? B','PARTNER_B','??','13800000002',0,1,'??????','2026-03-12 20:30:49','2026-03-12 20:30:49');
/*!40000 ALTER TABLE `channels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation_results`
--

DROP TABLE IF EXISTS `evaluation_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluation_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '?? ID',
  `report_id` varchar(100) NOT NULL,
  `org_name` varchar(200) NOT NULL,
  `total_score` decimal(5,2) DEFAULT NULL,
  `maturity_level` varchar(50) DEFAULT NULL,
  `compliance_score` decimal(5,2) DEFAULT NULL,
  `quality_score` decimal(5,2) DEFAULT NULL,
  `rights_score` decimal(5,2) DEFAULT NULL,
  `value_score` decimal(5,2) DEFAULT NULL,
  `cost_score` decimal(5,2) DEFAULT NULL,
  `p0_issues` json DEFAULT NULL,
  `p1_issues` json DEFAULT NULL,
  `p2_issues` json DEFAULT NULL,
  `report_data` json DEFAULT NULL,
  `report_pdf_url` varchar(500) DEFAULT NULL COMMENT 'PDF ??????',
  `report_word_url` varchar(500) DEFAULT NULL COMMENT 'Word ??????',
  `generated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` tinyint(1) DEFAULT '0' COMMENT '????',
  PRIMARY KEY (`id`),
  UNIQUE KEY `report_id` (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation_results`
--

LOCK TABLES `evaluation_results` WRITE;
/*!40000 ALTER TABLE `evaluation_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluation_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_docs`
--

DROP TABLE IF EXISTS `knowledge_docs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledge_docs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doc_type` varchar(50) NOT NULL,
  `title` varchar(500) NOT NULL,
  `content` text NOT NULL,
  `tags` json DEFAULT NULL,
  `source` varchar(200) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_docs`
--

LOCK TABLES `knowledge_docs` WRITE;
/*!40000 ALTER TABLE `knowledge_docs` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_docs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rule_configs`
--

DROP TABLE IF EXISTS `rule_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rule_configs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dimension_code` varchar(50) NOT NULL,
  `rule_name` varchar(200) NOT NULL,
  `logic_expression` text NOT NULL,
  `weight` decimal(5,2) DEFAULT '0.00',
  `risk_threshold` decimal(5,2) DEFAULT '0.00',
  `is_active` tinyint(1) DEFAULT '1',
  `source_type` varchar(50) DEFAULT 'manual',
  `version` varchar(20) DEFAULT '1.0',
  `ai_prompt_context` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rule_configs`
--

LOCK TABLES `rule_configs` WRITE;
/*!40000 ALTER TABLE `rule_configs` DISABLE KEYS */;
INSERT INTO `rule_configs` VALUES (1,'C','C-01','sensitive_data == \"??????\"',30.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(2,'C','C-02','user_auth == \"????????',25.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(3,'C','C-03','data_encrypt == \"??',20.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(4,'C','C-04','security_cert == [\"??]',15.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(5,'C','C-05','data_policy == \"??',15.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(6,'C','C-06','compliance_history == \"?????????\"',30.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(7,'Q','Q-01','update_frequency in [\"?????????, \"???\"]',15.00,0.70,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(8,'Q','Q-02','completeness < 80',25.00,0.60,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(9,'Q','Q-03','len(data_format) <= 1',10.00,0.80,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(10,'O','O-01','\"?? in rights_cert',40.00,1.00,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(11,'O','O-02','originality == \"??(?????????)\"',20.00,0.50,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(12,'O','O-03','cost_accounting == \"??????\"',15.00,0.60,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(13,'V','V-01','len(application_scenario) <= 1',15.00,0.70,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(14,'V','V-02','len(pain_points) >= 3',20.00,0.60,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(15,'V','V-03','len(asset_purpose) <= 1',15.00,0.70,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(16,'CO','CO-01','cost_input < 50',20.00,0.50,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(17,'CO','CO-02','commercial_plan == \"??',25.00,0.60,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41'),(18,'CO','CO-03','expected_revenue < 100',15.00,0.70,1,'manual','1.0',NULL,'2026-03-12 17:59:41','2026-03-12 17:59:41');
/*!40000 ALTER TABLE `rule_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '?? ID',
  `username` varchar(50) NOT NULL COMMENT '???',
  `password_hash` varchar(255) NOT NULL COMMENT '????',
  `email` varchar(100) DEFAULT NULL COMMENT '??',
  `phone` varchar(20) DEFAULT NULL COMMENT '???',
  `referrer_code` varchar(20) DEFAULT NULL COMMENT '??????????',
  `channel_id` int DEFAULT NULL COMMENT '???? ID',
  `user_type` enum('client','admin','channel') DEFAULT 'client' COMMENT '????',
  `is_vip` tinyint(1) DEFAULT '0' COMMENT '?? VIP',
  `vip_expire_date` date DEFAULT NULL COMMENT 'VIP ????',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '????',
  `last_login_at` timestamp NULL DEFAULT NULL COMMENT '??????',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '????',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `channel_id` (`channel_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`channel_id`) REFERENCES `channels` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='???';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu','admin@shuwei.com','13800000000',NULL,NULL,'admin',0,NULL,1,NULL,'2026-03-12 20:30:49','2026-03-12 20:30:49'),(2,'test_user','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu','test@test.com','13800000001','OFFICIAL',1,'client',0,NULL,1,NULL,'2026-03-12 20:30:49','2026-03-12 20:30:49'),(3,'vip_user','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu','vip@test.com','13800000002','PARTNER_A',2,'client',1,'2027-03-12',1,NULL,'2026-03-12 20:30:49','2026-03-12 20:30:49');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'shuwei_data_manager'
--

--
-- Dumping routines for database 'shuwei_data_manager'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-12 22:42:22
