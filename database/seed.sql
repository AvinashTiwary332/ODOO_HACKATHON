USE hrms_db;

INSERT INTO users (name, email, password_hash, role) VALUES
('Aarav Admin', 'admin@hrms.test', 'pbkdf2:sha256:1000000$demo$replace-with-flask-hash', 'Admin'),
('Hira HR', 'hr@hrms.test', 'pbkdf2:sha256:1000000$demo$replace-with-flask-hash', 'HR Officer'),
('Esha Patel', 'employee@hrms.test', 'pbkdf2:sha256:1000000$demo$replace-with-flask-hash', 'Employee');

INSERT INTO employees (user_id, employee_id, department, designation, joining_date, phone, address, salary) VALUES
(1, 'EMP-1000', 'Leadership', 'System Admin', '2022-01-05', '9000000001', 'Ahmedabad', 120000),
(2, 'EMP-1001', 'People Ops', 'HR Officer', '2022-06-12', '9000000002', 'Mumbai', 85000),
(3, 'EMP-1002', 'Engineering', 'Frontend Engineer', '2023-03-20', '9000000003', 'Bengaluru', 72000);
