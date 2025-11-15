-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: foodmanagementdb
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `allergens`
--

DROP TABLE IF EXISTS `allergens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `allergens` (
  `allergen_id` int NOT NULL AUTO_INCREMENT,
  `allergen_name` varchar(50) NOT NULL,
  PRIMARY KEY (`allergen_id`),
  UNIQUE KEY `allergen_name` (`allergen_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `allergens`
--

LOCK TABLES `allergens` WRITE;
/*!40000 ALTER TABLE `allergens` DISABLE KEYS */;
/*!40000 ALTER TABLE `allergens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foodinventory`
--

DROP TABLE IF EXISTS `foodinventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foodinventory` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `item_name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `quantity` int DEFAULT '0',
  `weight` varchar(20) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foodinventory`
--

LOCK TABLES `foodinventory` WRITE;
/*!40000 ALTER TABLE `foodinventory` DISABLE KEYS */;
INSERT INTO `foodinventory` VALUES (1,'Chicken Soup','Soup',0,'15 oz','2025-10-18 23:52:22'),(2,'Tomato Soup','Soup',99,'15 oz','2025-11-15 20:34:04'),(3,'Vegetable Soup','Soup',98,'15 oz','2025-11-10 19:19:02'),(4,'Vegetarian Soup','Soup',97,'15 oz','2025-11-10 19:19:02'),(5,'Beef Stew','Soup',100,'15 oz','2025-10-17 22:45:10'),(6,'Chili','Soup',98,'15 oz','2025-11-03 02:29:56'),(7,'Cream','Soup',99,'15 oz','2025-11-03 02:29:56'),(8,'Chicken Broth','Broth/Boullion',100,'32 oz','2025-10-17 22:45:10'),(9,'Beef Broth','Broth/Boullion',100,'32 oz','2025-10-17 22:45:10'),(10,'Vegetable Broth','Broth/Boullion',99,'32 oz','2025-11-03 02:09:21'),(11,'Chicken Ramen','Ramen',100,'3 oz','2025-10-17 22:45:10'),(12,'Beef Ramen','Ramen',100,'3 oz','2025-10-17 22:45:10'),(13,'Chicken','Canned Meat/Fish',100,'5 oz','2025-10-17 22:45:10'),(14,'Tuna','Canned Meat/Fish',100,'5 oz','2025-10-17 22:45:10'),(15,'Sardines','Canned Meat/Fish',100,'4 oz','2025-10-17 22:45:10'),(16,'Spam','Canned Meat/Fish',100,'12 oz','2025-10-17 22:45:10'),(17,'Vienna','Canned Meat/Fish',100,'5 oz','2025-10-17 22:45:10'),(18,'Cereal','Cereal/Breakfast',100,'12 oz','2025-10-17 22:45:10'),(19,'Oatmeal','Cereal/Breakfast',100,'10 oz','2025-10-17 22:45:10'),(20,'Pop Tarts','Cereal/Breakfast',100,'14 oz','2025-10-17 22:45:10'),(21,'Nut Butter','Cereal/Breakfast',100,'16 oz','2025-10-17 22:45:10'),(22,'Jelly','Cereal/Breakfast',100,'18 oz','2025-10-17 22:45:10'),(23,'Apple Butter','Cereal/Breakfast',100,'17 oz','2025-10-17 22:45:10'),(24,'Boxed Milk','Cereal/Breakfast',100,'32 oz','2025-10-17 22:45:10'),(25,'Green Beans','Canned Vegetables',100,'15 oz','2025-10-17 22:45:10'),(26,'Peas','Canned Vegetables',100,'15 oz','2025-10-17 22:45:10'),(27,'Corn','Canned Vegetables',100,'15 oz','2025-10-17 22:45:10'),(28,'Diced Tomatoes','Canned Vegetables',100,'14 oz','2025-11-03 03:16:01'),(29,'Carrots','Canned Vegetables',100,'15 oz','2025-10-17 22:45:10'),(30,'Greens','Canned Vegetables',100,'15 oz','2025-10-17 22:45:10'),(31,'Beets','Canned Vegetables',100,'15 oz','2025-10-17 22:45:10'),(32,'Black Olives','Canned Vegetables',100,'3 oz','2025-11-03 03:16:01'),(33,'Black Beans','Beans',100,'15 oz','2025-10-17 22:45:10'),(34,'Kidney Beans','Beans',100,'15 oz','2025-10-17 22:45:10'),(35,'White Beans','Beans',100,'15 oz','2025-10-17 22:45:10'),(36,'Chickpeas','Beans',100,'15 oz','2025-10-17 22:45:10'),(37,'Pinto Beans','Beans',99,'15 oz','2025-11-03 02:09:37'),(38,'Refried Beans','Beans',100,'16 oz','2025-10-17 22:45:10'),(39,'Baked Beans','Beans',100,'16 oz','2025-11-15 21:09:00'),(40,'Ketchup','Sauces/Condiments',100,'20 oz','2025-10-17 22:45:10'),(41,'Tomato Sauce','Sauces/Condiments',100,'15 oz','2025-10-17 22:45:10'),(42,'Salsa','Sauces/Condiments',100,'16 oz','2025-10-17 22:45:10'),(43,'Alfredo Sauce','Sauces/Condiments',100,'15 oz','2025-10-17 22:45:10'),(44,'Salad Dressing','Sauces/Condiments',100,'16 oz','2025-10-17 22:45:10'),(45,'Cran Sauce','Other',100,'14 oz','2025-10-17 22:45:10'),(46,'Pumpkin','Other',100,'15 oz','2025-10-17 22:45:10'),(47,'Granola Bars','Snacks',100,'8 oz','2025-10-17 22:45:10'),(48,'Crackers','Snacks',100,'10 oz','2025-10-17 22:45:10'),(49,'Chips','Snacks',100,'9 oz','2025-10-17 22:45:10'),(50,'Pretzels','Snacks',100,'12 oz','2025-10-17 22:45:10'),(51,'Microwave Popcorn','Snacks',100,'9 oz','2025-10-17 22:45:10'),(52,'Fruit Cups','Snacks',100,'4 oz','2025-10-17 22:45:10'),(53,'Applesauce','Snacks',100,'12 oz','2025-10-17 22:45:10'),(54,'Dry Pasta','Pasta',100,'16 oz','2025-10-17 22:45:10'),(55,'Canned Meat Pasta','Pasta',100,'15 oz','2025-10-17 22:45:10'),(56,'Canned Veg Pasta','Pasta',100,'15 oz','2025-10-17 22:45:10'),(57,'Macaroni & Cheese','Pasta',100,'7 oz','2025-10-17 22:45:10'),(58,'Egg Noodles','Pasta',100,'12 oz','2025-10-17 22:45:10'),(59,'Flavored Noodle Side','Pasta',100,'5 oz','2025-10-17 22:48:21'),(60,'White Rice','Rice/Potatoes',100,'16 oz','2025-10-17 22:45:10'),(61,'Brown Rice','Rice/Potatoes',99,'16 oz','2025-11-03 02:23:23'),(62,'Flavored Rice Side','Rice/Potatoes',100,'5 oz','2025-10-17 22:49:21'),(63,'Canned Potatoes','Rice/Potatoes',100,'15 oz','2025-10-17 22:45:10'),(64,'Instant Potatoes','Rice/Potatoes',99,'13 oz','2025-11-15 20:34:04'),(65,'Quinoa','Rice/Potatoes',100,'12 oz','2025-10-17 22:45:10'),(66,'Ground Coffee','Drinks',100,'12 oz','2025-10-17 22:45:10'),(67,'Black Tea','Drinks',100,'2 oz','2025-10-17 22:45:10'),(68,'Herbal Tea','Drinks',100,'2 oz','2025-10-17 22:45:10'),(69,'Iced Tea','Drinks',100,'8 oz','2025-10-17 22:45:10'),(70,'Drink Sticks','Drinks',100,'5 oz','2025-10-17 22:45:10'),(71,'Fruit Juice','Drinks',100,'64 oz','2025-10-17 22:45:10');
/*!40000 ALTER TABLE `foodinventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logins`
--

DROP TABLE IF EXISTS `logins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logins` (
  `user_id` varchar(15) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','staff','student','newUser') DEFAULT 'newUser',
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logins`
--

LOCK TABLES `logins` WRITE;
/*!40000 ALTER TABLE `logins` DISABLE KEYS */;
INSERT INTO `logins` VALUES ('admin1','$argon2id$v=19$m=65536,t=3,p=4$m85MFxVLdNSyVSWabmqFHw$uMA/OkLDgtlr+vXskthVugVdP4gJD7DZ9K8YXSqcdAw','admin',NULL,NULL,NULL,'2025-10-04 03:03:31'),('MT-24239014','$argon2id$v=19$m=65536,t=3,p=4$U7185bmcuRA7lkKmTJZuOw$rpsrBjqFOFie/QplYXp0aMtUX/lplX8DA3k68zmIL6E','student','steph','z','zs@email.msmary.edu','2025-11-10 00:25:22'),('MT-27610845','$argon2id$v=19$m=65536,t=3,p=4$7vumm3JdD5qN5C1nw/3Q4w$9zC73Aodo3lCFQEUxvJPXa5o5QcQM9W+/3SHLDtFVYs','student','tyler','woo','tw@email.msmary.edu','2025-11-10 05:12:07'),('MT-50965481','$argon2id$v=19$m=65536,t=3,p=4$3jHgiiiZsfrtz+j7JvGMcA$Q1n5pkY+NkpCp7TFSv1UjBi+XNhPu8e0WAeO8ylv+C8','student','Thomas','Saldari','t.e.saldari@email.msmary.edu','2025-10-04 03:32:27'),('MT-74329803','$argon2id$v=19$m=65536,t=3,p=4$zN2ujfMe8Ap+4RMGIbjUcA$yw6rFzSZj/zVCfk2JItiGhfPMPmcM0nvtussQNvP3/k','student','John','Doe','JohnDoe@email.msmary.edu','2025-10-27 04:26:37'),('MT-75583182','$argon2id$v=19$m=65536,t=3,p=4$SFEpsATX7YqXy+SeJq0Uiw$4C0gUnYXmH/yxGhOkEK1UGuarhw84S0Cc+4knRfsIYg','newUser','john','smith','jsmith@email.msmary.edu','2025-11-03 01:15:54'),('MT-89198008','$argon2id$v=19$m=65536,t=3,p=4$8ZNI6XehqmXTcVFOYS3XLw$cgQsMz9zlh7XYB3GrJ/xmzbWTyTdL8hW9eAdEjcBRT0','student','Jane','Doe','JaneDoe@email.msmary.edu','2025-10-27 18:15:23'),('student1','$argon2id$v=19$m=65536,t=3,p=4$m85MFxVLdNSyVSWabmqFHw$uMA/OkLDgtlr+vXskthVugVdP4gJD7DZ9K8YXSqcdAw','student',NULL,NULL,NULL,'2025-10-04 03:03:07');
/*!40000 ALTER TABLE `logins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request_items`
--

DROP TABLE IF EXISTS `request_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_items` (
  `request_id` int NOT NULL,
  `item_id` int NOT NULL,
  PRIMARY KEY (`request_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `request_items_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `requests` (`request_id`),
  CONSTRAINT `request_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `foodinventory` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request_items`
--

LOCK TABLES `request_items` WRITE;
/*!40000 ALTER TABLE `request_items` DISABLE KEYS */;
INSERT INTO `request_items` VALUES (2,1),(2,2),(3,2),(4,2),(5,2),(2,3),(3,3),(4,3),(7,3),(11,3),(12,3),(6,4),(7,4),(8,4),(9,4),(11,4),(2,6),(6,6),(7,6),(2,7),(7,7),(2,8),(2,9),(2,10),(2,11),(2,12),(2,13),(2,16),(12,16),(2,17),(12,17),(2,18),(2,20),(10,20),(2,22),(2,23),(2,24),(2,25),(2,26),(2,27),(2,28),(2,29),(2,30),(2,31),(2,32),(2,33),(2,34),(2,35),(2,36),(2,37),(2,38),(2,39),(2,40),(2,41),(2,42),(2,43),(2,44),(2,45),(2,46),(2,47),(2,48),(2,49),(12,49),(2,50),(2,51),(2,52),(2,53),(2,54),(2,55),(2,56),(2,57),(2,58),(2,59),(2,60),(2,61),(6,61),(2,62),(2,63),(2,64),(5,64),(2,65),(2,66),(2,67),(2,68),(2,69),(2,70),(2,71);
/*!40000 ALTER TABLE `request_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requests`
--

DROP TABLE IF EXISTS `requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) DEFAULT NULL,
  `request_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','approved','denied') DEFAULT 'pending',
  `admin_note` text,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requests`
--

LOCK TABLES `requests` WRITE;
/*!40000 ALTER TABLE `requests` DISABLE KEYS */;
INSERT INTO `requests` VALUES (1,'student1','2025-10-14 23:47:07','approved',NULL),(2,'student1','2025-10-17 22:53:02','pending',NULL),(3,'MT-74329803','2025-10-27 04:36:00','approved',NULL),(4,'MT-74329803','2025-10-27 04:37:02','pending',NULL),(5,'MT-74329803','2025-10-27 04:38:19','approved','Sorry we had to remove an item, your order with everything else will be ready on 11/15 at 2pm. See you then!'),(6,'MT-89198008','2025-10-27 18:18:03','approved',NULL),(7,'MT-74329803','2025-11-03 02:29:38','approved',NULL),(8,'MT-24239014','2025-11-10 00:27:23','pending',NULL),(9,'MT-24239014','2025-11-10 00:27:34','pending',NULL),(10,'MT-74329803','2025-11-10 04:45:28','denied',NULL),(11,'MT-74329803','2025-11-10 19:16:36','approved',NULL),(12,'MT-74329803','2025-11-15 21:22:18','pending',NULL);
/*!40000 ALTER TABLE `requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userallergens`
--

DROP TABLE IF EXISTS `userallergens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userallergens` (
  `user_id` varchar(15) NOT NULL,
  `allergen_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`allergen_id`),
  KEY `allergen_id` (`allergen_id`),
  CONSTRAINT `userallergens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `logins` (`user_id`),
  CONSTRAINT `userallergens_ibfk_2` FOREIGN KEY (`allergen_id`) REFERENCES `allergens` (`allergen_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userallergens`
--

LOCK TABLES `userallergens` WRITE;
/*!40000 ALTER TABLE `userallergens` DISABLE KEYS */;
/*!40000 ALTER TABLE `userallergens` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-15 16:50:55
