-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema tsy_db_test
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tsy_db_test
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tsy_db_test` DEFAULT CHARACTER SET utf8 ;
USE `tsy_db_test` ;

-- -----------------------------------------------------
-- Table `tsy_db_test`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`User` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`User` (
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
-- Table `tsy_db_test`.`Memberships`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`Memberships` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`Memberships` (
  `MembershipTypeId` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(255) NOT NULL,
  `BaseFee` DOUBLE NOT NULL,
  `Title` VARCHAR(255) NOT NULL,
  `Description` LONGTEXT NULL,
  `Picture` LONGTEXT,
  PRIMARY KEY (`MembershipTypeId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`MembershipRecord`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`MembershipRecord` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`MembershipRecord` (
  `MembershipRecordId` INT NOT NULL AUTO_INCREMENT,
  `UserId` INT NOT NULL,
  `MembershipTypeId` INT NOT NULL,
  `StartDate` DATE NOT NULL,
  `EndDate` DATE,
  `ActiveStatus` VARCHAR(255) NOT NULL DEFAULT "Inactive",
  `StatusRemarks` LONGTEXT NULL DEFAULT NULL,
  INDEX `MembershipTypeFK_idx` (`MembershipTypeId` ASC) VISIBLE,
  PRIMARY KEY (`MembershipRecordId`),
  INDEX `UserFK_idx` (`UserId` ASC) VISIBLE,
  CONSTRAINT `MembershipTypeFK`
    FOREIGN KEY (`MembershipTypeId`)
    REFERENCES `tsy_db_test`.`Memberships` (`MembershipTypeId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `UserFK`
    FOREIGN KEY (`UserId`)
    REFERENCES `tsy_db_test`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`Payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`Payment` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`Payment` (
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
    REFERENCES `tsy_db_test`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
AUTO_INCREMENT = 7000 
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`Class`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`Class` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`Class` (
  `ClassId` INT NOT NULL AUTO_INCREMENT,
  `ClassName` VARCHAR(45) NOT NULL,
  `Description` LONGTEXT NOT NULL,
  `MaximumCapacity` INT NOT NULL,
  `ClassType` INT NOT NULL,
  PRIMARY KEY (`ClassId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`ClassSlot`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`ClassSlot` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`ClassSlot` (
  `ClassSlotId` INT NOT NULL,
  `Day` VARCHAR(45) NOT NULL,
  `StartTime` TIMESTAMP NOT NULL,
  `EndTime` TIMESTAMP NOT NULL,
  `ClassId` INT NOT NULL,
  PRIMARY KEY (`ClassSlotId`, `ClassId`),
  INDEX `fk_ClassSlot_Class1_idx` (`ClassId` ASC) VISIBLE,
  CONSTRAINT `fk_ClassSlot_Class1`
    FOREIGN KEY (`ClassId`)
    REFERENCES `tsy_db_test`.`Class` (`ClassId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`Booking`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`Booking` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`Booking` (
  `BookingDate` DATE NOT NULL,
  `ClassDate` DATE NOT NULL,
  `User_UserId` INT NOT NULL,
  `ClassSlot_ClassSlotId` INT NOT NULL,
  `ClassSlot_Class_ClassId` INT NOT NULL,
  INDEX `fk_Booking_User1_idx` (`User_UserId` ASC) VISIBLE,
  INDEX `fk_Booking_ClassSlot1_idx` (`ClassSlot_ClassSlotId` ASC, `ClassSlot_Class_ClassId` ASC) VISIBLE,
  CONSTRAINT `fk_Booking_User1`
    FOREIGN KEY (`User_UserId`)
    REFERENCES `tsy_db_test`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Booking_ClassSlot1`
    FOREIGN KEY (`ClassSlot_ClassSlotId` , `ClassSlot_Class_ClassId`)
    REFERENCES `tsy_db_test`.`ClassSlot` (`ClassSlotId` , `ClassId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`BlockedDate`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`BlockedDate` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`BlockedDate` (
  `BlockedDateID` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL DEFAULT NULL,
  `StartTime` DATETIME NULL DEFAULT NULL,
  `StopTime` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`BlockedDateID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`MembershipLog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`MembershipLog` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`MembershipLog` (
  `MembershipLogId` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NULL DEFAULT NULL,
  `ActionType` VARCHAR(255) NULL DEFAULT NULL,
  `Description` LONGTEXT NULL DEFAULT NULL,
  `MembershipRecordId` INT NOT NULL,
  PRIMARY KEY (`MembershipLogId`, `MembershipRecordId`),
  INDEX `fk_MembershipLog_MembershipRecord1_idx` (`MembershipRecordId` ASC) VISIBLE,
  CONSTRAINT `fk_MembershipLog_MembershipRecord1`
    FOREIGN KEY (`MembershipRecordId`)
    REFERENCES `tsy_db_test`.`MembershipRecord` (`MembershipRecordId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB 
AUTO_INCREMENT = 900 
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `tsy_db_test`.`IndemnityForm`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsy_db_test`.`IndemnityForm` ;

CREATE TABLE IF NOT EXISTS `tsy_db_test`.`IndemnityForm` (
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
    REFERENCES `tsy_db_test`.`User` (`UserId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB AUTO_INCREMENT = 300 DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`User`
-- -----------------------------------------------------
INSERT INTO `User` VALUES 
(1, 'testuser@tsy.com', 'John', 'Doe', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 1),
(2, 'admin@tsy.com', 'John', 'Doe', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'A', '2023-08-16', "", 1),
(3, 'user1@example.com', 'Alex', 'Johnson', 'M', '1990-03-15', '123 Main St', 123456, '98765432', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/1.jpg', 1),
(4, 'user2@example.com', 'Emily', 'Smith', 'F', '1995-07-20', '456 Elm St', 789012, '87654321', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/2.jpg', 1),
(5, 'user3@example.com', 'Daniel', 'Brown', 'M', '1988-11-30', '789 Oak St', 345678, '23456789', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/3.jpg', 1),
(6, 'user4@example.com', 'Emma', 'Davis', 'F', '1999-05-12', '567 Maple St', 456789, '12345678', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/4.jpg', 1),
(32, 'user29@example.com', 'Olivia', 'Garcia', 'F', '1993-09-10', '567 Pine St', 567890, '34567890', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/14.jpg', 1),
(33, 'user30@example.com', 'Mason', 'Williams', 'M', '1992-11-05', '789 Oak St', 345678, '23456789', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/15.jpg', 1),
(34, 'user31@example.com', 'Sophia', 'Lee', 'F', '1991-02-28', '890 Oak St', 456789, '23456789', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/1.jpg', 1),
(35, 'user32@example.com', 'William', 'Clark', 'M', '1987-06-18', '567 Elm St', 567890, '34567890', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/2.jpg', 1),
(36, 'user33@example.com', 'Ava', 'Martin', 'F', '2000-12-04', '123 Maple St', 678901, '45678901', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/3.jpg', 1),
(37, 'user34@example.com', 'James', 'Lewis', 'M', '1994-08-09', '456 Pine St', 789012, '56789012', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/4.jpg', 1),
(38, 'user35@example.com', 'Isabella', 'Taylor', 'F', '1989-03-22', '789 Elm St', 123456, '67890123', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/5.jpg', 1),
(39, 'user36@example.com', 'Liam', 'Harris', 'M', '2002-09-15', '567 Oak St', 234567, '78901234', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/6.jpg', 1),
(40, 'user37@example.com', 'Charlotte', 'Martin', 'F', '1997-04-26', '123 Elm St', 345678, '89012345', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/7.jpg', 1),
(41, 'user38@example.com', 'Noah', 'Jones', 'M', '2001-11-03', '456 Oak St', 456789, '90123456', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/8.jpg', 1),
(42, 'user39@example.com', 'Mia', 'Brown', 'F', '1993-07-12', '789 Elm St', 567890, '01234567', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/female/9.jpg', 1),
(43, 'user40@example.com', 'Ethan', 'Wilson', 'M', '1985-05-30', '123 Pine St', 678901, '12345678', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', 'https://xsgames.co/randomusers/assets/avatars/male/10.jpg', 1),
(100, 'mukminpitoyo@gmail.com', 'Mukmin', 'Pitoyo', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 1),
(101, 'sample@gmail.com', 'Sarah', 'Tan', 'F', '2003-01-01', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "https://xsgames.co/randomusers/assets/avatars/female/10.jpg", 1),
(102, 'isalsamudra@gmail.com', 'Faisal', 'Samudra', 'M', '1996-12-30', 'Sample Address', 123456, '96116907', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 1);

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`Memberships`
-- -----------------------------------------------------
INSERT INTO `memberships` VALUES 
(1, 'Monthly', 250, 'Progressive Strength Class Membership (Standard)', "Get access to our Progressive Strength Class and enjoy a well-rounded fitness experience. This membership includes monthly sessions to help you build strength and improve your overall fitness.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(2, 'Yearly', 2400, 'Progressive Strength Class Membership (Standard)', "Make a commitment to your fitness journey with our Progressive Strength Class Membership. This yearly plan gives you access to our classes, helping you achieve your strength and fitness goals throughout the year.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(3, 'Monthly', 200, 'Progressive Strength Class Membership (Student)',"Designed exclusively for students, this membership offers access to our Progressive Strength Class. Stay fit while you pursue your education with our monthly class sessions.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(4, 'Yearly', 1800, 'Progressive Strength Class Membership (Student)', "Students can enjoy a full year of fitness with this membership. Attend our Progressive Strength Class sessions and work towards a healthier lifestyle throughout the academic year.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(5, 'Monthly', 90, 'Open Gym Membership', "Embrace a consistent fitness routine with our Open Gym Membership. Enjoy a full year of access to our gym, allowing you to stay active and work towards your fitness goals.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(6, 'Yearly', 900, 'Open Gym Membership', "Embrace a consistent fitness routine with our Open Gym Membership. Enjoy a full year of access to our gym, allowing you to stay active and work towards your fitness goals.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(7, 'One-Time', 260, 'Beginner Olympic Weightlifting Course', "Discover the world of Olympic weightlifting with our Beginner Course. This one-time fee covers the cost of the course, where you'll learn the fundamentals of safe and effective weightlifting.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(8, 'One-Time', 150, 'Barbell Fundamentals Course', "Master the art of working with barbells through our Fundamentals Course. This one-time fee grants you access to the course, where you'll learn essential techniques and principles.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG");

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`MembershipRecord`
-- -----------------------------------------------------
INSERT INTO `MembershipRecord` VALUES 
(1, 100, 5, '2023-01-15', '2023-05-15', 'Active', NULL),
(2, 101, 2, '2022-08-28', '2023-08-28', 'Active', NULL),
(3, 43, 2, '2023-01-01', '2024-01-01', 'Active', NULL),
(4, 102, 1, '2023-07-02', '2023-09-02', 'Active', NULL);
-- (7, 103, 1, '2023-04-01', '2023-12-31', 'Inactive'),
-- (8, 104, 2, '2023-05-01', '2023-12-31', 'Inactive'),
-- (9, 105, 4, '2023-06-01', '2023-12-31', 'Inactive'),
-- (10, 106, 3, '2023-07-01', '2023-12-31', 'Inactive'),
-- (11, 107, 1, '2023-08-01', '2023-12-31', 'Inactive'),
-- (12, 108, 4, '2023-09-01', '2023-12-31', 'Inactive'),
-- (13, 109, 2, '2023-10-01', '2023-12-31', 'Inactive');

INSERT INTO `MembershipLog` VALUES 
(900, '2023-01-01', 'Created', 'Membership record created', 1),
(901, '2023-01-01', 'Created', 'Membership record created', 2),
(902, '2023-01-01', 'Created', 'Membership record created', 3),
(903, '2023-01-01', 'Created', 'Membership record created', 4);
-- (904, '2023-02-01', 'Created', 'Membership record created', 5),
-- (905, '2023-03-01', 'Created', 'Membership record created', 6);
-- (906, '2023-04-01', 'Membership record created', 'Created', 7),
-- (907, '2023-05-01', 'Membership record created', 'Created', 8),
-- (908, '2023-06-01', 'Membership record created', 'Created', 9),
-- (909, '2023-07-01', 'Membership record created', 'Created', 10),
-- (910, '2023-08-01', 'Membership record created', 'Created', 11),
-- (911, '2023-09-01', 'Membership record created', 'Created', 12),
-- (912, '2023-10-01', 'Membership record created', 'Created', 13);

INSERT INTO `Payment` VALUES
(7000, NULL, 1, '2023-01-15', 90, 0, 'PayNow'),
(7001, NULL, 1, '2023-02-15', 90, 0, 'PayNow'),
(7002, NULL, 1, '2023-03-15', 90, 0, 'PayNow'),
(7003, NULL, 1, '2023-04-15', 90, 0, 'PayNow'),
(7004, NULL, 2, '2023-01-01', 2400, 0, 'PayNow'),
(7005, NULL, 3, '2023-01-01', 2400, 0, 'PayNow'),
(7006, NULL, 4, '2023-07-02', 250, 0, 'PayNow'),
(7007, NULL, 4, '2023-08-02', 250, 0, 'PayNow');