CREATE TABLE Employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(100), 
    position_id int, 
    hours_worked INT DEFAULT 0, 
    days_taken_off INT DEFAULT 0, 
    days_in_office INT DEFAULT 0, 
    FOREIGN KEY (position_id) REFERENCES Position(id)
);

CREATE TABLE Position(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(100),
    base_salary INT,
    expected_hours_per_week INT,
    expected_days_in_office INT, 
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES Employee(id)
);

CREATE TABLE Rating(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INT,
    reviewer_id INT,
    rating DOUBLE,
    date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    FOREIGN KEY (reviewer_id) REFERENCES Employee(id)
)