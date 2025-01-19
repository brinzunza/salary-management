import sqlite3

#table reset and connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute(''' DROP TABLE IF EXISTS Employee''')
cursor.execute(''' DROP TABLE IF EXISTS Position''')
cursor.execute(''' DROP TABLE IF EXISTS Rating''')
conn.commit()

with open('database.sql', 'r') as sql_file:
    sql_script = sql_file.read()
cursor.executescript(sql_script)
conn.commit()

#seeding data into database

#positions
cursor.execute("INSERT INTO Position (name, base_salary, expected_hours_per_week, expected_days_in_office, manager_id) VALUES (?, ?, ?, ?, ?)", ('Manager', 100, 40, 20, None))
cursor.execute("INSERT INTO Position (name, base_salary, expected_hours_per_week, expected_days_in_office, manager_id) VALUES (?, ?, ?, ?, ?)", ('Software Engineer', 48, 40, 20, 1))
cursor.execute("INSERT INTO Position (name, base_salary, expected_hours_per_week, expected_days_in_office, manager_id) VALUES (?, ?, ?, ?, ?)", ('Software Engineer Intern', 25, 40, 20, 2))
conn.commit()

#employees
cursor.execute("INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) VALUES (?, ?, ?, ?, ?)", ('Andrew Adams', 1, 160, 14, 20))
cursor.execute("INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) VALUES (?, ?, ?, ?, ?)", ('Brandon Bob', 2, 140, 14, 20))
cursor.execute("INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) VALUES (?, ?, ?, ?, ?)", ('Chris Copa', 2, 140, 14, 20))
cursor.execute("INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) VALUES (?, ?, ?, ?, ?)", ('Dylan Daniels', 3, 100, 1, 20))
cursor.execute("INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) VALUES (?, ?, ?, ?, ?)", ('Elle Emmy', 3, 100, 0, 20))
conn.commit()

#ratings
cursor.execute("INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)", (1, 0, 95.0, '2025-01-01'))
cursor.execute("INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)", (2, 0, 95.0, '2025-01-01'))
cursor.execute("INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)", (3, 0, 81.0, '2025-01-01'))
cursor.execute("INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)", (0, 1, 90.0, '2025-01-01'))
cursor.execute("INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)", (0, 2, 91.0, '2025-01-01'))
cursor.execute("INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)", (3, 1, 79.0, '2025-01-01'))
conn.commit()

#analysis
cursor.execute("SELECT * FROM Employee")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("\n")

cursor.execute("UPDATE Position SET base_salary = ? WHERE id = ?", (90, 1))
conn.commit()

cursor.execute("SELECT * FROM Position")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("\n")

cursor.execute("DELETE FROM Employee WHERE id = ?", (1,))
conn.commit()

cursor.execute("SELECT Position.name AS PositionName, COUNT(Employee.id) AS EmployeeCount, AVG(Rating.rating) AS AverageRating, SUM(Employee.hours_worked) AS TotalHoursWorked, (SUM(Employee.hours_worked) / (COUNT(Employee.id) * Position.expected_hours_per_week)) * 100 AS StaffingEfficiency FROM Employee JOIN Position ON Employee.position_id = Position.id LEFT JOIN Rating ON Employee.id = Rating.employee_id GROUP BY Position.id, Position.name, Position.expected_hours_per_week ORDER BY StaffingEfficiency DESC;")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("\n")

conn.close()