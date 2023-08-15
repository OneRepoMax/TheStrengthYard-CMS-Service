-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`User` ;

CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `UserId` INT NOT NULL AUTO_INCREMENT,
  `EmailAddress` VARCHAR(255) NOT NULL,
  `First Name` LONGTEXT NOT NULL,
  `Last Name` LONGTEXT NOT NULL,
  `Gender` CHAR(1) NOT NULL,
  `DateOfBirth` DATE NOT NULL,
  `HomeAddress` VARCHAR(45) NOT NULL,
  `PostalCode` INT NOT NULL,
  `ContactNo` VARCHAR(100) NOT NULL,
  `Username` VARCHAR(45) NOT NULL,
  `Password` LONGTEXT NOT NULL,
  `UserType` CHAR(1) NOT NULL,
  `MemberJoinDate` DATE NOT NULL,
  `MembershipStatus` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE INDEX `EmailAddress_UNIQUE` (`EmailAddress` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Memberships`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Memberships` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Memberships` (
  `MembershipTypeId` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(255) NOT NULL,
  `BaseFee` DOUBLE NOT NULL,
  `Description` VARCHAR(255) NULL,
  PRIMARY KEY (`MembershipTypeId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`MembershipRecord`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`MembershipRecord` ;

CREATE TABLE IF NOT EXISTS `mydb`.`MembershipRecord` (
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
    REFERENCES `mydb`.`Memberships` (`MembershipTypeId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `UserFK`
    FOREIGN KEY (`UserId`)
    REFERENCES `mydb`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Payment` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Payment` (
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
    REFERENCES `mydb`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Class`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Class` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Class` (
  `ClassId` INT NOT NULL AUTO_INCREMENT,
  `ClassName` VARCHAR(45) NOT NULL,
  `Description` LONGTEXT NOT NULL,
  `MaximumCapacity` INT NOT NULL,
  `ClassType` INT NOT NULL,
  PRIMARY KEY (`ClassId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ClassSlot`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`ClassSlot` ;

CREATE TABLE IF NOT EXISTS `mydb`.`ClassSlot` (
  `ClassSlotId` INT NOT NULL,
  `Day` VARCHAR(45) NOT NULL,
  `StartTime` TIMESTAMP NOT NULL,
  `EndTime` TIMESTAMP NOT NULL,
  `ClassId` INT NOT NULL,
  PRIMARY KEY (`ClassSlotId`, `ClassId`),
  INDEX `fk_ClassSlot_Class1_idx` (`ClassId` ASC) VISIBLE,
  CONSTRAINT `fk_ClassSlot_Class1`
    FOREIGN KEY (`ClassId`)
    REFERENCES `mydb`.`Class` (`ClassId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Booking`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Booking` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Booking` (
  `BookingDate` DATE NOT NULL,
  `ClassDate` DATE NOT NULL,
  `User_UserId` INT NOT NULL,
  `ClassSlot_ClassSlotId` INT NOT NULL,
  `ClassSlot_Class_ClassId` INT NOT NULL,
  INDEX `fk_Booking_User1_idx` (`User_UserId` ASC) VISIBLE,
  INDEX `fk_Booking_ClassSlot1_idx` (`ClassSlot_ClassSlotId` ASC, `ClassSlot_Class_ClassId` ASC) VISIBLE,
  CONSTRAINT `fk_Booking_User1`
    FOREIGN KEY (`User_UserId`)
    REFERENCES `mydb`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Booking_ClassSlot1`
    FOREIGN KEY (`ClassSlot_ClassSlotId` , `ClassSlot_Class_ClassId`)
    REFERENCES `mydb`.`ClassSlot` (`ClassSlotId` , `ClassId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`BlockedDate`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`BlockedDate` ;

CREATE TABLE IF NOT EXISTS `mydb`.`BlockedDate` (
  `BlockedDateID` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL,
  `StartTime` DATETIME NULL,
  `StopTime` DATETIME NULL,
  PRIMARY KEY (`BlockedDateID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`MembershipLog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`MembershipLog` ;

CREATE TABLE IF NOT EXISTS `mydb`.`MembershipLog` (
  `MembershipLogId` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL,
  `ActionType` VARCHAR(255) NULL,
  `Description` LONGTEXT NULL,
  `MembershipRecordId` INT NOT NULL,
  PRIMARY KEY (`MembershipLogId`, `MembershipRecordId`),
  INDEX `fk_MembershipLog_MembershipRecord1_idx` (`MembershipRecordId` ASC) VISIBLE,
  CONSTRAINT `fk_MembershipLog_MembershipRecord1`
    FOREIGN KEY (`MembershipRecordId`)
    REFERENCES `mydb`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
