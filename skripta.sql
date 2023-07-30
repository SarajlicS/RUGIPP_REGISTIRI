CREATE DATABASE  IF NOT EXISTS `registri_rugipp` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `registri_rugipp`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: registri_rugipp
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `registar_firmi`
--

DROP TABLE IF EXISTS `registar_firmi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registar_firmi` (
  `ID_FIRM` int NOT NULL AUTO_INCREMENT,
  `JIB` varchar(20) NOT NULL,
  `Naziv` varchar(100) NOT NULL,
  `Adresa` varchar(100) NOT NULL,
  `Broj_Telefona` varchar(45) NOT NULL,
  PRIMARY KEY (`ID_FIRM`,`JIB`),
  UNIQUE KEY `JIB_UNIQUE` (`JIB`),
  UNIQUE KEY `ID_UNIQUE` (`ID_FIRM`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registar_firmi`
--

LOCK TABLES `registar_firmi` WRITE;
/*!40000 ALTER TABLE `registar_firmi` DISABLE KEYS */;
INSERT INTO `registar_firmi` VALUES (6,'4400999640004','Републичка управа за геодетске и имовинско-правне послове','Трг Републике Српске бр. 8, Бања Лука','051/338-000');
/*!40000 ALTER TABLE `registar_firmi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registar_geodeta`
--

DROP TABLE IF EXISTS `registar_geodeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registar_geodeta` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `JMBG` varchar(20) NOT NULL,
  `Ime` varchar(45) DEFAULT NULL,
  `Prezime` varchar(45) DEFAULT NULL,
  `Strucna_Sprema` varchar(45) DEFAULT NULL,
  `Broj_Strucnog` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`,`JMBG`),
  UNIQUE KEY `JMBG_UNIQUE` (`JMBG`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registar_geodeta`
--

LOCK TABLES `registar_geodeta` WRITE;
/*!40000 ALTER TABLE `registar_geodeta` DISABLE KEYS */;
INSERT INTO `registar_geodeta` VALUES (28,'2602989000000','Срђан','Сарајлић','ВСС','89595/15');
/*!40000 ALTER TABLE `registar_geodeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registar_instrumenata`
--

DROP TABLE IF EXISTS `registar_instrumenata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registar_instrumenata` (
  `ID_INST` int NOT NULL AUTO_INCREMENT,
  `Seriski_broj` int NOT NULL,
  `Tip_Instrumenta` varchar(90) NOT NULL,
  `Proizvodjac` varchar(90) NOT NULL,
  `Etaloniran_Do` date NOT NULL,
  `Registar_Firmi_JIB` varchar(20) NOT NULL,
  PRIMARY KEY (`ID_INST`,`Registar_Firmi_JIB`),
  UNIQUE KEY `Seriski_broj_UNIQUE` (`Seriski_broj`),
  UNIQUE KEY `idInstrument_UNIQUE` (`ID_INST`),
  KEY `fk_Registar_Instrumenata_Registar_Privatnih_Firmi_idx` (`Registar_Firmi_JIB`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registar_instrumenata`
--

LOCK TABLES `registar_instrumenata` WRITE;
/*!40000 ALTER TABLE `registar_instrumenata` DISABLE KEYS */;
INSERT INTO `registar_instrumenata` VALUES (4,98889000,'ГНСС','Leica','2023-12-26','4400999640004');
/*!40000 ALTER TABLE `registar_instrumenata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `idUser` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `active` tinyint(1) DEFAULT '0',
  `password` varchar(100) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`idUser`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `idUser_UNIQUE` (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'admin@gmail.com',1,'admin','admin','admin','admin',1),(7,'user@gmail.com',0,'user','user','user','user',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-30 22:34:58
