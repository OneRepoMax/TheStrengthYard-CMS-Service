-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`User`
-- -----------------------------------------------------
INSERT INTO `User` VALUES 
(1, 'testuser@tsy.com', 'John', 'Doe', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0),
(100, 'mukminpitoyo@gmail.com', 'Mukmin', 'Pitoyo', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0),
(101, 'sample@gmail.com', 'Sarah', 'Tan', 'F', '2003-01-01', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0),
(102, 'isalsamudra@gmail.com', 'Faisal', 'Samudra', 'M', '1996-12-30', 'Sample Address', 123456, '96116907', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0);

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
-- Inserting Sample Data into Table `tsy_db`.`MembershipRecord`
-- -----------------------------------------------------
INSERT INTO `MembershipRecord` VALUES 
(1, 100, 5, '2023-01-01', '2023-05-01', 'Active'),
(2, 101, 2, '2023-01-01', '2024-01-01', 'Active');

