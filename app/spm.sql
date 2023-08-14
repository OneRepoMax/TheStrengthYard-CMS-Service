-- !!!FOR REFERENCE ONLY!!!------
-- Below is CLI command to import sql data into local MySQL db (TO-RUN from /spm-backend dir):
-- mysql -uroot < app/spm.sql

-- MySQL dump 10.13  Distrib 8.0.28, for macos12.0 (arm64)
--
-- Host: spm-db.c300l1maonyq.ap-southeast-1.rds.amazonaws.com    Database: spm_db
-- ------------------------------------------------------
-- Server version	8.0.28

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
-- SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

-- SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Current Database: `spm_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `spm_db` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `spm_db`;

--
-- Table structure for table `Access_Role`
--

DROP TABLE IF EXISTS `Access_Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Access_Role` (
  `Role_ID` int NOT NULL AUTO_INCREMENT,
  `Role_Name` varchar(20) NOT NULL,
  PRIMARY KEY (`Role_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Access_Role`
--

LOCK TABLES `Access_Role` WRITE;
/*!40000 ALTER TABLE `Access_Role` DISABLE KEYS */;
INSERT INTO `Access_Role` VALUES (1,'Admin'),(2,'User'),(3,'Manager'),(4,'Trainer');
/*!40000 ALTER TABLE `Access_Role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Course`
--

DROP TABLE IF EXISTS `Course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Course` (
  `Course_ID` varchar(20) NOT NULL,
  `Course_Name` varchar(45) NOT NULL,
  `Course_Desc` varchar(255) NOT NULL,
  `Course_Type` varchar(10) NOT NULL,
  `Course_Status` varchar(15) NOT NULL,
  `Course_Category` varchar(50) NOT NULL,
  PRIMARY KEY (`Course_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Course`
--

LOCK TABLES `Course` WRITE;
/*!40000 ALTER TABLE `Course` DISABLE KEYS */;
INSERT INTO `Course` VALUES ('COR001','Systems Thinking and Design','This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking','Internal','Active','Core'),('COR002','Lean Six Sigma Green Belt Certification','Apply Lean Six Sigma methodology and statistical tools such as Minitab to be used in process analytics','Internal','Active','Core'),('COR004','Service Excellence','The programme provides the learner with the key foundations of what builds customer confidence in the service industr','Internal','Pending','Core'),('COR006','Manage Change','Identify risks associated with change and develop risk mitigation plans.','External','Retired','Core'),('FIN001','Data Collection and Analysis','Data is meaningless unless insights and analysis can be drawn to provide useful information for business decision-making. It is imperative that data quality, integrity and security ','External','Active','Finance'),('FIN002','Risk and Compliance Reporting','Regulatory reporting is a requirement for businesses from highly regulated sectors to demonstrate compliance with the necessary regulatory provisions.','External','Active','Finance'),('FIN003','Business Continuity Planning','Business continuity planning is essential in any business to minimise loss when faced with potential threats and disruptions.','External','Retired','Finance'),('HRD001','Leading and Shaping a Culture in Learning','This training programme, delivered by the National Centre of Excellence (Workplace Learning), aims to equip participants with the skills and knowledge of the National workplace learning certification framework,','External','Active','HR'),('MGT001','People Management','enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.','Internal','Active','Management'),('MGT002','Workplace Conflict Management for Professiona','This course will address the gaps to build consensus and utilise knowledge of conflict management techniques to diffuse tensions and achieve resolutions effectively in the best interests of the organisation.','External','Active','Management'),('MGT003','Enhance Team Performance Through Coaching','The course aims to upskill real estate team leaders in the area of service coaching for performance.','Internal','Pending','Management'),('MGT004','Personal Effectiveness for Leaders','Learners will be able to acquire the skills and knowledge to undertake self-assessment in relation to oneís performance and leadership style','External','Active','Management'),('MGT007','Supervisory Management Skills','Supervisors lead teams, manage tasks, solve problems, report up and down the hierarchy, and much more. ','External','Retired','Management'),('SAL001','Risk Management for Smart Business','Apply risk management concepts to digital business','Internal','Retired','Sales'),('SAL002','CoC in Smart Living Solutions','Participants will acquire the knowledge and skills in setting up a smart living solution','External','Pending','Sales'),('SAL003','Optimising Your Brand For The Digital Spaces','Digital has fundamentally shifted communication between brands and their consumers from a one-way broadcast to a two-way dialogue. In a hastened bid to transform their businesses to be digital market-ready,','External','Active','Sales'),('SAL004','Stakeholder Management','Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.','Internal','Active','Sales'),('tch001','Print Server Setup','Setting up print server in enterprise environment','Internal','Retired','Technical'),('tch002','Canon MFC Setup','Setting up Canon ImageRUNNER series of products','Internal','Retired','Technical'),('tch003','Canon MFC Mainteance and Troubleshooting','Troubleshoot and fixing L2,3 issues of Canon ImageRUNNER series of products','Internal','Active','Technical'),('tch004','Introduction to Open Platform Communications','This course provides the participants with a good in-depth understanding of the SS IEC 62541 standard','Internal','Pending','Technical'),('tch005','An Introduction to Sustainability','The course provides learners with the multi-faceted basic knowledge of sustainability.','External','Active','Technical'),('tch006','Machine Learning DevOps Engineer','The Machine Learning DevOps Engineer Nanodegree program focuses on the software engineering fundamentals needed to successfully streamline the deployment of data and machine-learning models','Internal','Pending','Technical'),('tch008','Technology Intelligence and Strategy','Participants will be able to gain knowledge and skills on: - establishing technology strategy with technology intelligence framework and tools','External','Active','Technical'),('tch009','Smart Sensing Technology','This course introduces sensors and sensing systems. The 5G infrastructure enables the many fast-growing IoT applications equipped with sensors ','External','Pending','Technical'),('tch012','Internet of Things','The Internet of Things (IoT) is integrating our digital and physical world, opening up new and exciting opportunities to deploy, automate, optimize and secure diverse use cases and applications. ','Internal','Active','Technical'),('tch013','Managing Cybersecurity and Risks','Digital security is the core of our daily lives considering that our dependence on the digital world','Internal','Active','Technical'),('tch014','Certified Information Privacy Professional','The Certified Information Privacy Professional/ Asia (CIPP/A) is the first publicly available privacy certification','External','Active','Technical'),('tch015','Network Security','Understanding of the fundamental knowledge of network security including cryptography, authentication and key distribution. The security techniques at various layers of computer networks are examined.','External','Active','Technical'),('tch018','Professional Project Management','solid foundation in the project management processes from initiating a project, through planning, execution, control,','Internal','Active','Technical'),('tch019','Innovation and Change Management','the organization that constantly reinvents itself to be relevant has a better chance of making progress','External','Active','Technical');
/*!40000 ALTER TABLE `Course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Course_has_Skill`
--

DROP TABLE IF EXISTS `Course_has_Skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Course_has_Skill` (
  `Skill_ID` int NOT NULL,
  `Course_ID` varchar(20) NOT NULL,
  KEY `Course_ID` (`Course_ID`),
  KEY `Skill_ID` (`Skill_ID`),
  CONSTRAINT `Course_has_Skill_ibfk_1` FOREIGN KEY (`Course_ID`) REFERENCES `Course` (`Course_ID`),
  CONSTRAINT `Course_has_Skill_ibfk_2` FOREIGN KEY (`Skill_ID`) REFERENCES `Skill` (`Skill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Course_has_Skill`
--

LOCK TABLES `Course_has_Skill` WRITE;
/*!40000 ALTER TABLE `Course_has_Skill` DISABLE KEYS */;
INSERT INTO `Course_has_Skill` VALUES (1,'COR001'),(2,'COR001'),(1,'COR002'),(2,'COR002'),(3,'COR002'),(3,'FIN001'),(3,'SAL002'),(2,'MGT004'),(3,'tch013'),(5,'tch008'),(3,'MGT003'),(8,'tch002'),(6,'tch012'),(6,'tch019'),(8,'tch004'),(7,'tch001'),(2,'HRD001'),(0,'FIN001'),(3,'tch005'),(2,'tch009'),(2,'tch015'),(6,'FIN003'),(8,'SAL002'),(7,'MGT002'),(1,'SAL003'),(6,'tch006'),(7,'COR001'),(4,'SAL004'),(3,'tch014'),(2,'COR006'),(9,'MGT007'),(0,'MGT001'),(7,'tch018'),(4,'SAL001');
/*!40000 ALTER TABLE `Course_has_Skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Job_Role`
--

DROP TABLE IF EXISTS `Job_Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Job_Role` (
  `Job_ID` int NOT NULL AUTO_INCREMENT,
  `Job_Role` varchar(20) NOT NULL,
  `Job_Title` varchar(20) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Description` TEXT NOT NULL,
  PRIMARY KEY (`Job_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=220 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Job_Role`
--

LOCK TABLES `Job_Role` WRITE;
/*!40000 ALTER TABLE `Job_Role` DISABLE KEYS */;
INSERT INTO `Job_Role` VALUES (1,'Operation Slave','Staff','Operations','Slavery is no go. Please promote me'),(2,'Sales Manager','Manager','Sales',''),(3,'Sales Rep','Staff','Sales',''),(4,'Operation Manager','Manager','Operations',''),(5,'Repair Engineer','Staff','Operations',''),(6,'Senior Roving Service','Staff','Operations',''),(7,'Junior Roving Service','Staff','Operations',''),(8,'HR and Admin Manager','Manager','HR and Admin',''),(9,'Operation Planning','Staff','HR and Admin',''),(10,'Admin and Call Cente','Staff','HR and Admin',''),(11,'Finance Manager','Manager','Finance',''),(12,'Finance Executive','Staff','Finance',''),(13,'Managing Director','Director','Executive Management','test');
/*!40000 ALTER TABLE `Job_Role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Learning_Journey`
--

DROP TABLE IF EXISTS `Learning_Journey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Learning_Journey` (
  `Learning_Journey_ID` int NOT NULL AUTO_INCREMENT,
  `Learning_Journey_Name` varchar(45) NOT NULL,
  `Staff_ID` int NOT NULL,
  `Description` TEXT DEFAULT NULL,
  `Job_Role_ID` int NOT NULL,
  PRIMARY KEY (`Learning_Journey_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Learning_Journey`
--

LOCK TABLES `Learning_Journey` WRITE;
/*!40000 ALTER TABLE `Learning_Journey` DISABLE KEYS */;
INSERT INTO `Learning_Journey` VALUES (1,'10:13pm 17 Oct --- Learning Journey for GODS',1,'test data',1),(2,'Learning Journey for Dummies (Sales Role) -- ',1,'lorem ipsum for dummies I HATE SALES',2),(3,'Advanced Learning Journey',2,'updateds',3);
INSERT INTO `Learning_Journey` VALUES (4,'10:13pm 17 Oct --- Learning Journey for GODS',140002,'just test journey journey',1),(5,'Learning Journey for Dummies (Sales Role) -- ',140002,'lorem ipsum for dummies I HATE SALES',2),(6,'Advanced Learning Journey',140002,'updateds',3);
/*!40000 ALTER TABLE `Learning_Journey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Learning_Journey_has_Course`
--

DROP TABLE IF EXISTS `Learning_Journey_has_Course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Learning_Journey_has_Course` (
  `Course_ID` varchar(20) NOT NULL,
  `Learning_Journey_ID` int NOT NULL,
  PRIMARY KEY (`Course_ID`,`Learning_Journey_ID`),
  KEY `Learning_Journey_ID` (`Learning_Journey_ID`),
  CONSTRAINT `Learning_Journey_has_Course_ibfk_1` FOREIGN KEY (`Course_ID`) REFERENCES `Course` (`Course_ID`),
  CONSTRAINT `Learning_Journey_has_Course_ibfk_2` FOREIGN KEY (`Learning_Journey_ID`) REFERENCES `Learning_Journey` (`Learning_Journey_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Learning_Journey_has_Course`
--

LOCK TABLES `Learning_Journey_has_Course` WRITE;
/*!40000 ALTER TABLE `Learning_Journey_has_Course` DISABLE KEYS */;
INSERT INTO `Learning_Journey_has_Course` VALUES ('COR001',1),('COR002',1),('FIN001',1),('SAL002',1),('COR001',2),('COR002',2),('FIN001',2),('SAL002',2),('COR001',3),('COR002',3);

INSERT INTO `Learning_Journey_has_Course` VALUES ('COR001',4),('COR002',4),('FIN001',4),('SAL002',4),('COR001',5),('COR002',5),('FIN001',5),('SAL002',5),('COR001',6),('COR002',6);

/*!40000 ALTER TABLE `Learning_Journey_has_Course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Registration`
--

DROP TABLE IF EXISTS `Registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Registration` (
  `Reg_ID` int NOT NULL AUTO_INCREMENT,
  `Course_ID` varchar(20) NOT NULL,
  `Staff_ID` int NOT NULL,
  `Reg_Status` varchar(20) NOT NULL,
  `Completion_Status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Reg_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=380 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Registration`
--

LOCK TABLES `Registration` WRITE;
/*!40000 ALTER TABLE `Registration` DISABLE KEYS */;
INSERT INTO `Registration` VALUES (380,'COR002',1,'Registered','Completed'), (1,'COR002',130001,'Registered','Completed'),(2,'COR002',130002,'Registered','Completed'),(3,'COR002',140001,'Registered','Completed'),(4,'COR002',140002,'Registered','Completed'),(5,'COR002',140003,'Rejected',NULL),(6,'COR002',140008,'Registered','OnGoing'),(7,'COR002',140025,'Registered','OnGoing'),(8,'COR002',140036,'Waitlist',NULL),(9,'COR002',140078,'Waitlist',NULL),(10,'COR002',140102,'Registered',NULL),(11,'COR002',140103,'Registered',NULL),(12,'COR002',140108,'Registered',NULL),(13,'COR002',140115,'Registered','Completed'),(14,'COR002',140525,'Rejected',NULL),(15,'COR002',140878,'Registered','Completed'),(16,'COR002',150075,'Registered','Completed'),(17,'COR002',150065,'Waitlist',NULL),(18,'COR002',150076,'Waitlist',NULL),(19,'COR002',150118,'Registered','Completed'),(20,'COR002',150142,'Registered','OnGoing'),(21,'COR002',150143,'Registered','OnGoing'),(22,'COR002',150148,'Registered',NULL),(23,'COR002',150155,'Rejected',NULL),(24,'COR002',150776,'Registered',NULL),(25,'COR002',150095,'Registered',NULL),(26,'COR002',150085,'Waitlist',NULL),(27,'COR002',150096,'Waitlist',NULL),(28,'COR002',150138,'Registered','Completed'),(29,'COR002',150162,'Registered','Completed'),(30,'COR002',150163,'Registered','Completed'),(31,'COR002',150168,'Registered','Completed'),(32,'COR002',150175,'Rejected',NULL),(33,'COR002',150796,'Registered','OnGoing'),(34,'COR002',150125,'Registered','OnGoing'),(35,'COR002',150115,'Waitlist',NULL),(36,'COR002',150126,'Waitlist',NULL),(37,'COR002',150192,'Registered',NULL),(38,'COR002',150193,'Registered',NULL),(39,'COR002',150198,'Registered',NULL),(40,'COR002',150205,'Registered','Completed'),(41,'COR002',150615,'Rejected',NULL),(42,'COR002',150968,'Registered','Completed'),(43,'COR002',150166,'Registered','Completed'),(44,'COR002',150208,'Waitlist',NULL),(45,'COR002',150232,'Waitlist',NULL),(46,'COR002',150233,'Registered','Completed'),(47,'COR002',150238,'Registered','OnGoing'),(48,'COR002',150245,'Registered','OnGoing'),(49,'COR002',150655,'Registered',NULL),(50,'COR002',150866,'Rejected',NULL),(51,'COR002',150215,'Registered',NULL),(52,'COR002',150258,'Registered',NULL),(53,'COR002',150282,'Waitlist',NULL),(54,'COR002',150283,'Waitlist',NULL),(55,'COR002',150288,'Registered','Completed'),(56,'COR002',150295,'Registered','Completed'),(57,'COR002',150705,'Registered','Completed'),(58,'COR002',150916,'Registered','Completed'),(59,'COR002',151058,'Rejected',NULL),(60,'COR002',150265,'Registered','OnGoing'),(61,'COR002',150318,'Registered','OnGoing'),(62,'COR002',150342,'Waitlist',NULL),(63,'COR002',150343,'Waitlist',NULL),(64,'COR002',150348,'Registered',NULL),(65,'COR002',150355,'Registered',NULL),(66,'COR002',150765,'Registered',NULL),(67,'COR002',150976,'Registered','Completed'),(68,'COR002',151118,'Rejected',NULL),(69,'COR002',150356,'Registered','Completed'),(70,'COR002',150422,'Registered','Completed'),(71,'COR002',150423,'Waitlist',NULL),(72,'COR002',150428,'Waitlist',NULL),(73,'COR002',150435,'Registered','Completed'),(74,'COR002',150845,'Registered','OnGoing'),(75,'COR002',151056,'Registered','OnGoing'),(76,'COR002',151198,'Registered',NULL),(77,'COR002',150445,'Rejected',NULL),(78,'COR002',150488,'Registered',NULL),(79,'COR002',150513,'Registered','Completed'),(80,'COR002',150518,'Waitlist',NULL),(81,'COR002',150525,'Waitlist',NULL),(82,'COR002',150935,'Registered','Completed'),(83,'COR002',151146,'Registered','Completed'),(84,'COR002',151288,'Registered','Completed'),(85,'COR002',150555,'Registered','OnGoing'),(86,'COR002',150566,'Rejected',NULL),(87,'COR002',150632,'Registered','OnGoing'),(88,'COR002',150638,'Registered',NULL),(89,'COR002',150645,'Waitlist',NULL),(90,'COR002',151055,'Waitlist',NULL),(91,'COR002',151266,'Registered',NULL),(92,'COR002',151408,'Registered',NULL),(93,'COR002',150695,'Registered','Completed'),(94,'COR002',160008,'Registered','Completed'),(95,'COR002',160075,'Rejected',NULL),(96,'COR002',160076,'Registered','Completed'),(97,'COR002',160142,'Registered','Completed'),(98,'COR002',160143,'Waitlist',NULL),(99,'COR002',160148,'Waitlist',NULL),(100,'COR002',160155,'Registered','OnGoing'),(101,'COR002',160145,'Registered','OnGoing'),(102,'COR002',160135,'Registered',NULL),(103,'COR002',160146,'Registered',NULL),(104,'COR002',160188,'Rejected',NULL),(105,'COR002',160213,'Registered',NULL),(106,'COR002',160225,'Registered','Completed'),(107,'COR002',160258,'Waitlist',NULL),(108,'COR002',160282,'Waitlist',NULL),(109,'COR002',151008,'Registered',NULL),(110,'COR002',150216,'Waitlist',NULL),(111,'SAL004',140001,'Registered','Completed'),(112,'SAL004',140002,'Registered','Completed'),(113,'SAL003',140003,'Registered','Completed'),(114,'SAL003',140004,'Registered','OnGoing'),(115,'SAL004',140008,'Rejected',NULL),(116,'SAL003',140025,'Registered','OnGoing'),(117,'SAL004',140078,'Registered',NULL),(118,'SAL004',140102,'Waitlist',NULL),(119,'SAL003',140103,'Waitlist',NULL),(120,'SAL003',140108,'Registered','Completed'),(121,'SAL004',140115,'Registered','Completed'),(122,'SAL004',140525,'Registered','Completed'),(123,'SAL003',140736,'Registered','OnGoing'),(124,'SAL003',140878,'Rejected',NULL),(125,'tch002',150075,'Registered',NULL),(126,'tch003',150065,'Waitlist',NULL),(127,'tch005',150118,'Registered','Completed'),(128,'tch001',150143,'Registered','Completed'),(129,'tch002',150148,'Registered','OnGoing'),(130,'tch003',150155,'Rejected',NULL),(131,'tch001',150095,'Waitlist',NULL),(132,'tch002',150085,'Waitlist',NULL),(133,'tch003',150096,'Registered','Completed'),(134,'tch005',150162,'Registered','Completed'),(135,'tch001',150168,'Rejected',NULL),(136,'tch005',150938,'Waitlist',NULL),(137,'tch001',150115,'Registered','Completed'),(138,'tch002',150126,'Registered','Completed'),(139,'tch003',150192,'Registered','Completed'),(140,'tch005',150198,'Rejected',NULL),(141,'tch002',150826,'Registered',NULL),(142,'tch003',150968,'Waitlist',NULL),(143,'tch005',150166,'Registered','Completed'),(144,'tch001',150232,'Registered','Completed'),(145,'tch002',150233,'Registered','OnGoing'),(146,'tch003',150238,'Rejected',NULL),(147,'tch001',151008,'Waitlist',NULL),(148,'tch002',150215,'Waitlist',NULL),(149,'tch003',150216,'Registered','Completed'),(150,'tch005',150282,'Registered','Completed'),(151,'tch001',150288,'Rejected',NULL),(152,'tch005',151058,'Waitlist',NULL),(153,'tch001',150265,'Registered','Completed'),(154,'tch002',150276,'Registered','Completed'),(155,'tch003',150318,'Registered','Completed'),(156,'tch005',150343,'Rejected',NULL),(157,'tch002',150765,'Registered',NULL),(158,'tch003',150976,'Waitlist',NULL),(159,'tch005',150345,'Registered','Completed'),(160,'tch001',150398,'Registered','Completed'),(161,'tch002',150422,'Registered','OnGoing'),(162,'tch003',150423,'Rejected',NULL),(163,'tch001',151056,'Waitlist',NULL),(164,'tch002',151198,'Waitlist',NULL),(165,'tch003',150445,'Registered','Completed'),(166,'tch005',150488,'Registered','Completed'),(167,'tch001',150513,'Rejected',NULL),(168,'tch005',151146,'Waitlist',NULL),(169,'tch001',150555,'Registered','Completed'),(170,'tch002',150566,'Registered','Completed'),(171,'tch003',150608,'Registered','Completed'),(172,'tch005',150633,'Rejected',NULL),(173,'tch002',151055,'Registered',NULL),(174,'tch003',151266,'Waitlist',NULL),(175,'tch005',150695,'Registered','Completed'),(176,'HRD001',160008,'Registered','Completed'),(177,'MGT001',160075,'Registered','Completed'),(178,'MGT002',160065,'Registered','Completed'),(179,'MGT004',160118,'Rejected',NULL),(180,'MGT001',160148,'Registered',NULL),(181,'MGT002',160155,'Waitlist',NULL),(182,'MGT004',160135,'Registered','Completed'),(183,'MGT007',160146,'Registered','Completed'),(184,'HRD001',160188,'Registered','Completed'),(185,'MGT001',160212,'Registered','OnGoing'),(186,'MGT002',160213,'Rejected',NULL),(187,'MGT007',160258,'Registered',NULL),(188,'MGT001',160282,'Waitlist',NULL),(189,'FIN001',150166,'Waitlist',NULL),(190,'FIN002',150208,'Registered','Completed'),(191,'FIN001',150232,'Registered','Completed'),(192,'FIN002',150233,'Registered','Completed'),(193,'FIN001',150238,'Registered','OnGoing'),(194,'FIN002',150245,'Rejected',NULL),(195,'FIN001',150655,'Waitlist',NULL),(196,'FIN002',150866,'Registered','Completed'),(197,'FIN001',151008,'Registered','Completed'),(198,'FIN002',150215,'Registered','Completed'),(199,'FIN001',150216,'Registered','OnGoing'),(200,'MGT001',140001,'Registered','Completed'),(201,'MGT001',150008,'Registered','Completed'),(202,'MGT001',150166,'Registered','Completed'),(203,'COR002',140004,'Registered','Completed'),(204,'COR002',140015,'Waitlist',NULL),(205,'COR002',140736,'Waitlist',NULL),(206,'COR002',150008,'Registered','Completed'),(207,'COR002',150565,'Registered',NULL),(208,'COR002',150918,'Registered',NULL),(209,'COR002',150585,'Registered','OnGoing'),(210,'COR002',150938,'Rejected',NULL),(211,'COR002',150826,'Rejected',NULL),(212,'COR002',150165,'Registered','OnGoing'),(213,'COR002',150275,'Waitlist',NULL),(214,'COR002',150276,'Registered','Completed'),(215,'COR002',150345,'Registered',NULL),(216,'COR002',150398,'Registered','Completed'),(217,'COR002',150446,'Registered',NULL),(218,'COR002',150512,'Registered',NULL),(219,'COR002',150608,'Registered','OnGoing'),(220,'COR002',150633,'Waitlist',NULL),(221,'COR002',160065,'Waitlist',NULL),(222,'SAL004',160118,'Registered','Completed'),(223,'SAL004',160142,'Registered','Completed'),(224,'SAL003',160143,'Registered','Completed'),(225,'SAL003',160148,'Registered','OnGoing'),(226,'SAL004',160155,'Rejected',NULL),(227,'SAL003',160145,'Registered',NULL),(228,'SAL004',160135,'Waitlist',NULL),(229,'SAL004',160146,'Registered','Completed'),(230,'SAL003',160188,'Registered','Completed'),(231,'SAL003',160212,'Registered','OnGoing'),(232,'SAL004',160213,'Rejected',NULL),(233,'SAL004',160218,'Waitlist',NULL),(234,'SAL003',160225,'Waitlist',NULL),(235,'SAL003',160258,'Registered','Completed'),(236,'tch002',160282,'Registered','Completed'),(237,'tch003',150166,'Rejected',NULL),(238,'tch005',150208,'Waitlist',NULL),(239,'tch001',150245,'Rejected',NULL),(240,'tch002',150655,'Registered',NULL),(241,'tch003',150866,'Waitlist',NULL),(242,'tch005',151008,'Registered','Completed'),(243,'tch001',150215,'Registered','Completed'),(244,'tch005',150216,'Registered','OnGoing'),(245,'COR001',130001,'Registered','Completed'),(246,'COR006',140001,'Waitlist',NULL),(247,'FIN001',140002,'Waitlist',NULL),(248,'FIN002',140003,'Registered','Completed'),(249,'FIN003',140004,'Registered','OnGoing'),(250,'HRD001',140008,'Registered','OnGoing'),(251,'MGT001',140015,'Registered',NULL),(252,'MGT002',140025,'Rejected',NULL),(253,'MGT004',140036,'Registered',NULL),(254,'MGT007',140078,'Registered','Completed'),(255,'SAL001',140102,'Waitlist',NULL),(256,'SAL004',140108,'Registered','Completed'),(257,'tch001',140115,'Registered','Completed'),(258,'tch002',140525,'Registered','Completed'),(259,'tch003',140736,'Registered','OnGoing'),(260,'tch005',140878,'Rejected',NULL),(261,'tch008',150008,'Registered','OnGoing'),(262,'tch012',150075,'Registered',NULL),(263,'tch013',150065,'Waitlist',NULL),(264,'tch014',150076,'Waitlist',NULL),(265,'tch015',150118,'Registered',NULL),(266,'tch018',150142,'Registered',NULL),(267,'tch019',150143,'Registered','Completed'),(268,'COR001',150148,'Registered','Completed'),(269,'COR006',150565,'Registered','Completed'),(270,'FIN001',150776,'Registered','Completed'),(271,'FIN002',150918,'Waitlist',NULL),(272,'FIN003',150095,'Waitlist',NULL),(273,'HRD001',150085,'Registered','OnGoing'),(274,'MGT001',150096,'Registered','OnGoing'),(275,'MGT002',150138,'Registered',NULL),(276,'MGT004',150162,'Registered',NULL),(277,'MGT007',150163,'Rejected',NULL),(278,'SAL001',150168,'Registered',NULL),(279,'SAL003',150175,'Registered','Completed'),(280,'SAL004',150585,'Waitlist',NULL),(281,'tch001',150796,'Waitlist',NULL),(282,'tch002',150938,'Registered','Completed'),(283,'tch003',150125,'Registered','Completed'),(284,'tch005',150115,'Registered','Completed'),(285,'tch008',150126,'Registered','OnGoing'),(286,'tch012',150192,'Rejected',NULL),(287,'tch013',150193,'Registered','OnGoing'),(288,'tch014',150198,'Registered',NULL),(289,'tch015',150205,'Waitlist',NULL),(290,'tch018',150615,'Waitlist',NULL),(291,'tch019',150826,'Registered','Completed'),(292,'COR001',150968,'Registered','Completed'),(293,'COR006',150166,'Registered','OnGoing'),(294,'FIN001',150208,'Rejected',NULL),(295,'FIN002',150232,'Registered','OnGoing'),(296,'FIN003',150233,'Registered',NULL),(297,'HRD001',150238,'Waitlist',NULL),(298,'MGT001',150245,'Waitlist',NULL),(299,'MGT002',150655,'Registered','Completed'),(300,'MGT004',150866,'Registered','Completed'),(301,'MGT007',151008,'Registered','Completed'),(302,'SAL001',150215,'Registered','OnGoing'),(303,'SAL003',150216,'Rejected',NULL),(304,'SAL004',150258,'Registered',NULL),(305,'tch001',150282,'Waitlist',NULL),(306,'tch002',150283,'Registered','Completed'),(307,'tch003',150288,'Registered','Completed'),(308,'tch005',150295,'Registered','OnGoing'),(309,'tch008',150705,'Rejected',NULL),(310,'tch012',150916,'Waitlist',NULL),(311,'tch013',151058,'Waitlist',NULL),(312,'tch014',150275,'Registered','Completed'),(313,'tch015',150265,'Registered','Completed'),(314,'tch018',150276,'Rejected',NULL),(315,'tch019',150318,'Waitlist',NULL),(316,'COR001',150342,'Registered','Completed'),(317,'COR006',150348,'Registered','Completed'),(318,'FIN001',150355,'Rejected',NULL),(319,'FIN002',150765,'Registered',NULL),(320,'FIN003',150976,'Waitlist',NULL),(321,'HRD001',151118,'Registered','Completed'),(322,'MGT001',150345,'Registered','Completed'),(323,'MGT002',150356,'Registered','OnGoing'),(324,'MGT004',150398,'Registered','Completed'),(325,'MGT007',150422,'Registered','Completed'),(326,'SAL001',150423,'Waitlist',NULL),(327,'SAL003',150428,'Waitlist',NULL),(328,'SAL004',150435,'Registered','Completed'),(329,'tch001',150845,'Registered','OnGoing'),(330,'tch002',151056,'Registered','OnGoing'),(331,'tch003',151198,'Registered',NULL),(332,'tch005',150445,'Rejected',NULL),(333,'tch008',150446,'Registered',NULL),(334,'tch012',150488,'Registered','Completed'),(335,'tch013',150512,'Waitlist',NULL),(336,'tch014',150513,'Waitlist',NULL),(337,'tch015',150518,'Registered','Completed'),(338,'tch018',150525,'Registered','Completed'),(339,'tch019',150935,'Registered','Completed'),(340,'COR001',151146,'Registered','OnGoing'),(341,'COR006',150555,'Registered','OnGoing'),(342,'FIN001',150566,'Registered',NULL),(343,'FIN002',150608,'Waitlist',NULL),(344,'FIN003',150632,'Waitlist',NULL),(345,'HRD001',150633,'Registered',NULL),(346,'MGT001',150638,'Registered',NULL),(347,'MGT002',150645,'Registered','Completed'),(348,'MGT004',151055,'Registered','Completed'),(349,'MGT007',151266,'Rejected',NULL),(350,'SAL001',151408,'Registered','Completed'),(351,'SAL003',150695,'Registered','Completed'),(352,'SAL004',160008,'Waitlist',NULL),(353,'tch001',160075,'Waitlist',NULL),(354,'tch002',160065,'Registered','OnGoing'),(355,'tch003',160076,'Registered','OnGoing'),(356,'tch005',160118,'Registered',NULL),(357,'tch008',160142,'Registered',NULL),(358,'tch012',160143,'Rejected',NULL),(359,'tch013',160148,'Registered',NULL),(360,'tch014',160155,'Registered','Completed'),(361,'tch015',160145,'Waitlist',NULL),(362,'tch018',160135,'Waitlist',NULL),(363,'tch019',160146,'Registered','Completed'),(364,'COR001',160188,'Registered','Completed'),(365,'COR002',160212,'Registered','Completed'),(366,'COR006',160213,'Registered','OnGoing'),(367,'FIN001',160218,'Rejected',NULL),(368,'FIN002',160225,'Registered','OnGoing'),(369,'FIN003',160258,'Registered',NULL),(370,'HRD001',160282,'Waitlist',NULL),(371,'MGT002',150208,'Registered','Completed'),(372,'MGT004',150232,'Registered','Completed'),(373,'MGT007',150233,'Registered','Completed'),(374,'SAL001',150238,'Registered','OnGoing'),(375,'SAL003',150245,'Rejected',NULL),(376,'SAL004',150655,'Registered','OnGoing'),(377,'tch001',150866,'Registered',NULL),(378,'tch002',151008,'Waitlist',NULL),(379,'tch003',150215,'Waitlist',NULL);
/*!40000 ALTER TABLE `Registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Role_has_Skill`
--

DROP TABLE IF EXISTS `Role_has_Skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Role_has_Skill` (
  `Job_ID` int NOT NULL,
  `Skill_ID` int NOT NULL,
  KEY `Job_ID` (`Job_ID`),
  KEY `Skill_ID` (`Skill_ID`),
  CONSTRAINT `Role_has_Skill_ibfk_1` FOREIGN KEY (`Job_ID`) REFERENCES `Job_Role` (`Job_ID`),
  CONSTRAINT `Role_has_Skill_ibfk_2` FOREIGN KEY (`Skill_ID`) REFERENCES `Skill` (`Skill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Role_has_Skill`
--

LOCK TABLES `Role_has_Skill` WRITE;
/*!40000 ALTER TABLE `Role_has_Skill` DISABLE KEYS */;
INSERT INTO `Role_has_Skill` VALUES (1,1),(1,2),(2,2),(2,1),(5,8),(3,2),(3,3),(3,5),(5,2),(6,3),(6,5),(6,6),(7,1),(7,7),(8,0),(8,8),(9,2),(10,6),(10,0),(11,7),(11,4),(12,1),(12,2),(4,3),(5,3),(8,3),(4,4),(4,6),(2,8),(4,5),(13,1),(13,2),(13,3),(13,4),(1,3),(1,5),(1,6),(2,5),(2,6),(6,4),(6,5);
/*!40000 ALTER TABLE `Role_has_Skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Skill`
--

DROP TABLE IF EXISTS `Skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Skill` (
  `Skill_ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`Skill_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Skill`
--

LOCK TABLES `Skill` WRITE;
/*!40000 ALTER TABLE `Skill` DISABLE KEYS */;
INSERT INTO `Skill` VALUES (1,'Critical Thinking'),(2,'People Management'),(3,'Business Applications'),(4,'Adobe Photoshop'),(5,'Data Analysis'),(6,'Analytical Skills'),(7,'AutoCAD'),(8,'Financial Analysis'),(9,'Business Analysis'),(10,'Accounting'),(11,'Business Strategy'),(12,'Team Building'),(13,'Business Development'),(14,'Budgeting'),(15,'Business Planning'),(16,'Banking'),(17,'C (Progamming Language)'),(18,'Change Management'),(19,'Communication'),(20,'Coaching'),(21,'Contract Negotiation'),(22,'Product Development'),(23,'Software Development'),(24,'Graphic Design'),(25,'Digital Marketing'),(26,'Leadership Development'),(27,'Research and Development'),(28,'Microsoft Excel'),(29,'English'),(30,'Engineering'),(31,'Event Management'),(32,'Editing'),(33,'E-commerce'),(34,'Entrepreneurship'),(35,'Higher Education'),(36,'HTML'),(37,'HTML5'),(38,'Process Improvement'),(39,'Inventory Management'),(40,'Business Process Improvement'),(41,'CI/CD'),(42,'Business Intelligence'),(43,'Microsoft Office'),(44,'Java'),(45,'JavaScript'),(46,'jQuery'),(47,'Journalism'),(48,'Jira'),(49,'Confluence'),(50,'NodeJS'),(51,'Core Java'),(52,'TypeScript'),(53,'Golang'),(54,'Kaizen'),(55,'Kanban'),(56,'Key Account Development'),(57,'Team Leadership'),(58,'Logistics Management'),(59,'Linux'),(60,'Python '),(61,'Lean Manufacturing'),(62,'Agile Methodology'),(63,'Networking'),(64,'Online Marketing'),(65,'Sales Operations'),(66,'Qualitative Research'),(67,'Quality Assurance'),(68,'Unix'),(69,'Figma'),(70,'Zendeck'),(71,'Salesforce'),(72,'CSS'),(73,'Elasticsearch'),(74,'Kubernetes'),(75,'Docker');
/*!40000 ALTER TABLE `Skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Staff`
--

DROP TABLE IF EXISTS `Staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Staff` (
  `Staff_ID` int NOT NULL AUTO_INCREMENT,
  `Staff_FName` varchar(50) NOT NULL,
  `Staff_LName` varchar(50) NOT NULL,
  `Dept` varchar(50) NOT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Role_ID` int NOT NULL,
  PRIMARY KEY (`Staff_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=171009 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
INSERT INTO `Staff` VALUES (1,'john','doe','test','john.doe@test.com.sg',1), (130001,'John','Sim','Chariman','jack.sim@allinone.com.sg',1),(130002,'Jack','Sim','CEO','jack.sim@allinone.com.sg',1),(140001,'Derek','Tan','Sales','Derek.Tan@allinone.com.sg',3),(140002,'Susan','Goh','Sales','Susan.Goh@allinone.com.sg',2),(140003,'Janice','Chan','Sales','Janice.Chan@allinone.com.sg',2),(140004,'Mary','Teo','Sales','Mary.Teo@allinone.com.sg',2),(140008,'Jaclyn','Lee','Sales','Jaclyn.Lee@allinone.com.sg',2),(140015,'Oliva','Lim','Sales','Oliva.Lim@allinone.com.sg',2),(140025,'Emma','Heng','Sales','Emma.Heng@allinone.com.sg',2),(140036,'Charlotte','Wong','Sales','Charlotte.Wong@allinone.com.sg',2),(140078,'Amelia','Ong','Sales','Amelia.Ong@allinone.com.sg',2),(140102,'Eva','Yong','Sales','Eva.Yong@allinone.com.sg',2),(140103,'Sophia','Toh','Sales','Sophia.Toh@allinone.com.sg',2),(140108,'Liam','The','Sales','Liam.The@allinone.com.sg',2),(140115,'Noah','Ng','Sales','Noah.Ng@allinone.com.sg',2),(140525,'Oliver','Tan','Sales','Oliver.Tan@allinone.com.sg',2),(140736,'William','Fu','Sales','William.Fu@allinone.com.sg',2),(140878,'James','Tong','Sales','James.Tong@allinone.com.sg',2),(150008,'Eric','Loh','Ops','Eric.Loh@allinone.com.sg',3),(150065,'Noah','Goh','Ops','Noah.Goh@allinone.com.sg',4),(150075,'Liam','Tan','Ops','Liam.Tan@allinone.com.sg',4),(150076,'Oliver','Chan','Ops','Oliver.Chan@allinone.com.sg',4),(150085,'Michael','Ng','Ops','Michael.Ng@allinone.com.sg',4),(150095,'Alexander','The','Ops','Alexander.The@allinone.com.sg',4),(150096,'Ethan','Tan','Ops','Ethan.Tan@allinone.com.sg',4),(150115,'Jaclyn','Lee','Ops','Jaclyn.Lee@allinone.com.sg',4),(150118,'William','Teo','Ops','William.Teo@allinone.com.sg',4),(150125,'Mary','Teo','Ops','Mary.Teo@allinone.com.sg',4),(150126,'Oliva','Lim','Ops','Oliva.Lim@allinone.com.sg',2),(150138,'Daniel','Fu','Ops','Daniel.Fu@allinone.com.sg',4),(150142,'James','Lee','Ops','James.Lee@allinone.com.sg',4),(150143,'John','Lim','Ops','John.Lim@allinone.com.sg',4),(150148,'Jack','Heng','Ops','Jack.Heng@allinone.com.sg',4),(150155,'Derek','Wong','Ops','Derek.Wong@allinone.com.sg',4),(150162,'Jacob','Tong','Ops','Jacob.Tong@allinone.com.sg',4),(150163,'Logan','Loh','Ops','Logan.Loh@allinone.com.sg',4),(150165,'Oliver','Tan','Ops','Oliver.Tan@allinone.com.sg',2),(150166,'William','Fu','Ops','William.Fu@allinone.com.sg',2),(150168,'Jackson','Tan','Ops','Jackson.Tan@allinone.com.sg',4),(150175,'Aiden','Tan','Ops','Aiden.Tan@allinone.com.sg',4),(150192,'Emma','Heng','Ops','Emma.Heng@allinone.com.sg',2),(150193,'Charlotte','Wong','Ops','Charlotte.Wong@allinone.com.sg',2),(150198,'Amelia','Ong','Ops','Amelia.Ong@allinone.com.sg',2),(150205,'Eva','Yong','Ops','Eva.Yong@allinone.com.sg',2),(150208,'James','Tong','Ops','James.Tong@allinone.com.sg',2),(150215,'Michael','Lee','Ops','Michael.Lee@allinone.com.sg',2),(150216,'Ethan','Lim','Ops','Ethan.Lim@allinone.com.sg',2),(150232,'John','Loh','Ops','John.Loh@allinone.com.sg',2),(150233,'Jack','Tan','Ops','Jack.Tan@allinone.com.sg',2),(150238,'Derek','Tan','Ops','Derek.Tan@allinone.com.sg',2),(150245,'Benjamin','Tan','Ops','Benjamin.Tan@allinone.com.sg',2),(150258,'Daniel','Heng','Ops','Daniel.Heng@allinone.com.sg',2),(150265,'Jaclyn','Tong','Ops','Jaclyn.Tong@allinone.com.sg',2),(150275,'Mary','Fu','Ops','Mary.Fu@allinone.com.sg',2),(150276,'Oliva','Loh','Ops','Oliva.Loh@allinone.com.sg',2),(150282,'Jacob','Wong','Ops','Jacob.Wong@allinone.com.sg',2),(150283,'Logan','Ong','Ops','Logan.Ong@allinone.com.sg',2),(150288,'Jackson','Yong','Ops','Jackson.Yong@allinone.com.sg',2),(150295,'Aiden','Toh','Ops','Aiden.Toh@allinone.com.sg',2),(150318,'Emma','Tan','Ops','Emma.Tan@allinone.com.sg',2),(150342,'Charlotte','Tan','Ops','Charlotte.Tan@allinone.com.sg',2),(150343,'Amelia','Tan','Ops','Amelia.Tan@allinone.com.sg',2),(150345,'William','Heng','Ops','William.Heng@allinone.com.sg',2),(150348,'Eva','Goh','Ops','Eva.Goh@allinone.com.sg',2),(150355,'Sophia','Chan','Ops','Sophia.Chan@allinone.com.sg',2),(150356,'James','Wong','Ops','James.Wong@allinone.com.sg',2),(150398,'John','Ong','Ops','John.Ong@allinone.com.sg',2),(150422,'Jack','Yong','Ops','Jack.Yong@allinone.com.sg',2),(150423,'Derek','Toh','Ops','Derek.Toh@allinone.com.sg',2),(150428,'Benjamin','The','Ops','Benjamin.The@allinone.com.sg',2),(150435,'Lucas','Ng','Ops','Lucas.Ng@allinone.com.sg',2),(150445,'Ethan','Loh','Ops','Ethan.Loh@allinone.com.sg',2),(150446,'Daniel','Tan','Ops','Daniel.Tan@allinone.com.sg',2),(150488,'Jacob','Tan','Ops','Jacob.Tan@allinone.com.sg',2),(150512,'Logan','Tan','Ops','Logan.Tan@allinone.com.sg',2),(150513,'Jackson','Goh','Ops','Jackson.Goh@allinone.com.sg',2),(150518,'Aiden','Chan','Ops','Aiden.Chan@allinone.com.sg',2),(150525,'Samuel','Teo','Ops','Samuel.Teo@allinone.com.sg',2),(150555,'Jaclyn','Wong','Ops','Jaclyn.Wong@allinone.com.sg',2),(150565,'Benjamin','Ong','Ops','Benjamin.Ong@allinone.com.sg',4),(150566,'Oliva','Ong','Ops','Oliva.Ong@allinone.com.sg',2),(150585,'Samuel','Tan','Ops','Samuel.Tan@allinone.com.sg',4),(150608,'Emma','Yong','Ops','Emma.Yong@allinone.com.sg',2),(150615,'Sophia','Toh','Ops','Sophia.Toh@allinone.com.sg',2),(150632,'Charlotte','Toh','Ops','Charlotte.Toh@allinone.com.sg',2),(150633,'Amelia','The','Ops','Amelia.The@allinone.com.sg',2),(150638,'Eva','Ng','Ops','Eva.Ng@allinone.com.sg',2),(150645,'Sophia','Tan','Ops','Sophia.Tan@allinone.com.sg',2),(150655,'Lucas','Goh','Ops','Lucas.Goh@allinone.com.sg',2),(150695,'William','Tan','Ops','William.Tan@allinone.com.sg',2),(150705,'Samuel','The','Ops','Samuel.The@allinone.com.sg',2),(150765,'Liam','Teo','Ops','Liam.Teo@allinone.com.sg',2),(150776,'Lucas','Yong','Ops','Lucas.Yong@allinone.com.sg',4),(150796,'Susan','Goh','Ops','Susan.Goh@allinone.com.sg',4),(150826,'Liam','The','Ops','Liam.The@allinone.com.sg',2),(150845,'Henry','Tan','Ops','Henry.Tan@allinone.com.sg',2),(150866,'Henry','Chan','Ops','Henry.Chan@allinone.com.sg',2),(150916,'Susan','Ng','Ops','Susan.Ng@allinone.com.sg',2),(150918,'Henry','Toh','Ops','Henry.Toh@allinone.com.sg',4),(150935,'Susan','Lee','Ops','Susan.Lee@allinone.com.sg',2),(150938,'Janice','Chan','Ops','Janice.Chan@allinone.com.sg',4),(150968,'Noah','Ng','Ops','Noah.Ng@allinone.com.sg',2),(150976,'Noah','Lee','Ops','Noah.Lee@allinone.com.sg',2),(151008,'Alexander','Teo','Ops','Alexander.Teo@allinone.com.sg',2),(151055,'Liam','Fu','Ops','Liam.Fu@allinone.com.sg',2),(151056,'Alexander','Fu','Ops','Alexander.Fu@allinone.com.sg',2),(151058,'Janice','Tan','Ops','Janice.Tan@allinone.com.sg',2),(151118,'Oliver','Lim','Ops','Oliver.Lim@allinone.com.sg',2),(151146,'Janice','Lim','Ops','Janice.Lim@allinone.com.sg',2),(151198,'Michael','Tong','Ops','Michael.Tong@allinone.com.sg',2),(151266,'Noah','Tong','Ops','Noah.Tong@allinone.com.sg',2),(151288,'Mary','Heng','Ops','Mary.Heng@allinone.com.sg',2),(151408,'Oliver','Loh','Ops','Oliver.Loh@allinone.com.sg',2),(160008,'Sally','Loh','HR','Sally.Loh@allinone.com.sg',1),(160065,'John','Tan','HR','John.Tan@allinone.com.sg',1),(160075,'James','Tan','HR','James.Tan@allinone.com.sg',1),(160076,'Jack','Goh','HR','Jack.Goh@allinone.com.sg',1),(160118,'Derek','Chan','HR','Derek.Chan@allinone.com.sg',1),(160135,'Jaclyn','Ong','HR','Jaclyn.Ong@allinone.com.sg',2),(160142,'Benjamin','Teo','HR','Benjamin.Teo@allinone.com.sg',1),(160143,'Lucas','Lee','HR','Lucas.Lee@allinone.com.sg',1),(160145,'Mary','Wong','HR','Mary.Wong@allinone.com.sg',2),(160146,'Oliva','Yong','HR','Oliva.Yong@allinone.com.sg',2),(160148,'Henry','Lim','HR','Henry.Lim@allinone.com.sg',1),(160155,'Alexander','Heng','HR','Alexander.Heng@allinone.com.sg',1),(160188,'Emma','Toh','HR','Emma.Toh@allinone.com.sg',2),(160212,'Charlotte','The','HR','Charlotte.The@allinone.com.sg',2),(160213,'Amelia','Ng','HR','Amelia.Ng@allinone.com.sg',2),(160218,'Eva','Tan','HR','Eva.Tan@allinone.com.sg',2),(160225,'Sophia','Fu','HR','Sophia.Fu@allinone.com.sg',2),(160258,'Michael','Tong','HR','Michael.Tong@allinone.com.sg',2),(160282,'Ethan','Loh','HR','Ethan.Loh@allinone.com.sg',2),(170166,'David','Yap','Finance','David.Yap@allinone.com.sg',3),(170208,'Daniel','Tan','Finance','Daniel.Tan@allinone.com.sg',2),(170215,'Mary','Wong','Finance','Mary.Wong@allinone.com.sg',2),(170216,'Jaclyn','Ong','Finance','Jaclyn.Ong@allinone.com.sg',2),(170232,'Jacob','Tan','Finance','Jacob.Tan@allinone.com.sg',2),(170233,'Logan','Goh','Finance','Logan.Goh@allinone.com.sg',2),(170238,'Jackson','Chan','Finance','Jackson.Chan@allinone.com.sg',2),(170245,'Aiden','Teo','Finance','Aiden.Teo@allinone.com.sg',2),(170655,'Samuel','Lee','Finance','Samuel.Lee@allinone.com.sg',2),(170866,'Susan','Lim','Finance','Susan.Lim@allinone.com.sg',2),(171008,'Janice','Heng','Finance','Janice.Heng@allinone.com.sg',2);
/*!40000 ALTER TABLE `Staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_has_Skill`
--

DROP TABLE IF EXISTS `User_has_Skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_has_Skill` (
  `Skill_ID` int NOT NULL,
  `Staff_ID` int NOT NULL,
  `Date_Acquired` date NOT NULL,
  KEY `Skill_ID` (`Skill_ID`),
  KEY `Staff_ID` (`Staff_ID`),
  CONSTRAINT `User_has_Skill_ibfk_1` FOREIGN KEY (`Skill_ID`) REFERENCES `Skill` (`Skill_ID`),
  CONSTRAINT `User_has_Skill_ibfk_2` FOREIGN KEY (`Staff_ID`) REFERENCES `Staff` (`Staff_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_has_Skill`
--

LOCK TABLES `User_has_Skill` WRITE;
/*!40000 ALTER TABLE `User_has_Skill` DISABLE KEYS */;
INSERT INTO `User_has_Skill` VALUES (1,130001,'2021-12-31'),(2,130001,'2022-03-03'),(1,140001,'2021-01-01'),(3,140103,'2022-01-01'),(3,150215,'2020-04-28'),(7,150265,'2022-07-05'),(4,150845,'2021-04-27'),(1,150345,'2020-07-13'),(7,171008,'2020-03-22'),(5,140525,'2020-10-04'),(6,150095,'2021-04-03'),(8,160258,'2021-10-22'),(9,150148,'2021-09-03'),(5,170208,'2021-04-19'),(3,150565,'2021-12-23'),(9,150348,'2020-09-21'),(0,151118,'2020-01-20'),(9,150162,'2021-01-14'),(2,150138,'2022-10-08'),(5,140102,'2022-09-23'),(1,150258,'2021-11-14'),(7,150075,'2020-03-11'),(0,160065,'2022-02-19'),(2,150163,'2021-06-20'),(8,140736,'2022-01-14'),(6,160065,'2021-12-06'),(0,170232,'2020-03-13'),(3,150143,'2021-03-13'),(8,160142,'2021-10-14'),(3,160213,'2022-07-22'),(6,150918,'2020-07-06'),(6,170232,'2021-08-22'),(8,170215,'2021-05-03'),(7,150705,'2020-03-28'),(8,150633,'2021-10-21'),(1,171008,'2022-08-15'),(0,150615,'2022-07-29'),(4,150198,'2021-04-01'),(4,140015,'2022-04-26'),(4,140736,'2021-03-17'),(0,151056,'2020-05-02'),(5,151056,'2020-12-10'),(6,150076,'2020-11-21'),(1,160065,'2020-03-12'),(5,170232,'2021-12-11'),(3,151008,'2022-08-26'),(8,150233,'2021-08-17'),(5,160076,'2021-08-02'),(2,150142,'2020-05-16'),(0,150265,'2021-02-04'),(4,150976,'2022-02-07'),(2,150288,'2022-03-01'),(4,150318,'2020-05-02'),(8,160076,'2020-05-30'),(7,140878,'2021-03-15'),(1,150095,'2021-06-16'),(9,150216,'2020-05-29'),(0,140078,'2021-11-08'),(6,150115,'2021-11-04'),(9,150288,'2020-05-09'),(1,140025,'2022-06-21'),(7,150295,'2020-01-04'),(3,150142,'2021-10-28'),(4,150085,'2020-11-02'),(5,160258,'2021-01-29'),(2,150275,'2022-09-26'),(4,150423,'2022-06-21'),(1,170866,'2021-05-22'),(9,150245,'2021-09-17'),(6,160225,'2020-07-09'),(3,140525,'2022-07-21'),(2,150918,'2020-04-11'),(5,150193,'2022-05-14'),(7,150126,'2022-01-17'),(2,150445,'2020-12-12');
/*!40000 ALTER TABLE `User_has_Skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'spm_db'
--
-- SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-18  9:34:37