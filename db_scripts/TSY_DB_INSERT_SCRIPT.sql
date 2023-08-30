-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`User`
-- -----------------------------------------------------
INSERT INTO `User` VALUES 
(1, 'testuser@tsy.com', 'John', 'Doe', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0),
(2, 'admin@tsy.com', 'John', 'Doe', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'A', '2023-08-16', "", 0),
(100, 'mukminpitoyo@gmail.com', 'Mukmin', 'Pitoyo', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0),
(101, 'sample@gmail.com', 'Sarah', 'Tan', 'F', '2003-01-01', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0),
(102, 'isalsamudra@gmail.com', 'Faisal', 'Samudra', 'M', '1996-12-30', 'Sample Address', 123456, '96116907', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "", 0);

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`Memberships`
-- -----------------------------------------------------
INSERT INTO `Memberships` VALUES 
(1, 'Monthly', 250, 'Progressive Strength Class Membership (Standard)', "Get access to our Progressive Strength Class and enjoy a well-rounded fitness experience. This membership includes monthly sessions to help you build strength and improve your overall fitness.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(2, 'Yearly', 2400, 'Progressive Strength Class Membership (Standard)', "Make a commitment to your fitness journey with our Progressive Strength Class Membership. This yearly plan gives you access to our classes, helping you achieve your strength and fitness goals throughout the year.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(3, 'Monthly', 200, 'Progressive Strength Class Membership (Student)',"Designed exclusively for students, this membership offers access to our Progressive Strength Class. Stay fit while you pursue your education with our monthly class sessions.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(4, 'Yearly', 1800, 'Progressive Strength Class Membership (Student)', "Students can enjoy a full year of fitness with this membership. Attend our Progressive Strength Class sessions and work towards a healthier lifestyle throughout the academic year.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(6, 'Yearly', 900, 'Open Gym Membership', "Embrace a consistent fitness routine with our Open Gym Membership. Enjoy a full year of access to our gym, allowing you to stay active and work towards your fitness goals.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(7, 'One-Time', 260, 'Beginner Olympic Weightlifting Course', "Discover the world of Olympic weightlifting with our Beginner Course. This one-time fee covers the cost of the course, where you'll learn the fundamentals of safe and effective weightlifting.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG"),
(8, 'One-Time', 150, 'Barbell Fundamentals Course', "Master the art of working with barbells through our Fundamentals Course. This one-time fee grants you access to the course, where you'll learn essential techniques and principles.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG");

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`MembershipRecord`
-- -----------------------------------------------------
INSERT INTO `MembershipRecord` VALUES 
(1, 100, 5, '2023-01-01', '2023-05-01', 'Active'),
(2, 101, 2, '2023-01-01', '2024-01-01', 'Active');

