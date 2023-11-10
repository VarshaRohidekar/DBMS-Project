INSERT INTO Student (srn, semester, cgpa, Fname, Lname, email, pswd, outgoing_year) values
('PES1UG21CS695', 5, 8.35, 'Vaishnavi', 'Venu', 'vaishnavigv@example.com', 'ABC', 2025),
('PES1UG21CS699', 5, 8.7, 'Varsha', 'Rohidekar', 'varshar@example.com', 'ABC', 2025),
('PES1UG21CS628', 5, 8.9, 'Stuti', 'Udupa', 'stuthiu@example.com', 'ABC', 2025),
('PES1UG21CS629', 5, 9.0, 'Stuthi', 'Pathak', 'stuthip@example.com', 'ABC', 2025),
('PES1UG21CS700', 5, 7.6, 'Adithya', 'S', 'adithyas@example.com', 'ABC', 2025),
('PES1UG21CS701', 5, 8.45, 'Adithi', 'Bhushan', 'adithib@example.com', 'ABC', 2025),
('PES1UG21CS702', 5, 7.97, 'Anagha', 'Kumble', 'anaghak@example.com', 'ABC', 2025),
('PES1UG21CS703', 5, 7.4, 'Ujjwal', 'MK', 'ujjwalmk@example.com', 'ABC', 2025),
('PES1UG21CS704', 5, 8.20, 'Varun', 'B', 'varunb@example.com', 'ABC', 2025),
('PES1UG21CS705', 5, 8.19, 'Nikhata', 'S', 'nikhatas@example.com', 'ABC', 2025),
('PES1UG21CS706', 5, 9.5, 'Ananya', 'J', 'ananyaj@example.com', 'ABC', 2025),
('PES1UG21CS707', 5, 8.0, 'Sanjana', 'M', 'sanjanam@example.com', 'ABC', 2025),
('PES1UG20CS500', 7, 9.7, 'Kruthika', 'Sanjay', 'kruthikas@example.com', 'ABC', 2024),
('PES1UG20CS501', 7, 8.04, 'Vishrutha', 'Balaji', 'vishruthab@example.com', 'ABC', 2024),
('PES1UG20CS502', 7, 10, 'Punith', 'N', 'punithn@example.com', 'ABC', 2024),
('PES1UG20CS503', 7, 9.8, 'Pranav', 'Acharya', 'pranava@example.com', 'ABC', 2024),
('PES1UG20CS504', 7, 8.94, 'Guna', 'C', 'gunac@example.com', 'ABC', 2024),
('PES1UG20CS505', 7, 8.53, 'Vedant', 'J', 'vedantj@example.com', 'ABC', 2024),
('PES1UG20CS506', 7, 7.98, 'Harshith', 'Gowda', 'harshithg@example.com', 'ABC', 2024),
('PES1UG20CS508', 7, 9.0, 'Rex', 'Lapis', 'moraxarchon@example.com', 'ABC', 2024),
('PES1UG20CS509', 7, 7.5, 'Laasya', 'G', 'laasyag@example.com', 'ABC', 2024),
('PES1UG20CS510', 7, 8.93, 'Shrikar', 'M', 'shrikarm@example.com', 'ABC', 2024),
('PES1UG20CS511', 7, 9.8, 'Aryan', 'Agarwal', 'aryana@example.com', 'ABC', 2024),
('PES1UG20CS512', 7, 8.33, 'Nambrata', 'A', 'nambrataa@example.com', 'ABC', 2024);


INSERT INTO Teacher (teacher_id, Fname, Lname, email, floor, cabin_no, pswd) VALUES 
('T123456789000', 'Sowmya', 'R', 'sowmyar@example.com', 0, 1, 'DEF'),
('T123456789001', 'Pavan', 'A', 'pavana@example.com', 1, 2, 'DEF'),
('T123456789002', 'Vidhya', 'C', 'vidhyac@example.com', 3, 6, 'DEF'),
('T123456789003', 'Narayan', 'Desai', 'narayand@example.com', 4, 5, 'DEF'),
('T123456789004', 'Madhu', 'P', 'madhu@example.com', 5, 2, 'DEF'),
('T123456789005', 'Sundar', 'L', 'sundarl@example.com', 2, 1, 'DEF'),
('T123456789006', 'Jyothi', 'Kumar', 'jyothik@example.com', 3, 1, 'DEF'),
('T123456789007', 'Shankar', 'Sathish', 'shankars@example.com', 9, 2, 'DEF'),
('T123456789008', 'Shwetha', 'N', 'shwethan@example.com', 8, 7, 'DEF'),
('T123456789009', 'Hrudaya', 'Naidu', 'hrudayan@example.com', 7, 4, 'DEF');

INSERT INTO `Admin` (admin_id, pswd, email) VALUES 
('A1B2C3D', 'Password123', 'user1@example.com'),
('E4F5G6H', 'SecurePass123', 'user2@example.com'),
('I7J8K9L', 'SecretPwd456', 'user3@example.com');

/* 'T123456789005' and  'T123456789002' have one 7th sem team each   */

/* 'T123456789008' only took for the current 7th sem  and has one team under them*/
INSERT INTO `Supervisor` (supervisor_id, team_limit) VALUES 
('T123456789000', 2),
('T123456789002', 2),
('T123456789005', 2),
('T123456789006', 2),
('T123456789008', 2);

INSERT INTO `Domain` (domain) VALUES 
('Computer Vision'),
('Natural Language Processing'),
('Data Analytics'),
('Machine Learning'),
('AR/VR'),
('Cloud Computing'),
('Image Processing');

INSERT INTO `Supervisor_Domains` (supervisor_id, domain) VALUES 
('T123456789000', 'Computer Vision'),
('T123456789000', 'Data Analytics'),
('T123456789002', 'Machine Learning'),
('T123456789002', 'Image Processing'),
('T123456789005', 'Machine Learning'),
('T123456789005', 'Natural Language Processing'),
('T123456789005', 'Cloud Computing'),
('T123456789006', 'AR/VR'),
('T123456789006', 'Image Processing'),
('T123456789006', 'Cloud Computing'),
('T123456789008', 'Natural Language Processing'),
('T123456789008', 'Data Analytics');

INSERT INTO `Supervisor_years` (supervisor_id, batch) VALUES 
('T123456789000', 2025),
('T123456789002', 2025),
('T123456789002', 2024),
('T123456789005', 2025),
('T123456789005', 2024),
('T123456789006', 2025),
('T123456789008', 2024);

INSERT INTO Team (team_id, team_name) VALUES 
(1, 'ML Team'),
(2, 'NLP Team'),
(3, 'Data Analytics Team'),
(4, 'Image Processing Team');

UPDATE Student 
SET team_id = 1
WHERE srn in ('PES1UG20CS500', 'PES1UG20CS501', 'PES1UG20CS502', 'PES1UG20CS503');

UPDATE Student 
SET team_id = 2
WHERE srn in ('PES1UG20CS504', 'PES1UG20CS506', 'PES1UG20CS505', 'PES1UG20CS508');

UPDATE Student 
SET team_id = 3
WHERE srn in ('PES1UG20CS510', 'PES1UG20CS511', 'PES1UG20CS512', 'PES1UG20CS509');

UPDATE Student 
SET team_id = 4
WHERE srn in ('PES1UG21CS704', 'PES1UG21CS705', 'PES1UG21CS706', 'PES1UG21CS707');

INSERT INTO Project (team_id, supervisor_id, start_d, cur_phase, domain, problem_statement) VALUES 
(1, 'T123456789005', '2022-10-09', 3, 'Machine Learning', 'Develop a predictive model to identify patients at risk of chronic diseases'),
(2, 'T123456789002', '2022-11-27', 3, 'Natural Language Processing', 'A sentiment analysis system'),
(3, 'T123456789008', '2022-11-13', 3, 'Data Analytics', 'Optimize a supply chain by analyzing historical demand patterns and supplier performance');

INSERT INTO Reviewed_by (project_id, phase, reviewer_id, feedback) VALUES
(1, 1, 'T123456789001', 'Clear Presentation'),
(1, 1, 'T123456789003', 'Research could"ve been more thorough'),
(1, 2, 'T123456789001', 'Needs to be more refined'),
(1, 2, 'T123456789004', 'Good effort'),
(2, 1, 'T123456789007', ''),
(2, 1, 'T123456789003', ''),
(2, 2, 'T123456789009', ''),
(2, 2, 'T123456789005', ''),
(3, 1, 'T123456789004', ''),
(3, 1, 'T123456789007', ''),
(3, 2, 'T123456789009', ''),
(3, 2, 'T123456789005', '');

INSERT INTO Review (project_id, phase, grade) VALUES 
(1, 1, 'A'),
(1, 2, 'B'),
(2, 1, 'S'),
(2, 2, 'B'),
(3, 1, 'A'),
(3, 2, 'S');

