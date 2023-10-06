-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`User`
-- -----------------------------------------------------
INSERT INTO `User` VALUES 
(1, 'testuser@tsy.com', 'Bob', 'Stewart', 'M', '1997-05-29', 'Sample Address', 123456, '96116908', 'pbkdf2:sha256:260000$hJm022YX$5cdc10522fe8bdca504ffceff61f8a7822eb3de05b3e29efee100e246c8e804d', 'C', '2023-08-16', "https://tsy-fyp-user-display-picture.s3.ap-southeast-1.amazonaws.com/ee9c81a6-e7c0-436a-a09d-8be00be9e0a5.gif", 1),
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
-- Inserting Sample Data into Table `tsy_db`.`IndemnityForm`
-- -----------------------------------------------------
INSERT INTO `IndemnityForm` VALUES
(300, "Search Engine, Friend's Recommendation, Walking Pass, Google Maps, Facebook Adverts, Google Adverts, Other", "Heart Problems, Pain in Chest when exercising/not exercising, Low Blood Pressure/High Blood Pressure, Any breathing difficulties or asthma, Diabetes, Fainting spells, Joint problems, Epilepsy, Currently on medication, Significant illness/Operations, None, Other","I had a heart operation back in 2008 and my knees are very weak. I am also on medication for my heart. I also have fainting spells once in a while.", 1, 1, 1),
(301, "Search Engine, Friend's Recommendation, Walking Pass, Google Maps, Facebook Adverts, Google Adverts, Other", "Heart Problems, Pain in Chest when exercising/not exercising, Low Blood Pressure/High Blood Pressure, Any breathing difficulties or asthma, Diabetes, Fainting spells, Joint problems, Epilepsy, Currently on medication, Significant illness/Operations, None, Other","I had a heart operation back in 2008 and my knees are very weak. I am also on medication for my heart. I also have fainting spells once in a while.", 1, 1, 102);


-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`Memberships`
-- -----------------------------------------------------
INSERT INTO `memberships` VALUES 
(1, 'Monthly', "Public", 250, 'Progressive Strength Class Membership (Standard)', "Get access to our Progressive Strength Class and enjoy a well-rounded fitness experience. This membership includes monthly sessions to help you build strength and improve your overall fitness.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-3Y5474454G139761KMUA2YTA", 70),
(2, 'Yearly', "Public", 2400, 'Progressive Strength Class Membership (Standard)', "Make a commitment to your fitness journey with our Progressive Strength Class Membership. This yearly plan gives you access to our classes, helping you achieve your strength and fitness goals throughout the year.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-7VE04701FA968924KMUA3ADA", 70),
(3, 'Monthly', "Public", 200, 'Progressive Strength Class Membership (Student)',"Designed exclusively for students, this membership offers access to our Progressive Strength Class. Stay fit while you pursue your education with our monthly class sessions.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-2CG607110D459422MMUECUIA", 70),
(4, 'Yearly', "Public", 1800, 'Progressive Strength Class Membership (Student)', "Students can enjoy a full year of fitness with this membership. Attend our Progressive Strength Class sessions and work towards a healthier lifestyle throughout the academic year.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-9K282057GE548025UMUECU6I", 70),
(5, 'Monthly', "Public", 90, 'Open Gym Membership', "Embrace a consistent fitness routine with our Open Gym Membership. Enjoy a full year of access to our gym, allowing you to stay active and work towards your fitness goals.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-28V320045U278380RMUA3XOI", 70),
(6, 'Yearly', "Public", 900, 'Open Gym Membership', "Embrace a consistent fitness routine with our Open Gym Membership. Enjoy a full year of access to our gym, allowing you to stay active and work towards your fitness goals.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-57K47766M4645771LMUECVWY", 70),
(7, 'One-Time', "Public", 260, 'Beginner Olympic Weightlifting Course', "Discover the world of Olympic weightlifting with our Beginner Course. This one-time fee covers the cost of the course, where you'll learn the fundamentals of safe and effective weightlifting.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", NULL, 0),
(8, 'One-Time', "Public", 150, 'Barbell Fundamentals Course', "Master the art of working with barbells through our Fundamentals Course. This one-time fee grants you access to the course, where you'll learn essential techniques and principles.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", NULL, 0),
(9, 'Monthly', "Private", 250, 'Progressive Strength Class Membership (Standard) discounted', "Get access to our Progressive Strength Class and enjoy a well-rounded fitness experience. This membership includes monthly sessions to help you build strength and improve your overall fitness.", "https://tsy-admin-bucket.s3.ap-southeast-1.amazonaws.com/AEC1ADBF-6A40-4150-BC9E-169496C3E737-1022-0000175AF0BEA8F0.JPG", "P-3Y5474454G139761KMUA2YTA", 70);

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`MembershipRecord`
-- -----------------------------------------------------
INSERT INTO `MembershipRecord` VALUES 
(1, "I-AYW50U49PVHR", 100, 5, '2023-09-17', '2023-10-17', 'Active', NULL),
(2, "I-4HNBN7BYS9R1", 1, 1, '2023-09-20', '2023-10-20', 'Active', NULL),
(3, "I-BW42BRSB56P0", 3, 5, '2023-09-19', '2023-10-19', 'Active', NULL);
-- (3, 43, 2, '2023-01-01', '2024-01-01', 'Active', NULL),
-- (4, 102, 1, '2023-07-02', '2023-09-14', 'Active', NULL);
-- (5, 101, 3, '2023-02-01', '2023-12-31', 'Active'),
-- (6, 102, 2, '2023-03-01', '2023-12-31', 'Active');
-- (7, 103, 1, '2023-04-01', '2023-12-31', 'Inactive'),
-- (8, 104, 2, '2023-05-01', '2023-12-31', 'Inactive'),
-- (9, 105, 4, '2023-06-01', '2023-12-31', 'Inactive'),
-- (10, 106, 3, '2023-07-01', '2023-12-31', 'Inactive'),
-- (11, 107, 1, '2023-08-01', '2023-12-31', 'Inactive'),
-- (12, 108, 4, '2023-09-01', '2023-12-31', 'Inactive'),
-- (13, 109, 2, '2023-10-01', '2023-12-31', 'Inactive');

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`MembershipLog`
-- -----------------------------------------------------
INSERT INTO `MembershipLog` VALUES 
(900, '2023-09-17', 'Created', 'Membership record created', 1),
(901, '2023-09-20', 'Created', 'Membership record created', 2),
(902, '2023-09-19', 'Created', 'Membership record created', 3);
-- (903, '2023-07-02', 'Created', 'Membership record created', 4);
-- (904, '2023-02-01', 'Created', 'Membership record created', 5),
-- (905, '2023-03-01', 'Created', 'Membership record created', 6);
-- (906, '2023-04-01', 'Membership record created', 'Created', 7),
-- (907, '2023-05-01', 'Membership record created', 'Created', 8),
-- (908, '2023-06-01', 'Membership record created', 'Created', 9),
-- (909, '2023-07-01', 'Membership record created', 'Created', 10),
-- (910, '2023-08-01', 'Membership record created', 'Created', 11),
-- (911, '2023-09-01', 'Membership record created', 'Created', 12),
-- (912, '2023-10-01', 'Membership record created', 'Created', 13);

-- -----------------------------------------------------
-- Inserting Sample Data into Table `tsy_db`.`Payment`
-- -----------------------------------------------------
INSERT INTO `Payment` VALUES
(7000, "5R580284D01408702", 1, '2023-09-17', 90, 0, 'PayPal'),
(7001, "7XG40156VL4166704", 2, '2023-09-20', 250, 0, 'PayPal'),
(7002, "57M12318994098505", 3, '2023-09-19', 90, 0, 'PayPal');
-- (7002, NULL, 1, '2023-03-15', 90, 0, 'PayNow'),
-- (7003, NULL, 1, '2023-04-15', 90, 0, 'PayNow'),
-- (7004, NULL, 2, '2023-01-01', 2400, 0, 'PayNow'),
-- (7005, NULL, 3, '2023-01-01', 2400, 0, 'PayNow'),
-- (7006, NULL, 4, '2023-07-02', 250, 0, 'PayNow'),
-- (7007, NULL, 4, '2023-08-02', 250, 0, 'PayNow');




