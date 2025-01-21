import sqlite3

class SalaryManagementSystem:
    def __init__(self, db_path = 'database.db'):
        self.db_path = db_path
        self.setup_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def setup_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        #Reset tables
        cursor.execute('''DROP TABLE IF EXISTS Employee''')
        cursor.execute('''DROP TABLE IF EXISTS Position''')
        cursor.execute('''DROP TABLE IF EXISTS Rating''')
        
        #Create tables from SQL file
        with open('database.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)
        
        #Seed initial data
        self.seed(cursor)
        
        conn.commit()
        conn.close()
    
    def seed(self, cursor):
        #Positions
        positions = [
            ('Manager', 100, 40, 20, None),
            ('Software Engineer', 48, 40, 20, 1),
            ('Software Engineer Intern', 25, 40, 20, 2)
        ]
        cursor.executemany(
            "INSERT INTO Position (name, base_salary, expected_hours_per_week, expected_days_in_office, manager_id) VALUES (?, ?, ?, ?, ?)",
            positions
        )
        
        #Employees
        employees = [
            ('Andrew Adams', 1, 160, 14, 20),
            ('Brandon Bob', 2, 140, 14, 20),
            ('Chris Copa', 2, 140, 14, 20),
            ('Dylan Daniels', 3, 100, 1, 20),
            ('Elle Emmy', 3, 100, 0, 20)
        ]
        cursor.executemany(
            "INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) VALUES (?, ?, ?, ?, ?)",
            employees
        )
        
        #Ratings
        ratings = [
            (1, 0, 95.0, '2025-01-01'),
            (2, 0, 95.0, '2025-01-01'),
            (3, 0, 81.0, '2025-01-01'),
            (0, 1, 90.0, '2025-01-01'),
            (0, 2, 91.0, '2025-01-01'),
            (3, 1, 79.0, '2025-01-01')
        ]
        cursor.executemany(
            "INSERT INTO Rating (employee_id, reviewer_id, rating, date) VALUES (?, ?, ?, ?)",
            ratings
        )

    # CRUD Operations
    def create_employee(self, name, position_id, hours_worked, days_taken_off, days_in_office):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Employee (name, position_id, hours_worked, days_taken_off, days_in_office) 
               VALUES (?, ?, ?, ?, ?)""",
            (name, position_id, hours_worked, days_taken_off, days_in_office)
        )
        employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return employee_id

    def get_employee(self, employee_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.*, p.name as position_name, p.base_salary 
            FROM Employee e
            JOIN Position p ON e.position_id = p.id
            WHERE e.id = ?
        """, (employee_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'position_id': result[2],
                'hours_worked': result[3],
                'days_taken_off': result[4],
                'days_in_office': result[5],
                'position_name': result[6],
                'base_salary': result[7]
            }
        return None

    def update_employee(self, employee_id, update_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clause = []
        for k in update_data.keys():
            set_clause.append(f"{k} = ?")
        set_clause = ', '.join(set_clause)
        values = list(update_data.values()) + [employee_id]
        cursor.execute(
            f"UPDATE Employee SET {set_clause} WHERE id = ?",
            values
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def delete_employee(self, employee_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employee WHERE id = ?", (employee_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    #Efficieny Report by position
    def get_department_efficiency_report(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                Position.name AS position_name,
                COUNT(Employee.id) AS employee_count,
                AVG(Rating.rating) AS average_rating,
                SUM(Employee.hours_worked) AS total_hours_worked,
                (SUM(Employee.hours_worked) * 100.0 / 
                 (COUNT(Employee.id) * Position.expected_hours_per_week)) AS staffing_efficiency
            FROM Employee
            JOIN Position ON Employee.position_id = Position.id
            LEFT JOIN Rating ON Employee.id = Rating.employee_id
            GROUP BY Position.id, Position.name, Position.expected_hours_per_week
            ORDER BY staffing_efficiency DESC
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'position_name': row[0],
            'employee_count': row[1],
            'average_rating': row[2],
            'total_hours_worked': row[3],
            'staffing_efficiency': row[4]
        } for row in results]


if __name__ == "__main__":
    company = SalaryManagementSystem()
    
    new_employee = company.create_employee('Frank Fisher', 2, 120, 5, 15)
    print(f"Created new employee with ID: {new_employee}")
    
    employee = company.get_employee(new_employee)
    print(f"Employee details: {employee}")

    update_data = {
        'hours_worked': 170,
        'days_taken_off': 5
    }
    update_success = company.update_employee(1, update_data)
    print(update_success)

    delete_success = company.delete_employee(2)
    print(delete_success)
    
    report = company.get_department_efficiency_report()
    print("\nDepartment Efficiency Report:")
    for entry in report:
        print(f"Position: {entry['position_name']}")
        print(f"Efficiency: {entry['staffing_efficiency']}")
        print(f"Average Rating: {entry['average_rating']}" if entry['average_rating'] is not None else "Average Rating: N/A")
        print("----------------------------")