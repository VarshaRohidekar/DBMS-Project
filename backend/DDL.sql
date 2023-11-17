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
    interested_domain varchar(50) not null,
    idea varchar(140),
    req_status int not null check(req_status in (-1, 0, 1)),
    constraint team_id_ref foreign key (team_id) references Team(team_id) 
            on update cascade on delete cascade,
    constraint super_id_ref foreign key (supervisor_id) references Supervisor(supervisor_id)
            on update cascade on delete set default
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

create table Document (
    project_id int,
    phase int check(phase in (1,2,3)),
    dname varchar(20) not null,
    dfile blob not null,
    primary key(project_id, phase),
    foreign key (project_id) references Project(project_id)
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