create database Capstone_Mapping;
use Capstone_Mapping;

/*  numeric keys make for faster lookup  */

/*

make a

*/

create table Student (
    srn char(13) primary key,
    semester int not null check (semester in (1,2,3,4,5,6,7,8)),
    cgpa float(2) check ((cgpa >=0) and (cgpa <=10)),
    Fname varchar(15) not null,
    Lname varchar(15) not null,
    email varchar(50) not null,
    resume_doc mediumblob default null,
    pswd varchar(20) not null,
    outgoing_year year not null
);

create table Teacher (
    teacher_id char(13) primary key,
    Fname varchar(15) not null,
    Lname varchar(15) not null,
    email varchar(50) not null,
    floor int default null,
    cabin_no varchar(10) default null,
    pswd varchar(20) not null,
    unique (floor, cabin_no)
);

create table Admin (
    admin_id char(7) primary key,
    pswd varchar(30) not null,
    email varchar(70) not null
);

create table Team (
    team_id int primary key auto_increment,
    team_name varchar(50) not null
);

alter table Student add team_id int;
alter table Student add foreign key (team_id) references Team(team_id) on update cascade on delete set null;

/* 

when the supervisor hits limit, automatically reject the pending requests 
if active_projects = team_limit-1 and supervisor wants to accept the last time,
need to put pop saying that this is the last team they can accept, and on accepting the request


*/

create table Supervisor (
    supervisor_id char(13) not null,
    team_limit int not null check (team_limit > 0),
    foreign key (supervisor_id) references Teacher(teacher_id) on update cascade on delete restrict
);

    /* need to find a way to be able to set domain values */

create table Supervisor_years (
    supervisor_id char(13),
    batch year,
    primary key (supervisor_id, batch),
    foreign key (supervisor_id) references Supervisor(supervisor_id) on update cascade
);

create table Domain (
    domain varchar(70) primary key
);

create table Supervisor_Domains (
    supervisor_id char(13) not null,
    domain varchar(70) not null,
    primary key (supervisor_id, domain),
    foreign key (supervisor_id) references Supervisor(supervisor_id) on update cascade on delete cascade,
    foreign key (domain) references Domain(domain) on update cascade on delete cascade
);

/* for a supervisor id being 0000000000000, return value 'this supervisor is no longer available' */

create table Request (
    request_id int primary key auto_increment,
    team_id int not null,
    supervisor_id char(13) not null default '0000000000000',
    interested_domain varchar(70) not null,
    idea varchar(140),
    req_status int not null check(req_status in (-1, 0, 1)),
    constraint team_id_ref foreign key (team_id) references Team(team_id) 
            on update cascade on delete cascade,
    constraint super_id_ref foreign key (supervisor_id) references Supervisor(supervisor_id)
            on update cascade on delete set default,
    constraint domain_ref foreign key (interested_domain) references Domain(domain)
            on update cascade on delete cascade
);

/* an accepted request from the student's side should be used to create the project entry*/

create table Project (
    project_id int primary key auto_increment,
    team_id int not null,
    supervisor_id char(13) not null,
    start_d date,
    end_d date,
    cur_phase int not null check(cur_phase in(1,2,3)),
    domain varchar(50) not null,
    problem_statement varchar(200) not null,
    foreign key(team_id) references Team(team_id),
    foreign key(supervisor_id) references Supervisor(supervisor_id)
);

create table Review (
    project_id int,
    phase int check (phase in (1,2,3)),
    grade char(1) check (grade in ('S', 'A', 'B', 'C', 'D', 'E', 'F')),
    primary key (project_id, phase),
    foreign key (project_id) references Project(project_id)
);

create table Reviewed_by (
    project_id int,
    phase int check(phase in (1,2,3)),
    reviewer_id char(13) not null,
    feedback varchar(200) default null,
    primary key(project_id, phase, reviewer_id),
    foreign key(project_id) references Project(project_id),
    foreign key(reviewer_id) references Teacher(teacher_id)
);

-- create table latest_id (
--     table_name varchar(20) primary key check (table_name in ('Team', 'Request', 'Project')),
--     last_id char(10) not null
-- );


-- /*  setting base values for request ids  */
-- insert into latest_id values ('Team', '0000000000');
-- insert into latest_id values ('Request', '0000000000');
-- insert into latest_id values ('Project', '0000000000');

CREATE VIEW supervisor_projects AS 
WITH active_projects_count (supervisor_id, active_projects)
AS (
    SELECT supervisor_id, count(project_id)
    FROM Project
    WHERE end_d is NULL
    GROUP BY supervisor_id
),
accepted_request_count (supervisor_id, accepted_requests)
AS (
    SELECT supervisor_id, count(*)
    FROM Request
    WHERE req_status = 1
    GROUP BY supervisor_id
)
SELECT S.supervisor_id as supervisor_id, team_limit, active_projects, accepted_requests FROM Supervisor S 
left join active_projects_count on active_projects_count.supervisor_id=S.supervisor_id
left join accepted_request_count on accepted_request_count.supervisor_id=S.supervisor_id;

delimiter //

CREATE PROCEDURE team_avg_cgpa(IN team_id int)
    BEGIN
    SELECT s.team_id, avg(s.cgpa) FROM Student s GROUP BY s.team_id HAVING s.team_id=team_id;
    END //


CREATE TRIGGER delete_requests
    AFTER INSERT ON Project
    FOR EACH ROW
    BEGIN
    DECLARE p INT;
    DECLARE r INT;
    DECLARE t INT;

    DELETE FROM Request WHERE team_id=NEW.team_id;


    SELECT team_limit, active_projects INTO t, p
    FROM supervisor_projects
    WHERE supervisor_id = NEW.supervisor_id;

    IF p IS NOT NULL THEN 
        IF t<=p THEN
            UPDATE Request SET req_status=-1 WHERE supervisor_id=NEW.supervisor_id;
        END IF;
    END IF;

    END //

-- CREATE PROCEDURE decrement_active_projects(IN project_id int)
--     BEGIN
--     DECLARE supervisor_id varchar(15);
--     SELECT p.supervisor_id INTO supervisor_id
--     FROM Project p
--     WHERE p.project_id=project_id;
--     UPDATE Supervisor
--     SET active_projects = active_projects - 1
--     WHERE Supervisor.supervisor_id = supervisor_id;
--     END //

CREATE TRIGGER adding_review
    BEFORE INSERT ON Review 
    FOR EACH ROW 
    BEGIN 
        DECLARE num INT;
        SELECT count(*) INTO num 
        FROM Reviewed_by
        WHERE project_id=NEW.project_id AND phase=NEW.phase;
        IF num < 1 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No reviewer has posted their review yet';
        END IF;
    END //
    
delimiter ;


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
('PES1UG20CS512', 7, 8.33, 'Nambrata', 'A', 'nambrataa@example.com', 'ABC', 2024),
('PES1UG21CS712', 5, 8.69, 'Prajwal', 'Rai', 'prajwalrai@example.com', 'ABC', 2025),
('PES1UG21CS713', 5, 9.23, 'HariKrishnan', 'G', 'harig@example.com', 'ABC', 2025),
('PES1UG21CS714', 5, 9.51, 'Abhinav', 'Singh', 'abhisingh@example.com', 'ABC', 2025),
('PES1UG21CS715', 5, 8.82, 'Shrishti', 'A', 'shrishtia123@example.com', 'ABC', 2025);



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
(1, 1, 'T123456789001', 'Clear Presentation.'),
(1, 1, 'T123456789003', 'Research could"ve been more thorough.'),
(1, 2, 'T123456789001', 'Needs to be more refined.'),
(1, 2, 'T123456789004', 'Good effort.'),
(2, 1, 'T123456789007', 'Comprehensive project with innovative solutions and effective communication.'),
(2, 1, 'T123456789003', 'Timely delivery and user-friendly interface contribute to success.'),
(2, 2, 'T123456789009', 'User interface is intuitive, enhancing overall experience.'),
(2, 2, 'T123456789005', 'Great adaptability in handling changes.'),
(3, 1, 'T123456789004', 'Attention to detail in planning and execution ensures accuracy.'),
(3, 1, 'T123456789007', 'Measurable impact on targeted goals.'),
(3, 2, 'T123456789009', 'Effective teamwork is evident in collaborative efforts.'),
(3, 2, 'T123456789005', 'Thorough research and analysis contribute significantly to the project"s depth.');

INSERT INTO Review (project_id, phase, grade) VALUES 
(1, 1, 'A'),
(1, 2, 'B'),
(2, 1, 'S'),
(2, 2, 'B'),
(3, 1, 'A'),
(3, 2, 'S');
