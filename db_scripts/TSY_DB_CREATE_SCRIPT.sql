-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema tsy_db
-- -----------------------------------------------------

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
  `Password` LONGTEXT NOT NULL,
  `UserType` CHAR(1) NOT NULL,
  `AccountCreationDate` DATE NOT NULL,
  `DisplayPicture` LONGTEXT,
  `verified` TINYINT NOT NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE INDEX `EmailAddress_UNIQUE` (`EmailAddress` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 100
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `tsy_db`.`Memberships`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`Memberships` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`Memberships` (
  `MembershipTypeId` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(255) NOT NULL,
  `BaseFee` DOUBLE NOT NULL,
  `Description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`MembershipTypeId`))
ENGINE = InnoDB;


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
  `ActiveStatus` VARCHAR(255) NOT NULL DEFAULT "Active",
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
-- Table `tsy_db`.`Payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`Payment` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`Payment` (
  `PaymentId` INT NOT NULL AUTO_INCREMENT,
  `PayPalId` VARCHAR(255) NULL DEFAULT NULL,
  `MembershipRecordId` INT NOT NULL,
  `TransactionDate` DATE NOT NULL,
  `Amount` DOUBLE NOT NULL,
  `Discount` DOUBLE NULL DEFAULT NULL,
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
  `Date` DATE NULL DEFAULT NULL,
  `StartTime` DATETIME NULL DEFAULT NULL,
  `StopTime` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`BlockedDateID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db`.`MembershipLog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`MembershipLog` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`MembershipLog` (
  `MembershipLogId` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL DEFAULT NULL,
  `ActionType` VARCHAR(255) NULL DEFAULT NULL,
  `Description` LONGTEXT NULL DEFAULT NULL,
  `MembershipRecordId` INT NOT NULL,
  PRIMARY KEY (`MembershipLogId`, `MembershipRecordId`),
  INDEX `fk_MembershipLog_MembershipRecord1_idx` (`MembershipRecordId` ASC) VISIBLE,
  CONSTRAINT `fk_MembershipLog_MembershipRecord1`
    FOREIGN KEY (`MembershipRecordId`)
    REFERENCES `tsy_db`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 900
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `tsy_db`.`IndemnityForm`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db`.`IndemnityForm` ;

CREATE TABLE IF NOT EXISTS `tsy_db`.`IndemnityForm` (
  `IndemnityFormId` INT NOT NULL AUTO_INCREMENT,
  `FeedbackDiscover` LONGTEXT NULL,
  `MedicalHistory` LONGTEXT NULL,
  `MedicalRemarks` LONGTEXT NULL,
  `AcknowledgementTnC` TINYINT NULL,
  `AcknowledgementOpenGymRules` TINYINT NULL,
  `UserId` INT NOT NULL,
  PRIMARY KEY (`IndemnityFormId`, `UserId`),
  INDEX `fk_IndemnityForm_User1_idx` (`UserId` ASC) VISIBLE,
  CONSTRAINT `fk_IndemnityForm_User1`
    FOREIGN KEY (`UserId`)
    REFERENCES `tsy_db`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB AUTO_INCREMENT = 300 DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
