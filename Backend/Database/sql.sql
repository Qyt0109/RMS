CREATE TABLE job_statuses (
        id INTEGER NOT NULL, 
        name VARCHAR(64) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)



CREATE TABLE genders (
        id INTEGER NOT NULL, 
        name VARCHAR(64) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)



CREATE TABLE application_form_statuses (
        id INTEGER NOT NULL, 
        name VARCHAR(64), 
        status VARCHAR(64), 
        PRIMARY KEY (id)
)



CREATE TABLE requisition_statuses (
        id INTEGER NOT NULL, 
        name VARCHAR(64), 
        status VARCHAR(64), 
        PRIMARY KEY (id)
)



CREATE TABLE users (
        id INTEGER NOT NULL, 
        username VARCHAR(64) NOT NULL, 
        password_hash VARCHAR(64) NOT NULL, 
        name VARCHAR(64) NOT NULL, 
        email VARCHAR(64) NOT NULL, 
        phone_number VARCHAR(64), 
        birthday DATE NOT NULL, 
        role VARCHAR(64), 
        avatar BLOB, 
        gender_id INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (username), 
        UNIQUE (email), 
        FOREIGN KEY(gender_id) REFERENCES genders (id)
)



CREATE TABLE jobs (
        id INTEGER NOT NULL, 
        name VARCHAR(64) NOT NULL, 
        description VARCHAR(64) NOT NULL, 
        pay VARCHAR(64) NOT NULL, 
        requirement VARCHAR(64) NOT NULL, 
        job_status_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name), 
        FOREIGN KEY(job_status_id) REFERENCES job_statuses (id)
)



CREATE TABLE requisitions (
        id INTEGER NOT NULL, 
        name VARCHAR(64), 
        requisition_status_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(requisition_status_id) REFERENCES requisition_statuses (id)
)



CREATE TABLE admins (
        id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(id) REFERENCES users (id)
)



CREATE TABLE candidates (
        id INTEGER NOT NULL, 
        citizen_identification_code VARCHAR(64), 
        address VARCHAR(64), 
        skill VARCHAR(64), 
        academic_level VARCHAR(64), 
        experience VARCHAR(64), 
        degree VARCHAR(64), 
        PRIMARY KEY (id), 
        FOREIGN KEY(id) REFERENCES users (id)
)



CREATE TABLE interviewers (
        id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(id) REFERENCES users (id)
)



CREATE TABLE job_managers (
        id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(id) REFERENCES users (id)
)



CREATE TABLE interviewer_assignments (
        id INTEGER NOT NULL, 
        interview_location VARCHAR(64) NOT NULL, 
        interview_datetime DATETIME NOT NULL, 
        note VARCHAR(64), 
        interviewer_id INTEGER NOT NULL, 
        job_manager_id INTEGER NOT NULL, 
        candidate_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(interviewer_id) REFERENCES interviewers (id), 
        FOREIGN KEY(job_manager_id) REFERENCES job_managers (id), 
        FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)



CREATE TABLE application_forms (
        id INTEGER NOT NULL, 
        cv BLOB, 
        candidate_id INTEGER NOT NULL, 
        job_id INTEGER NOT NULL, 
        appliction_form_status_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(candidate_id) REFERENCES candidates (id), 
        FOREIGN KEY(job_id) REFERENCES jobs (id), 
        FOREIGN KEY(appliction_form_status_id) REFERENCES application_form_statuses (id)
)


INSERT INTO genders (name)
VALUES ('Male',)

INSERT INTO job_statuses (name)
VALUES ('Hiring',)

INSERT INTO users (username, password_hash, name, email, phone_number, birthday, role, avatar, gender_id)
VALUES ('admin1', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Admin Number 1', 'admin1@gmail.com', None, '2001-01-01', 'ADMIN', None, 1)
INSERT INTO admins (id)
VALUES (1,)

INSERT INTO candidates (id, citizen_identification_code, address, skill, academic_level, experience, degree)
VALUES (6, 'xxx2', '2 Street', 'Skill number 2', 'academic level 2', 'Test 2', 'Good 2')

INSERT INTO jobs (name, description, pay, requirement, job_status_id)
VALUES ('Job 1', "This is job 1's description...", '1.000.000.000 $ / Year', 'Required: Must have 1', 2)




