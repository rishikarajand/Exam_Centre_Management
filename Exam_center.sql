show databases;
create database exam_center_db;
use exam_center_db;
show tables;

-- Create the Student table
CREATE TABLE Student (
    StudentID VARCHAR(100) PRIMARY KEY,
    first_name varchar(100),
    last_name  varchar(100),
    Name varchar(200) as (concat_ws(' ', first_name, last_name)),
    Email VARCHAR(100),
    Address VARCHAR(100),
    State varchar(100),
    City varchar(100),
    Pincode varchar(100),
    AddressS varchar(400) AS (concat_ws(' ', State, City, Pincode)),
    DateOfBirth DATE,
    Age INT 
);

DELIMITER //

CREATE TRIGGER calculate_age
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    SET NEW.Age = YEAR(CURDATE()) - YEAR(NEW.DateOfBirth);
END;

CREATE TRIGGER update_age
BEFORE UPDATE ON Student
FOR EACH ROW
BEGIN
    SET NEW.Age = YEAR(CURDATE()) - YEAR(NEW.DateOfBirth);
END;
//
DELIMITER ;

INSERT INTO Student (StudentID, first_name, last_name, Email, Address, State, City, Pincode, DateOfBirth)
VALUES 
('S001', 'John', 'Doe', 'john.doe@email.com', '123 Main St', 'California', 'Los Angeles', '90001', '1990-05-15'),
('S002', 'Jane', 'Smith', 'jane.smith@email.com', '456 Oak St', 'New York', 'New York City', '10001', '1992-08-22'),
('S003', 'Alice', 'Johnson', 'alice.johnson@email.com', '789 Pine St', 'Texas', 'Houston', '77002', '1995-03-10'),
('S004', 'Bob', 'Williams', 'bob.williams@email.com', '101 Elm St', 'Florida', 'Miami', '33101', '1991-11-30'),
('S005', 'Eva', 'Miller', 'eva.miller@email.com', '202 Cedar St', 'Illinois', 'Chicago', '60601', '1993-07-18'),
('S006', 'David', 'Davis', 'david.davis@email.com', '303 Walnut St', 'Ohio', 'Columbus', '43201', '1994-09-25'),
('S007', 'Grace', 'Brown', 'grace.brown@email.com', '404 Maple St', 'Arizona', 'Phoenix', '85001', '1996-02-03'),
('S008', 'Charlie', 'Jones', 'charlie.jones@email.com', '505 Birch St', 'Colorado', 'Denver', '80202', '1990-12-14'),
('S009', 'Olivia', 'White', 'olivia.white@email.com', '606 Oak St', 'Washington', 'Seattle', '98101', '1992-06-08'),
('S010', 'Michael', 'Moore', 'michael.moore@email.com', '707 Pine St', 'Georgia', 'Atlanta', '30301', '1994-04-05');

-- Create the Exam table
CREATE TABLE Exam (
    ExamID VARCHAR(100) PRIMARY KEY,
    ExamName VARCHAR(100),
    ExamDate DATE,
    ExamDuration INT,
    TotalMarks INT
);

desc table exam;
INSERT INTO Exam (ExamID, ExamName, ExamDate, ExamDuration, TotalMarks)
VALUES 
('E001', 'Math Exam', '2023-12-01', 120, 100),
('E002', 'Science Exam', '2023-12-05', 90, 80),
('E003', 'History Exam', '2023-12-10', 60, 50),
('E004', 'English Exam', '2023-12-15', 75, 70),
('E005', 'Physics Exam', '2023-12-20', 100, 90),
('E006', 'Chemistry Exam', '2023-12-25', 80, 75),
('E007', 'Biology Exam', '2023-12-30', 70, 60),
('E008', 'Computer Science Exam', '2024-01-05', 45, 40),
('E009', 'Geography Exam', '2024-01-10', 55, 50),
('E010', 'Economics Exam', '2024-01-15', 65, 60);

DELIMITER //

CREATE PROCEDURE display_exam_table()
BEGIN
    SELECT * FROM Exam;
END 

DELIMITER ;


-- Create the ExamCenter table
CREATE TABLE ExamCenter (
    CenterID VARCHAR(100) PRIMARY KEY,
    CenterName VARCHAR(100),
    Location VARCHAR(100),
    RoomID VARCHAR(100),  -- Foreign key
    ExamID VARCHAR(100),  -- Foreign key
    RegisterID VARCHAR(100)  -- Foreign key
);
INSERT INTO ExamCenter (CenterID, CenterName, Location, RoomID, ExamID, RegisterID)
VALUES 
('C001', 'Center A', 'Location A', 'R001', 'E001', 'Reg001'),
('C002', 'Center B', 'Location B', 'R002', 'E002', 'Reg002'),
('C003', 'Center C', 'Location C', 'R003', 'E003', 'Reg003'),
('C004', 'Center D', 'Location D', 'R004', 'E004', 'Reg004'),
('C005', 'Center E', 'Location E', 'R005', 'E005', 'Reg005'),
('C006', 'Center F', 'Location F', 'R006', 'E006', 'Reg006'),
('C007', 'Center G', 'Location G', 'R007', 'E007', 'Reg007'),
('C008', 'Center H', 'Location H', 'R008', 'E008', 'Reg008'),
('C009', 'Center I', 'Location I', 'R009', 'E009', 'Reg009'),
('C010', 'Center J', 'Location J', 'R010', 'E010', 'Reg010');


-- Create the ExamRoom table
CREATE TABLE ExamRoom (
    RoomID VARCHAR(100) PRIMARY KEY,
    SeatID VARCHAR(100)  -- Foreign key
);
INSERT INTO ExamRoom (RoomID, SeatID)
VALUES 
('R001', 'Seat001'),
('R002', 'Seat002'),
('R003', 'Seat003'),
('R004', 'Seat004'),
('R005', 'Seat005'),
('R006', 'Seat006'),
('R007', 'Seat007'),
('R008', 'Seat008'),
('R009', 'Seat009'),
('R010', 'Seat010');


-- Create the Seat table
CREATE TABLE Seat (
    SeatID VARCHAR(100) PRIMARY KEY,
    StudentID VARCHAR(100)  -- Foreign key
);
INSERT INTO Seat (SeatID, StudentID)
VALUES 
('Seat001', 'S001'),
('Seat002', 'S002'),
('Seat003', 'S003'),
('Seat004', 'S004'),
('Seat005', 'S005'),
('Seat006', 'S006'),
('Seat007', 'S007'),
('Seat008', 'S008'),
('Seat009', 'S009'),
('Seat010', 'S010');


-- Create the Registration table
CREATE TABLE Registration (
    RegisterID VARCHAR(100) PRIMARY KEY,
    RegistrationDate DATE,
    StudentID VARCHAR(100),  -- Foreign key
    ExamID VARCHAR(100)  -- Foreign key
);

ALTER TABLE Registration
ADD COLUMN ExamName VARCHAR(100);

-- Update ExamName in Registration table using JOIN
UPDATE Registration
JOIN Exam ON Registration.ExamID = Exam.ExamID
SET Registration.ExamName = Exam.ExamName;

INSERT INTO Registration (RegisterID, RegistrationDate, StudentID, ExamID)
VALUES 
('Reg001', '2023-11-01', 'S001', 'E001'),
('Reg002', '2023-11-02', 'S002', 'E002'),
('Reg003', '2023-11-03', 'S003', 'E003'),
('Reg004', '2023-11-04', 'S004', 'E004'),
('Reg005', '2023-11-05', 'S005', 'E005'),
('Reg006', '2023-11-06', 'S006', 'E006'),
('Reg007', '2023-11-07', 'S007', 'E007'),
('Reg008', '2023-11-08', 'S008', 'E008'),
('Reg009', '2023-11-09', 'S009', 'E009'),
('Reg010', '2023-11-10', 'S010', 'E010');

-- Create the Result table
CREATE TABLE Result (
    RegisterID VARCHAR(100),  -- Foreign key
    MarksObtained INT,  
    Grade enum ("pass", "fail"),
    ExamName VARCHAR(100)  -- Foreign key
);
INSERT INTO Result (RegisterID, MarksObtained, Grade, ExamName)
VALUES 
('Reg001', 90, 'pass', 'Math Exam'),
('Reg002', 75, 'pass', 'Science Exam'),
('Reg003', 50, 'fail', 'History Exam'),
('Reg004', 70, 'pass', 'English Exam'),
('Reg005', 95, 'pass', 'Physics Exam'),
('Reg006', 80, 'pass', 'Chemistry Exam'),
('Reg007', 55, 'fail', 'Biology Exam'),
('Reg008', 40, 'fail', 'Computer Science Exam'),
('Reg009', 60, 'pass', 'Geography Exam'),
('Reg010', 75, 'pass', 'Economics Exam');


-- Add foreign keys to the ExamCenter table
ALTER TABLE ExamCenter
ADD FOREIGN KEY (RoomID) REFERENCES ExamRoom(RoomID),
ADD FOREIGN KEY (ExamID) REFERENCES Exam(ExamID),
ADD FOREIGN KEY (RegisterID) REFERENCES Registration(RegisterID);

-- Add foreign keys to the ExamRoom table
ALTER TABLE ExamRoom
ADD FOREIGN KEY (SeatID) REFERENCES Seat(SeatID);

-- Add foreign keys to the Seat table
ALTER TABLE Seat
ADD FOREIGN KEY (StudentID) REFERENCES Student(StudentID);

-- Add foreign keys to the Registration table
ALTER TABLE Registration
ADD FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
ADD FOREIGN KEY (ExamID) REFERENCES Exam(ExamID);

-- Add foreign keys to the Result table
ALTER TABLE Result
ADD FOREIGN KEY (RegisterID) REFERENCES Registration(RegisterID);

