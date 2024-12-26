-- Table: Department
CREATE TABLE departments (
    department_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Table: Course
CREATE TABLE courses (
    course_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit_hours BIGINT NOT NULL check(credit_hours >= 0),
    lecturer BIGINT,
    department BIGINT,
    year BIGINT check (year >=2000 AND year <= 2100),
    room BIGINT,
    date DATETIME,
    FOREIGN KEY (department) REFERENCES departments(department_ID)
);

-- Table: Student
CREATE TABLE students (
    Student_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    national_ID INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number CHAR(15),
    Email VARCHAR(100),
    GPA FLOAT check (gpa >= 0 AND gpa <= 4),
    department_id BIGINT,
    year BIGINT,
    FOREIGN KEY (department_id) REFERENCES departments(department_ID)
);

-- Table: Tuition Fees
CREATE TABLE tuition_fees (
    invoice_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    fees BIGINT NOT NULL check (fees > 0),
    payment_method CHAR(20) CHECK (payment_method IN ('Cash', 'Credit Card', 'Bank Transfer')),
    paid BIT,
    Student_ID BIGINT,
    FOREIGN KEY (Student_ID) REFERENCES students(Student_ID)
);

-- Table: Enrolls
CREATE TABLE enrolls (
    Enroll_ID BIGINT IDENTITY(1,1) NOT NULL,
    Student_ID BIGINT NOT NULL,
    course_ID BIGINT NOT NULL,
    pre_requisite BIT NOT NULL,
    PRIMARY KEY (Enroll_ID),
    FOREIGN KEY (Student_ID) REFERENCES students(Student_ID),
    FOREIGN KEY (course_ID) REFERENCES courses(course_ID),
);

-- Table: Pre-Requisites
CREATE TABLE pre_requisites (
    course_ID BIGINT,
    pre_requisite_id BIGINT,
    PRIMARY KEY (course_ID, pre_requisite_id),
    FOREIGN KEY (course_ID) REFERENCES courses(course_ID),
    FOREIGN KEY (pre_requisite_id) REFERENCES courses(course_ID)
);

-- Table: Lecturer
CREATE TABLE lecturers (
    dr_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    national_ID BIGINT,
    name VARCHAR(100) NOT NULL,
    salary FLOAT check (salary > 0),

    department_id BIGINT,
    FOREIGN KEY (department_id) REFERENCES departments(department_ID)
);

-- Table: Teaching Assistant
CREATE TABLE teaching_assistants (
    ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary FLOAT check (salary > 0)
);

-- Table: Section
CREATE TABLE sections (
    course_ID BIGINT,
    dr_ID BIGINT,
    assistant_ID BIGINT,
    date DATETIME,
    room BIGINT,
    PRIMARY KEY (course_ID, dr_ID, assistant_ID),
    FOREIGN KEY (course_ID) REFERENCES courses(course_ID),
    FOREIGN KEY (dr_ID) REFERENCES lecturers(dr_ID),
    FOREIGN KEY (assistant_ID) REFERENCES teaching_assistants(ID)
);

-- Table: Classroom
CREATE TABLE classrooms (
    Room_number BIGINT IDENTITY(1,1) PRIMARY KEY,
    date DATETIME,
    capacity INT check (capacity > 0),
    building BIGINT
);

INSERT INTO departments (name) VALUES
('Computer Science'), ('Mathematics'), ('Physics'), ('Chemistry'), ('Biology'),
('English Literature'), ('History'), ('Philosophy'), ('Sociology'), ('Psychology'),
('Political Science'), ('Economics'), ('Business Administration'), ('Finance'), ('Marketing'),
('Accounting'), ('Management'), ('Human Resources'), ('Electrical Engineering'), ('Mechanical Engineering'),
('Civil Engineering'), ('Software Engineering'), ('Biomedical Engineering'), ('Environmental Science'), ('Architecture'),
('Fine Arts'), ('Music'), ('Theater'), ('Journalism'), ('Media Studies'),
('Law'), ('Public Administration'), ('Education'), ('Special Education'), ('Primary Education'),
('Secondary Education'), ('Linguistics'), ('Foreign Languages'), ('Geography'), ('Geology'),
('Astronomy'), ('Anthropology'), ('Criminology'), ('Health Sciences'), ('Nursing'),
('Pharmacy'), ('Medicine'), ('Dentistry'), ('Veterinary Science'), ('Agriculture'),
('Forestry'), ('Horticulture'), ('Hospitality Management'), ('Tourism'), ('Culinary Arts'),
('Sports Management'), ('Physical Education'), ('Information Technology'), ('Cybersecurity'), ('Data Science'),
('Artificial Intelligence'), ('Machine Learning'), ('Robotics'), ('Nanotechnology'), ('Genetics'),
('Biotechnology'), ('Ethics'), ('Social Work'), ('Statistics'), ('Library Science'),
('Energy Studies'), ('International Relations'), ('Urban Planning'), ('Graphic Design'), ('Interior Design'),
('Fashion Design'), ('Film Studies');


INSERT INTO courses (course_name, credit_hours, lecturer, department, year, room, date) VALUES
('Introduction to Programming', 3, 101, 1, 2024, 101, '2024-01-15'),
('Data Structures', 3, 102, 2, 2024, 102, '2024-01-16'),
('Algorithms', 3, 103, 3, 2024, 103, '2024-01-17'),
('Calculus I', 4, 201, 4, 2024, 201, '2024-01-18'),
('Linear Algebra', 3, 202, 5, 2024, 202, '2024-01-19'),
('Physics I', 4, 301, 6, 2024, 301, '2024-01-20'),
('General Chemistry', 4, 302, 7, 2024, 302, '2024-01-21'),
('Biology I', 4, 303, 8, 2024, 303, '2024-01-22'),
('Introduction to Sociology', 3, 401, 9, 2024, 401, '2024-01-23'),
('Psychology Basics', 3, 402, 10, 2024, 402, '2024-01-24'),
('Introduction to Philosophy', 3, 403, 11, 2024, 403, '2024-01-25'),
('Principles of Economics', 3, 501, 12, 2024, 501, '2024-01-26'),
('Business Management', 3, 502, 13, 2024, 502, '2024-01-27'),
('Marketing Fundamentals', 3, 503, 14, 2024, 503, '2024-01-28'),
('Financial Accounting', 3, 504, 15, 2024, 504, '2024-01-29'),
('Human Resource Management', 3, 505, 16, 2024, 505, '2024-01-30'),
('Introduction to Law', 3, 601, 17, 2024, 601, '2024-02-01'),
('Public Administration', 3, 602, 18, 2024, 602, '2024-02-02'),
('Education Psychology', 3, 603, 19, 2024, 603, '2024-02-03'),
('Secondary Education Methods', 3, 604, 20, 2024, 604, '2024-02-04'),
('Linguistic Theory', 3, 701, 21, 2024, 701, '2024-02-05'),
('Foreign Language Teaching', 3, 702, 22, 2024, 702, '2024-02-06'),
('Geographic Information Systems', 3, 703, 23, 2024, 703, '2024-02-07'),
('Geology Basics', 3, 704, 24, 2024, 704, '2024-02-08'),
('Introduction to Astronomy', 3, 705, 25, 2024, 705, '2024-02-09'),
('Anthropology 101', 3, 801, 26, 2024, 801, '2024-02-10'),
('Health and Wellness', 3, 802, 27, 2024, 802, '2024-02-11'),
('Pharmaceutical Science', 4, 803, 28, 2024, 803, '2024-02-12'),
('Principles of Nursing', 4, 804, 29, 2024, 804, '2024-02-13'),
('Introduction to Agriculture', 3, 901, 30, 2024, 901, '2024-02-14'),
('Hospitality Management', 3, 902, 31, 2024, 902, '2024-02-15'),
('Culinary Arts Basics', 3, 903, 32, 2024, 903, '2024-02-16'),
('Sports Management', 3, 904, 33, 2024, 904, '2024-02-17'),
('Introduction to Cybersecurity', 3, 1001, 34, 2024, 1001, '2024-02-18'),
('Data Science Fundamentals', 3, 1002, 35, 2024, 1002, '2024-02-19'),
('Artificial Intelligence Basics', 3, 1003, 36, 2024, 1003, '2024-02-20'),
('Machine Learning Concepts', 3, 1004, 37, 2024, 1004, '2024-02-21'),
('Robotics Engineering', 4, 1005, 38, 2024, 1005, '2024-02-22'),
('Introduction to Ethics', 3, 1101, 39, 2024, 1101, '2024-02-23'),
('Social Work Fundamentals', 3, 1102, 40, 2024, 1102, '2024-02-24'),
('Urban Planning Basics', 3, 1103, 41, 2024, 1103, '2024-02-25'),
('Graphic Design Principles', 3, 1104, 42, 2024, 1104, '2024-02-26'),
('Interior Design Basics', 3, 1105, 43, 2024, 1105, '2024-02-27'),
('Fashion Design Concepts', 3, 1106, 44, 2024, 1106, '2024-02-28'),
('Introduction to Film Studies', 3, 1107, 45, 2024, 1107, '2024-02-29'),
('Introduction to Music Theory', 3, 1108, 46, 2024, 1108, '2024-03-01'),
('Advanced Web Development', 3, 1109, 47, 2024, 1109, '2024-03-02'),
('Creative Writing 101', 3, 1110, 48, 2024, 1110, '2024-03-03'),
('Introduction to Graphic Design', 3, 1111, 49, 2024, 1111, '2024-03-04'),
('Digital Marketing Basics', 3, 1112, 50, 2024, 1112, '2024-03-05');


INSERT INTO students (national_ID, first_name, last_name, phone_number, Email, GPA, department_id, year) VALUES
(12345678, 'John', 'Doe', '1234567890', 'john.doe@example.com', 3.5, 1, 2024),
(22345678, 'Jane', 'Smith', '1234567891', 'jane.smith@example.com', 3.7, 2, 2024),
(32345678, 'Michael', 'Johnson', '1234567892', 'michael.johnson@example.com', 3.2, 3, 2024),
(42345678, 'Emily', 'Davis', '1234567893', 'emily.davis@example.com', 3.8, 4, 2024),
(52345678, 'Chris', 'Brown', '1234567894', 'chris.brown@example.com', 3.0, 5, 2024),
(62345678, 'Sarah', 'Wilson', '1234567895', 'sarah.wilson@example.com', 3.6, 6, 2024),
(72345678, 'Matthew', 'Taylor', '1234567896', 'matthew.taylor@example.com', 3.4, 7, 2024),
(82345678, 'Laura', 'Anderson', '1234567897', 'laura.anderson@example.com', 3.9, 8, 2024),
(92345678, 'David', 'Thomas', '1234567898', 'david.thomas@example.com', 2.9, 9, 2024),
(102345678, 'Sophia', 'Moore', '1234567899', 'sophia.moore@example.com', 3.1, 10, 2024),
(112345678, 'Daniel', 'Martin', '1234567800', 'daniel.martin@example.com', 3.3, 1, 2024),
(122345678, 'Olivia', 'White', '1234567801', 'olivia.white@example.com', 3.5, 2, 2024),
(132345678, 'James', 'Harris', '1234567802', 'james.harris@example.com', 3.6, 3, 2024),
(142345678, 'Ava', 'Clark', '1234567803', 'ava.clark@example.com', 3.8, 4, 2024),
(152345678, 'Benjamin', 'Lewis', '1234567804', 'benjamin.lewis@example.com', 2.7, 5, 2024),
(162345678, 'Emma', 'Walker', '1234567805', 'emma.walker@example.com', 3.4, 6, 2024),
(172345678, 'Alexander', 'Hall', '1234567806', 'alexander.hall@example.com', 3.0, 7, 2024),
(182345678, 'Mia', 'Allen', '1234567807', 'mia.allen@example.com', 3.7, 8, 2024),
(192345678, 'Ethan', 'Young', '1234567808', 'ethan.young@example.com', 3.9, 9, 2024),
(202345678, 'Isabella', 'King', '1234567809', 'isabella.king@example.com', 3.2, 10, 2024),
(212345678, 'Liam', 'Scott', '1234567810', 'liam.scott@example.com', 3.4, 1, 2024),
(222345678, 'Amelia', 'Green', '1234567811', 'amelia.green@example.com', 3.8, 2, 2024),
(232345678, 'Noah', 'Adams', '1234567812', 'noah.adams@example.com', 3.6, 3, 2024),
(242345678, 'Ella', 'Baker', '1234567813', 'ella.baker@example.com', 3.7, 4, 2024),
(252345678, 'Lucas', 'Gonzalez', '1234567814', 'lucas.gonzalez@example.com', 3.5, 5, 2024),
(262345678, 'Grace', 'Carter', '1234567815', 'grace.carter@example.com', 3.2, 6, 2024),
(272345678, 'Jack', 'Mitchell', '1234567816', 'jack.mitchell@example.com', 3.4, 7, 2024),
(282345678, 'Scarlett', 'Perez', '1234567817', 'scarlett.perez@example.com', 3.8, 8, 2024),
(292345678, 'Henry', 'Roberts', '1234567818', 'henry.roberts@example.com', 3.1, 9, 2024),
(302345678, 'Lily', 'Turner', '1234567819', 'lily.turner@example.com', 3.9, 10, 2024),
(312345678, 'Samuel', 'Phillips', '1234567820', 'samuel.phillips@example.com', 3.6, 1, 2024),
(322345678, 'Victoria', 'Campbell', '1234567821', 'victoria.campbell@example.com', 3.7, 2, 2024),
(332345678, 'Oliver', 'Parker', '1234567822', 'oliver.parker@example.com', 3.5, 3, 2024),
(342345678, 'Chloe', 'Evans', '1234567823', 'chloe.evans@example.com', 3.8, 4, 2024),
(352345678, 'Mason', 'Edwards', '1234567824', 'mason.edwards@example.com', 3.2, 5, 2024),
(362345678, 'Hannah', 'Collins', '1234567825', 'hannah.collins@example.com', 3.4, 6, 2024),
(372345678, 'Aiden', 'Stewart', '1234567826', 'aiden.stewart@example.com', 3.0, 7, 2024),
(382345678, 'Zoey', 'Sanchez', '1234567827', 'zoey.sanchez@example.com', 3.7, 8, 2024),
(392345678, 'William', 'Morris', '1234567828', 'william.morris@example.com', 3.9, 9, 2024),
(402345678, 'Evelyn', 'Rogers', '1234567829', 'evelyn.rogers@example.com', 3.5, 10, 2024),
(412345678, 'Elijah', 'Reed', '1234567830', 'elijah.reed@example.com', 3.2, 1, 2024),
(422345678, 'Charlotte', 'Cook', '1234567831', 'charlotte.cook@example.com', 3.8, 2, 2024),
(432345678, 'Gabriel', 'Morgan', '1234567832', 'gabriel.morgan@example.com', 3.7, 3, 2024),
(442345678, 'Sofia', 'Bell', '1234567833', 'sofia.bell@example.com', 3.3, 4, 2024),
(452345678, 'Andrew', 'Murphy', '1234567834', 'andrew.murphy@example.com', 3.5, 5, 2024),
(462345678, 'Madison', 'Bailey', '1234567835', 'madison.bailey@example.com', 3.6, 6, 2024),
(472345678, 'Logan', 'Rivera', '1234567836', 'logan.rivera@example.com', 3.1, 7, 2024),
(482345678, 'Ella', 'Cooper', '1234567837', 'ella.cooper@example.com', 3.4, 8, 2024),
(492345678, 'Jacob', 'Richardson', '1234567838', 'jacob.richardson@example.com', 3.7, 9, 2024),
(502345678, 'Grace', 'Cox', '1234567839', 'grace.cox@example.com', 3.9, 10, 2024),
(142345678, 'Ava', 'Clark', '1234567803', 'ava.clark@example.com', 3.8, 4, 2024),
(152345678, 'Ethan', 'Lewis', '1234567804', 'ethan.lewis@example.com', 3.4, 5, 2024),
(162345678, 'Mason', 'Young', '1234567805', 'mason.young@example.com', 3.7, 6, 2024),
(172345678, 'Isabella', 'King', '1234567806', 'isabella.king@example.com', 3.2, 7, 2024);


INSERT INTO tuition_fees (fees, payment_method, paid, Student_ID) VALUES
(5000, 'Credit Card', 1, 1),     (4500, 'Bank Transfer', 1, 2),
(5200, 'Cash', 0, 3),            (4800, 'Credit Card', 1, 4),
(5100, 'Bank Transfer', 0, 5),   (4700, 'Cash', 1, 6),
(5500, 'Credit Card', 1, 7),     (4300, 'Bank Transfer', 1, 8),
(4900, 'Cash', 0, 9),            (5200, 'Credit Card', 1, 10),
(5000, 'Bank Transfer', 1, 11),  (4500, 'Cash', 1, 12),
(5300, 'Credit Card', 0, 13),    (4700, 'Bank Transfer', 1, 14),
(5100, 'Cash', 1, 15),           (4800, 'Credit Card', 0, 16),
(5200, 'Bank Transfer', 1, 17),  (4500, 'Cash', 1, 18),
(5000, 'Credit Card', 1, 19),    (4900, 'Bank Transfer', 0, 20),
(5200, 'Cash', 1, 21),           (4600, 'Credit Card', 1, 22),
(5400, 'Bank Transfer', 1, 23),  (4700, 'Cash', 1, 24),
(5000, 'Credit Card', 1, 25),    (4500, 'Bank Transfer', 0, 26),
(5300, 'Cash', 1, 27),           (4800, 'Credit Card', 1, 28),
(5100, 'Bank Transfer', 1, 29),  (5200, 'Cash', 1, 30),
(5000, 'Credit Card', 0, 31),    (4900, 'Bank Transfer', 1, 32),
(4800, 'Cash', 1, 33),           (5100, 'Credit Card', 1, 34),
(4500, 'Bank Transfer', 0, 35),  (5300, 'Cash', 1, 36),
(4700, 'Credit Card', 1, 37),    (5200, 'Bank Transfer', 1, 38),
(4800, 'Cash', 1, 39),           (5000, 'Credit Card', 1, 40),
(4600, 'Bank Transfer', 0, 41),  (5400, 'Cash', 1, 42),
(4700, 'Credit Card', 1, 43),    (5100, 'Bank Transfer', 1, 44),
(4800, 'Cash', 1, 45),           (5300, 'Credit Card', 1, 46),
(5000, 'Bank Transfer', 0, 47),  (5200, 'Cash', 1, 48),
(4900, 'Credit Card', 1, 49),    (4700, 'Bank Transfer', 1, 50);


INSERT INTO enrolls (Student_ID, course_ID, pre_requisite) VALUES
(1, 3, 1),   (2, 5, 0),   (3, 7, 1),   (4, 9, 0),   (5, 11, 1),
(6, 13, 0),  (7, 15, 1),  (8, 17, 0),  (9, 19, 1),  (10, 21, 0),
(11, 23, 1), (12, 2, 0),  (13, 4, 1),  (14, 6, 0),  (15, 8, 1),
(16, 10, 0), (17, 12, 1), (18, 14, 0), (19, 16, 1), (20, 18, 0),
(21, 20, 1), (22, 22, 0), (23, 24, 1), (24, 1, 0),  (25, 3, 1),
(26, 5, 0),  (27, 7, 1),  (28, 9, 0),  (29, 11, 1), (30, 13, 0),
(31, 15, 1), (32, 17, 0), (33, 19, 1), (34, 21, 0), (35, 23, 1),
(36, 2, 0),  (37, 4, 1),  (38, 6, 0),  (39, 8, 1),  (40, 10, 0),
(41, 12, 1), (42, 14, 0), (43, 16, 1), (44, 18, 0), (45, 20, 1),
(46, 22, 0), (47, 24, 1), (48, 1, 0),  (49, 3, 1),  (50, 5, 0);



INSERT INTO pre_requisites (course_ID, pre_requisite_id) VALUES
(1, 2), (1, 3), (2, 4), (3, 5), (4, 6),
(5, 7), (6, 8), (7, 9), (8, 10), (9, 11),
(10, 12), (11, 13), (12, 14), (13, 15), (14, 16),
(15, 17), (16, 18), (17, 19), (18, 20), (19, 21),
(20, 22), (21, 23), (22, 24), (23, 25), (24, 26),
(25, 27), (26, 28), (27, 29), (28, 30), (29, 31),
(30, 32), (31, 33), (32, 34), (33, 35), (34, 36),
(35, 37), (36, 38), (37, 39), (38, 40), (39, 41),
(40, 42), (41, 43), (42, 44), (43, 45), (44, 46),
(45, 47), (46, 48), (47, 49), (48, 50);


INSERT INTO lecturers (national_ID, name, salary, department_id) VALUES
(1000001, 'Dr. John Doe', 55000.00, 1), (1000002, 'Dr. Jane Smith', 60000.00, 2),
(1000003, 'Dr. Robert Brown', 65000.00, 3), (1000004, 'Dr. Emily White', 62000.00, 4),
(1000005, 'Dr. Michael Green', 58000.00, 5), (1000006, 'Dr. Sarah Black', 61000.00, 1),
(1000007, 'Dr. David Clark', 57000.00, 2), (1000008, 'Dr. Laura Lee', 59000.00, 3),
(1000009, 'Dr. Daniel Walker', 64000.00, 4), (1000010, 'Dr. Olivia Hall', 66000.00, 5),
(1000011, 'Dr. William Adams', 54000.00, 1), (1000012, 'Dr. Alice Nelson', 62500.00, 2),
(1000013, 'Dr. Henry Carter', 63000.00, 3), (1000014, 'Dr. Nancy Mitchell', 65000.00, 4),
(1000015, 'Dr. Joseph Taylor', 61000.00, 5), (1000016, 'Dr. Kimberly Perez', 60000.00, 1),
(1000017, 'Dr. Thomas Harris', 58000.00, 2), (1000018, 'Dr. Jessica Lewis', 59000.00, 3),
(1000019, 'Dr. Richard Walker', 62000.00, 4), (1000020, 'Dr. Karen Scott', 64000.00, 5),
(1000021, 'Dr. Daniel Lewis', 66000.00, 1), (1000022, 'Dr. Cheryl Young', 57000.00, 2),
(1000023, 'Dr. Elizabeth Hall', 55000.00, 3), (1000024, 'Dr. Steven Allen', 59000.00, 4),
(1000025, 'Dr. Joshua King', 60000.00, 5), (1000026, 'Dr. Megan Wright', 63000.00, 1),
(1000027, 'Dr. Brian Adams', 62000.00, 2), (1000028, 'Dr. Michelle Carter', 61000.00, 3),
(1000029, 'Dr. Paul Walker', 65000.00, 4), (1000030, 'Dr. Grace Turner', 67000.00, 5),
(1000031, 'Dr. Steven Miller', 64000.00, 1), (1000032, 'Dr. Lisa Evans', 58000.00, 2),
(1000033, 'Dr. Rachel Nelson', 59000.00, 3), (1000034, 'Dr. Benjamin Clark', 61000.00, 4),
(1000035, 'Dr. Hannah Thomas', 62000.00, 5), (1000036, 'Dr. Michael Robinson', 65000.00, 1),
(1000037, 'Dr. Emily Martinez', 64000.00, 2), (1000038, 'Dr. Anthony Lewis', 57000.00, 3),
(1000039, 'Dr. Julia Carter', 60000.00, 4), (1000040, 'Dr. William Harris', 62000.00, 5),
(1000041, 'Dr. Olivia Wilson', 65000.00, 1), (1000042, 'Dr. John Moore', 63000.00, 2),
(1000043, 'Dr. Barbara Young', 59000.00, 3), (1000044, 'Dr. David Thomas', 55000.00, 4),
(1000045, 'Dr. Patrick Smith', 57000.00, 5), (1000046, 'Dr. Laura Robinson', 65000.00, 1),
(1000047, 'Dr. Amanda Taylor', 62000.00, 2), (1000048, 'Dr. Thomas Brown', 60000.00, 3),
(1000049, 'Dr. Stephanie Scott', 59000.00, 4), (1000050, 'Dr. Matthew Harris', 58000.00, 5);


INSERT INTO teaching_assistants (name, salary) VALUES
('John Doe', 30000.00), ('Jane Smith', 32000.00), ('Robert Brown', 31000.00), ('Emily White', 33000.00), ('Michael Green', 32500.00),
('Sarah Black', 34000.00), ('David Clark', 31500.00), ('Laura Lee', 33500.00), ('Daniel Walker', 35000.00), ('Olivia Hall', 34500.00),
('William Adams', 30500.00), ('Alice Nelson', 33000.00), ('Henry Carter', 32500.00), ('Nancy Mitchell', 34000.00), ('Joseph Taylor', 31500.00),
('Kimberly Perez', 32000.00), ('Thomas Harris', 31000.00), ('Jessica Lewis', 30500.00), ('Richard Walker', 35000.00), ('Karen Scott', 34500.00),
('Daniel Lewis', 32500.00), ('Cheryl Young', 31500.00), ('Elizabeth Hall', 31000.00), ('Steven Allen', 33000.00), ('Joshua King', 33500.00),
('Megan Wright', 32000.00), ('Brian Adams', 34000.00), ('Michelle Carter', 35000.00), ('Paul Walker', 34500.00), ('Grace Turner', 32500.00),
('Steven Miller', 33000.00), ('Lisa Evans', 31500.00), ('Rachel Nelson', 31000.00), ('Benjamin Clark', 32000.00), ('Hannah Thomas', 33500.00),
('Michael Robinson', 32500.00), ('Emily Martinez', 34000.00), ('Anthony Lewis', 31500.00), ('Julia Carter', 33000.00), ('William Harris', 32000.00),
('Olivia Wilson', 35000.00), ('John Moore', 32500.00), ('Barbara Young', 31000.00), ('David Thomas', 33000.00), ('Patrick Smith', 31500.00),
('Laura Robinson', 34000.00), ('Amanda Taylor', 33000.00), ('Thomas Brown', 32000.00), ('Stephanie Scott', 31000.00), ('Matthew Harris', 32500.00);


INSERT INTO sections (course_ID, dr_ID, assistant_ID, date, room) VALUES
(1, 1, 1, '2024-12-23 09:00:00', 101), (2, 2, 2, '2024-12-23 10:00:00', 102), (3, 3, 3, '2024-12-23 11:00:00', 103),
(4, 4, 4, '2024-12-23 12:00:00', 104), (5, 5, 5, '2024-12-23 13:00:00', 105), (6, 6, 6, '2024-12-23 14:00:00', 106),
(7, 7, 7, '2024-12-23 15:00:00', 107), (8, 8, 8, '2024-12-23 16:00:00', 108), (9, 9, 9, '2024-12-23 17:00:00', 109),
(10, 10, 10, '2024-12-23 18:00:00', 110), (11, 11, 11, '2024-12-24 09:00:00', 111), (12, 12, 12, '2024-12-24 10:00:00', 112),
(13, 13, 13, '2024-12-24 11:00:00', 113), (14, 14, 14, '2024-12-24 12:00:00', 114), (15, 15, 15, '2024-12-24 13:00:00', 115),
(16, 16, 16, '2024-12-24 14:00:00', 116), (17, 17, 17, '2024-12-24 15:00:00', 117), (18, 18, 18, '2024-12-24 16:00:00', 118),
(19, 19, 19, '2024-12-24 17:00:00', 119), (20, 20, 20, '2024-12-24 18:00:00', 120), (21, 21, 21, '2024-12-25 09:00:00', 121),
(22, 22, 22, '2024-12-25 10:00:00', 122), (23, 23, 23, '2024-12-25 11:00:00', 123), (24, 24, 24, '2024-12-25 12:00:00', 124),
(25, 25, 25, '2024-12-25 13:00:00', 125), (26, 26, 26, '2024-12-25 14:00:00', 126), (27, 27, 27, '2024-12-25 15:00:00', 127),
(28, 28, 28, '2024-12-25 16:00:00', 128), (29, 29, 29, '2024-12-25 17:00:00', 129), (30, 30, 30, '2024-12-25 18:00:00', 130),
(31, 31, 31, '2024-12-26 09:00:00', 131), (32, 32, 32, '2024-12-26 10:00:00', 132), (33, 33, 33, '2024-12-26 11:00:00', 133),
(34, 34, 34, '2024-12-26 12:00:00', 134), (35, 35, 35, '2024-12-26 13:00:00', 135), (36, 36, 36, '2024-12-26 14:00:00', 136),
(37, 37, 37, '2024-12-26 15:00:00', 137), (38, 38, 38, '2024-12-26 16:00:00', 138), (39, 39, 39, '2024-12-26 17:00:00', 139),
(40, 40, 40, '2024-12-26 18:00:00', 140), (41, 41, 41, '2024-12-27 09:00:00', 141), (42, 42, 42, '2024-12-27 10:00:00', 142),
(43, 43, 43, '2024-12-27 11:00:00', 143), (44, 44, 44, '2024-12-27 12:00:00', 144), (45, 45, 45, '2024-12-27 13:00:00', 145),
(46, 46, 46, '2024-12-27 14:00:00', 146), (47, 47, 47, '2024-12-27 15:00:00', 147), (48, 48, 48, '2024-12-27 16:00:00', 148),
(49, 49, 49, '2024-12-27 17:00:00', 149), (50, 50, 50, '2024-12-27 18:00:00', 150);


INSERT INTO classrooms (date, capacity, building) VALUES
('2024-12-23 09:00:00', 30, 1), ('2024-12-23 10:00:00', 25, 2), ('2024-12-23 11:00:00', 40, 3),
('2024-12-23 12:00:00', 35, 4), ('2024-12-23 13:00:00', 50, 5), ('2024-12-23 14:00:00', 45, 6),
('2024-12-23 15:00:00', 30, 7), ('2024-12-23 16:00:00', 20, 8), ('2024-12-23 17:00:00', 60, 9),
('2024-12-23 18:00:00', 35, 10), ('2024-12-24 09:00:00', 40, 11), ('2024-12-24 10:00:00', 45, 12),
('2024-12-24 11:00:00', 50, 13), ('2024-12-24 12:00:00', 25, 14), ('2024-12-24 13:00:00', 60, 15),
('2024-12-24 14:00:00', 55, 16), ('2024-12-24 15:00:00', 35, 17), ('2024-12-24 16:00:00', 30, 18),
('2024-12-24 17:00:00', 40, 19), ('2024-12-24 18:00:00', 45, 20), ('2024-12-25 09:00:00', 50, 21),
('2024-12-25 10:00:00', 60, 22), ('2024-12-25 11:00:00', 40, 23), ('2024-12-25 12:00:00', 30, 24),
('2024-12-25 13:00:00', 55, 25), ('2024-12-25 14:00:00', 50, 26), ('2024-12-25 15:00:00', 35, 27),
('2024-12-25 16:00:00', 25, 28), ('2024-12-25 17:00:00', 60, 29), ('2024-12-25 18:00:00', 45, 30),
('2024-12-26 09:00:00', 50, 31), ('2024-12-26 10:00:00', 40, 32), ('2024-12-26 11:00:00', 30, 33),
('2024-12-26 12:00:00', 55, 34), ('2024-12-26 13:00:00', 60, 35), ('2024-12-26 14:00:00', 50, 36),
('2024-12-26 15:00:00', 45, 37), ('2024-12-26 16:00:00', 40, 38), ('2024-12-26 17:00:00', 25, 39),
('2024-12-26 18:00:00', 30, 40), ('2024-12-27 09:00:00', 35, 41), ('2024-12-27 10:00:00', 40, 42),
('2024-12-27 11:00:00', 50, 43), ('2024-12-27 12:00:00', 45, 44), ('2024-12-27 13:00:00', 30, 45),
('2024-12-27 14:00:00', 60, 46), ('2024-12-27 15:00:00', 55, 47), ('2024-12-27 16:00:00', 40, 48),
('2024-12-27 17:00:00', 25, 49), ('2024-12-27 18:00:00', 35, 50);