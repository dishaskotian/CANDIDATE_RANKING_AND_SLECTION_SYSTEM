CREATE DATABASE candidate_db;
USE candidate_db;


CREATE TABLE candidates (
    Candidate_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Contact_Info VARCHAR(20),
    Degree VARCHAR(50),
    Grad_Year INT,
    Education VARCHAR(100),
    Experience INT,
    Application_Date DATE
);

CREATE TABLE evaluation (
    Evaluation_ID INT PRIMARY KEY AUTO_INCREMENT,
    Candidate_ID INT,
    Evaluation_Type VARCHAR(50),
    Score INT CHECK (Score BETWEEN 0 AND 100),
    Feedback TEXT,
    Evaluation_Date DATE,
    FOREIGN KEY (Candidate_ID) REFERENCES candidates(Candidate_ID) ON DELETE CASCADE
);

CREATE TABLE skill (
    Skill_ID INT PRIMARY KEY AUTO_INCREMENT,
    Skill_Name VARCHAR(50)
);

CREATE TABLE candidate_skills (
    Candidate_ID INT,
    Skill_ID INT,
    Proficiency_Level VARCHAR(20),
    FOREIGN KEY (Candidate_ID) REFERENCES candidates(Candidate_ID) ON DELETE CASCADE,
    FOREIGN KEY (Skill_ID) REFERENCES skill(Skill_ID) ON DELETE CASCADE
);



