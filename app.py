from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Fetch the database details from the .env file
db_driver = os.getenv('DB_DRIVER')
db_server = os.getenv('DB_SERVER')
db_database = os.getenv('DB_DATABASE')

connection_string = (
    f'DRIVER={{{db_driver}}};'
    f'SERVER={db_server};'
    f'DATABASE={db_database};'
    f'Trusted_Connection=yes;'
)

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

# ... (Keep the rest of your app.py code exactly the same below this) ...

# Helper function to convert pyodbc rows to dictionaries so our HTML templates still work
def row_to_dict(cursor, row):
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    
    # Convert results to a list of dictionaries
    students = [row_to_dict(cursor, row) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        semester = request.form['semester']

        conn = get_db_connection()
        cursor = conn.cursor()
        # Note: pyodbc uses ? instead of %s for parameters
        cursor.execute(
            "INSERT INTO students (name, roll_no, department, semester) VALUES (?, ?, ?, ?)",
            (name, roll_no, department, semester)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        semester = request.form['semester']

        cursor.execute(
            "UPDATE students SET name=?, roll_no=?, department=?, semester=? WHERE id=?",
            (name, roll_no, department, semester, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    row = cursor.fetchone()
    student = row_to_dict(cursor, row) if row else None
    
    cursor.close()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)