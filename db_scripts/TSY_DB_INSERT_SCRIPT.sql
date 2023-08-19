-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tsy_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `tsy_db` ;

-- -----------------------------------------------------
-- Schema tsy_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tsy_db` DEFAULT CHARACTER SET utf8 ;
USE `tsy_db` ;

-- -----------------------------------------------------
-- Table `tsy_db`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`User` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`User` (
  `UserId` INT NOT NULL AUTO_INCREMENT,
  `EmailAddress` VARCHAR(255) NOT NULL,
  `FirstName` LONGTEXT NOT NULL,
  `LastName` LONGTEXT NOT NULL,
  `Gender` CHAR(1) NOT NULL,
  `DateOfBirth` DATE NOT NULL,
  `HomeAddress` VARCHAR(45) NOT NULL,
  `PostalCode` INT NOT NULL,
  `ContactNo` VARCHAR(100) NOT NULL,
  `Username` VARCHAR(45) NOT NULL,
  `Password` LONGTEXT NOT NULL,
  `UserType` CHAR(1) NOT NULL,
  `AccountCreationDate` DATE NOT NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE INDEX `EmailAddress_UNIQUE` (`EmailAddress` ASC) VISIBLE)
ENGINE = InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb3;

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`User`
-- -----------------------------------------------------
INSERT INTO `User` VALUES 
(1, 'testuser@tsy.com', 'John', 'Doe', 'M', '1997-05-29', 'Sample Address', 123456, '12345678', 'johndoe', '12345678', 'C', '2023-08-16'),
(100, 'mukminpitoyo@gmail.com', 'Mukmin', 'Pitoyo', 'M', '1997-05-29', 'Sample Address', 123456, '12345678', 'mukminpitoyo', '12345678', 'C', '2023-08-16'),
(101, 'sample@gmail.com', 'Sarah', 'Tan', 'F', '2003-01-01', 'Sample Address', 123456, '12345678', 'sarahtan', '12345678', 'C', '2023-08-16');

-- -----------------------------------------------------
-- Table `tsy_db`.`Memberships`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`Memberships` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`Memberships` (
  `MembershipTypeId` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(255) NOT NULL,
  `BaseFee` DOUBLE NOT NULL,
  `Description` VARCHAR(255) NULL,
  PRIMARY KEY (`MembershipTypeId`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`Memberships`
-- -----------------------------------------------------
INSERT INTO `Memberships` VALUES 
(1, 'Monthly', 250, 'Progressive Strength Class Membership (Standard)'),
(2, 'Yearly', 2400, 'Progressive Strength Class Membership (Standard)'),
(3, 'Monthly', 200, 'Progressive Strength Class Membership (Student)'),
(4, 'Yearly', 1800, 'Progressive Strength Class Membership (Student)'),
(5, 'Monthly', 90, 'Open Gym Membership'),
(6, 'Yearly', 900, 'Open Gym Membership'),
(7, 'One-Time', 260, 'Beginner Olympic Weightlifting Course'),
(8, 'One-Time', 150, 'Barbell Fundamentals Course');

-- -----------------------------------------------------
-- Table `tsy_db`.`MembershipRecord`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`MembershipRecord` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`MembershipRecord` (
  `MembershipRecordId` INT NOT NULL AUTO_INCREMENT,
  `UserId` INT NOT NULL,
  `MembershipTypeId` INT NOT NULL,
  `StartDate` DATE NOT NULL,
  `EndDate` DATE NOT NULL,
  INDEX `MembershipTypeFK_idx` (`MembershipTypeId` ASC) VISIBLE,
  PRIMARY KEY (`MembershipRecordId`),
  INDEX `UserFK_idx` (`UserId` ASC) VISIBLE,
  CONSTRAINT `MembershipTypeFK`
    FOREIGN KEY (`MembershipTypeId`)
    REFERENCES `tsy_db`.`Memberships` (`MembershipTypeId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `UserFK`
    FOREIGN KEY (`UserId`)
    REFERENCES `tsy_db`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`MembershipRecord`
-- -----------------------------------------------------
INSERT INTO `MembershipRecord` VALUES 
(1, 100, 5, '2023-01-01', '2023-05-01'),
(2, 101, 2, '2023-01-01', '2024-01-01');

-- -----------------------------------------------------
-- Table `tsy_db`.`Payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`Payment` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`Payment` (
  `PaymentId` INT NOT NULL AUTO_INCREMENT,
  `PayPalId` VARCHAR(255) NULL,
  `MembershipRecordId` INT NOT NULL,
  `TransactionDate` DATE NOT NULL,
  `Amount` DOUBLE NOT NULL,
  `Discount` DOUBLE NULL,
  `PaymentMode` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`PaymentId`),
  INDEX `MembershipRecordFK_idx` (`MembershipRecordId` ASC) VISIBLE,
  UNIQUE INDEX `MembershipRecordId_UNIQUE` (`MembershipRecordId` ASC) VISIBLE,
  CONSTRAINT `MembershipRecordFK`
    FOREIGN KEY (`MembershipRecordId`)
    REFERENCES `tsy_db`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db`.`Class`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`Class` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`Class` (
  `ClassId` INT NOT NULL AUTO_INCREMENT,
  `ClassName` VARCHAR(45) NOT NULL,
  `Description` LONGTEXT NOT NULL,
  `MaximumCapacity` INT NOT NULL,
  `ClassType` INT NOT NULL,
  PRIMARY KEY (`ClassId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db`.`ClassSlot`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`ClassSlot` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`ClassSlot` (
  `ClassSlotId` INT NOT NULL,
  `Day` VARCHAR(45) NOT NULL,
  `StartTime` TIMESTAMP NOT NULL,
  `EndTime` TIMESTAMP NOT NULL,
  `ClassId` INT NOT NULL,
  PRIMARY KEY (`ClassSlotId`, `ClassId`),
  INDEX `fk_ClassSlot_Class1_idx` (`ClassId` ASC) VISIBLE,
  CONSTRAINT `fk_ClassSlot_Class1`
    FOREIGN KEY (`ClassId`)
    REFERENCES `tsy_db`.`Class` (`ClassId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db`.`Booking`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`Booking` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`Booking` (
  `BookingDate` DATE NOT NULL,
  `ClassDate` DATE NOT NULL,
  `User_UserId` INT NOT NULL,
  `ClassSlot_ClassSlotId` INT NOT NULL,
  `ClassSlot_Class_ClassId` INT NOT NULL,
  INDEX `fk_Booking_User1_idx` (`User_UserId` ASC) VISIBLE,
  INDEX `fk_Booking_ClassSlot1_idx` (`ClassSlot_ClassSlotId` ASC, `ClassSlot_Class_ClassId` ASC) VISIBLE,
  CONSTRAINT `fk_Booking_User1`
    FOREIGN KEY (`User_UserId`)
    REFERENCES `tsy_db`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Booking_ClassSlot1`
    FOREIGN KEY (`ClassSlot_ClassSlotId` , `ClassSlot_Class_ClassId`)
    REFERENCES `tsy_db`.`ClassSlot` (`ClassSlotId` , `ClassId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db`.`BlockedDate`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`BlockedDate` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`BlockedDate` (
  `BlockedDateID` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL,
  `StartTime` DATETIME NULL,
  `StopTime` DATETIME NULL,
  PRIMARY KEY (`BlockedDateID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db`.`MembershipLog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`MembershipLog` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`MembershipLog` (
  `MembershipLogId` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL,
  `ActionType` VARCHAR(255) NULL,
  `Description` LONGTEXT NULL,
  `MembershipRecordId` INT NOT NULL,
  PRIMARY KEY (`MembershipLogId`, `MembershipRecordId`),
  INDEX `fk_MembershipLog_MembershipRecord1_idx` (`MembershipRecordId` ASC) VISIBLE,
  CONSTRAINT `fk_MembershipLog_MembershipRecord1`
    FOREIGN KEY (`MembershipRecordId`)
    REFERENCES `tsy_db`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
