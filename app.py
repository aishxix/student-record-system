# import os
# from flask import Flask, render_template, request, redirect, url_for
# import pyodbc
# from dotenv import load_dotenv

# # Load environment configurations
# load_dotenv()

# app = Flask(__name__)

# # Fetch the database details from the .env file
# db_driver = os.getenv('DB_DRIVER')
# db_server = os.getenv('DB_SERVER')
# db_database = os.getenv('DB_DATABASE')

# connection_string = (
#     f'DRIVER={{{db_driver}}};'
#     f'SERVER={db_server};'
#     f'DATABASE={db_database};'
#     f'Trusted_Connection=yes;'
# )

# def get_db_connection():
#     return pyodbc.connect(connection_string)

# # Helper function for SQL Server dictionaries
# def row_to_dict(cursor, row):
#     if not row:
#         return None
#     columns = [column[0] for column in cursor.description]
#     return dict(zip(columns, row))

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # Advanced query to calculate total courses and credits per student
#     query = """
#         SELECT 
#             s.id, 
#             s.name, 
#             s.roll_no, 
#             s.department, 
#             s.semester,
#             COUNT(e.course_id) AS total_courses,
#             COALESCE(SUM(c.credit_hours), 0) AS total_credits
#         FROM students s
#         LEFT JOIN enrollments e ON s.id = e.student_id
#         LEFT JOIN courses c ON e.course_id = c.course_id
#         GROUP BY 
#             s.id, 
#             s.name, 
#             s.roll_no, 
#             s.department, 
#             s.semester
#     """
    
#     cursor.execute(query)
#     # The row_to_dict function automatically attaches our new 'total_courses' 
#     # and 'total_credits' labels to the data so HTML can read it!
#     students = [row_to_dict(cursor, row) for row in cursor.fetchall()]
    
#     cursor.close()
#     conn.close()
#     return render_template('index.html', students=students)

# @app.route('/add', methods=['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         name = request.form['name']
#         roll_no = request.form['roll_no']
#         department = request.form['department']
#         semester = request.form['semester']

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO students (name, roll_no, department, semester) VALUES (?, ?, ?, ?)",
#             (name, roll_no, department, semester)
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return redirect(url_for('index'))
    
#     return render_template('add.html')

# @app.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit(id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     if request.method == 'POST':
#         name = request.form['name']
#         roll_no = request.form['roll_no']
#         department = request.form['department']
#         semester = request.form['semester']

#         cursor.execute(
#             "UPDATE students SET name=?, roll_no=?, department=?, semester=? WHERE id=?",
#             (name, roll_no, department, semester, id)
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return redirect(url_for('index'))

#     cursor.execute("SELECT * FROM students WHERE id=?", (id,))
#     student = row_to_dict(cursor, cursor.fetchone())
#     cursor.close()
#     conn.close()
#     return render_template('edit.html', student=student)

# @app.route('/delete/<int:id>')
# def delete(id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM students WHERE id=?", (id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return redirect(url_for('index'))

# # --- Course Registration Many-to-Many Routing Engine ---

# @app.route('/schedule/<int:id>')
# def schedule(id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # 1. Obtain student details
#     cursor.execute("SELECT * FROM students WHERE id=?", (id,))
#     student = row_to_dict(cursor, cursor.fetchone())

#     # 2. INNER JOIN query to pull courses mapped through the junction table
#     join_query = """
#         SELECT c.course_id, c.course_name, c.credit_hours, e.enrollment_id
#         FROM courses c
#         INNER JOIN enrollments e ON c.course_id = e.course_id
#         WHERE e.student_id = ?
#     """
#     cursor.execute(join_query, (id,))
#     enrolled_courses = [row_to_dict(cursor, row) for row in cursor.fetchall()]

#     # 3. Subquery looking for classes that this student hasn't signed up for yet
#     available_query = """
#         SELECT * FROM courses
#         WHERE course_id NOT IN (
#             SELECT course_id FROM enrollments WHERE student_id = ?
#         )
#     """
#     cursor.execute(available_query, (id,))
#     available_courses = [row_to_dict(cursor, row) for row in cursor.fetchall()]

#     cursor.close()
#     conn.close()
#     return render_template('schedule.html', student=student, enrolled_courses=enrolled_courses, available_courses=available_courses)

# @app.route('/enroll/<int:student_id>', methods=['POST'])
# def enroll(student_id):
#     course_id = request.form.get('course_id')
#     if course_id:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
#             (student_id, course_id)
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()
#     return redirect(url_for('schedule', id=student_id))

# @app.route('/drop/<int:student_id>/<int:enrollment_id>')
# def drop_course(student_id, enrollment_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM enrollments WHERE enrollment_id=?", (enrollment_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return redirect(url_for('schedule', id=student_id))
# # --- Fee Voucher & Billing Engine ---

# @app.route('/voucher/<int:student_id>')
# def voucher(student_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # 1. Fetch Student Details
#     cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
#     student = row_to_dict(cursor, cursor.fetchone())

#     # 2. Check if a voucher already exists
#     cursor.execute("SELECT * FROM fee_vouchers WHERE student_id=?", (student_id,))
#     existing_voucher = row_to_dict(cursor, cursor.fetchone())

#     if not existing_voucher:
#         # 3. Calculate total credits using Relational Algebra (Aggregate SUM)
#         credit_query = """
#             SELECT COALESCE(SUM(c.credit_hours), 0) AS total_credits
#             FROM enrollments e
#             INNER JOIN courses c ON e.course_id = c.course_id
#             WHERE e.student_id = ?
#         """
#         cursor.execute(credit_query, (student_id,))
#         credit_result = row_to_dict(cursor, cursor.fetchone())
#         total_credits = credit_result['total_credits'] if credit_result else 0

#         # Financial Math (Adjust these rates as needed for SSUET!)
#         per_credit_rate = 4500  # 4,500 PKR per credit hour
#         fixed_charges = 8500    # Lab, Library, and Sports fees
        
#         tuition_fee = total_credits * per_credit_rate
#         total_amount = tuition_fee + fixed_charges

#         # Insert new voucher into the database
#         insert_query = """
#             INSERT INTO fee_vouchers (student_id, total_credits, tuition_fee, total_amount, status)
#             VALUES (?, ?, ?, ?, 'Unpaid')
#         """
#         cursor.execute(insert_query, (student_id, total_credits, tuition_fee, total_amount))
#         conn.commit()
        
#         # Fetch the newly created voucher
#         cursor.execute("SELECT * FROM fee_vouchers WHERE student_id=?", (student_id,))
#         existing_voucher = row_to_dict(cursor, cursor.fetchone())

#     cursor.close()
#     conn.close()

#     # Pass the fixed charges to the template so they show on the invoice
#     fixed_charges = 8500 
#     return render_template('voucher.html', student=student, voucher=existing_voucher, fixed_charges=fixed_charges)

# @app.route('/pay_voucher/<int:voucher_id>/<int:student_id>')
# def pay_voucher(voucher_id, student_id):
#     # Simple route to mark the invoice as Paid
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE fee_vouchers SET status = 'Paid' WHERE voucher_id = ?", (voucher_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return redirect(url_for('voucher', student_id=student_id))
# if __name__ == '__main__':
#     app.run(debug=True)



import os
from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from dotenv import load_dotenv

# Load environment configurations
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
    return pyodbc.connect(connection_string)

# Helper function for SQL Server dictionaries
def row_to_dict(cursor, row):
    if not row:
        return None
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            s.id, 
            s.name, 
            s.roll_no, 
            s.department, 
            s.semester,
            COUNT(e.course_id) AS total_courses,
            COALESCE(SUM(c.credit_hours), 0) AS total_credits
        FROM students s
        LEFT JOIN enrollments e ON s.id = e.student_id
        LEFT JOIN courses c ON e.course_id = c.course_id
        GROUP BY 
            s.id, 
            s.name, 
            s.roll_no, 
            s.department, 
            s.semester
    """
    
    cursor.execute(query)
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
    student = row_to_dict(cursor, cursor.fetchone())
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

@app.route('/schedule/<int:id>')
def schedule(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = row_to_dict(cursor, cursor.fetchone())

    join_query = """
        SELECT c.course_id, c.course_name, c.credit_hours, e.enrollment_id
        FROM courses c
        INNER JOIN enrollments e ON c.course_id = e.course_id
        WHERE e.student_id = ?
    """
    cursor.execute(join_query, (id,))
    enrolled_courses = [row_to_dict(cursor, row) for row in cursor.fetchall()]

    available_query = """
        SELECT * FROM courses
        WHERE course_id NOT IN (
            SELECT course_id FROM enrollments WHERE student_id = ?
        )
    """
    cursor.execute(available_query, (id,))
    available_courses = [row_to_dict(cursor, row) for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return render_template('schedule.html', student=student, enrolled_courses=enrolled_courses, available_courses=available_courses)

@app.route('/enroll/<int:student_id>', methods=['POST'])
def enroll(student_id):
    course_id = request.form.get('course_id')
    if course_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
            (student_id, course_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('schedule', id=student_id))

@app.route('/drop/<int:student_id>/<int:enrollment_id>')
def drop_course(student_id, enrollment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollments WHERE enrollment_id=?", (enrollment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('schedule', id=student_id))

# --- Fee Voucher & Billing Engine ---

@app.route('/voucher/<int:student_id>')
def voucher(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch Student Details
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = row_to_dict(cursor, cursor.fetchone())

    # 2. Calculate the CURRENT total credits based on their actual enrollments
    credit_query = """
        SELECT COALESCE(SUM(c.credit_hours), 0) AS total_credits
        FROM enrollments e
        INNER JOIN courses c ON e.course_id = c.course_id
        WHERE e.student_id = ?
    """
    cursor.execute(credit_query, (student_id,))
    credit_result = row_to_dict(cursor, cursor.fetchone())
    total_credits = credit_result['total_credits'] if credit_result else 0

    # Financial Math
    per_credit_rate = 4500  # 4,500 PKR per credit hour
    fixed_charges = 8500    # Lab, Library, and Sports fees
    
    tuition_fee = total_credits * per_credit_rate
    total_amount = tuition_fee + fixed_charges

    # 3. Check if they already have a voucher
    cursor.execute("SELECT * FROM fee_vouchers WHERE student_id=?", (student_id,))
    existing_voucher = row_to_dict(cursor, cursor.fetchone())

    if existing_voucher:
        # If they do, UPDATE it with the new math
        update_query = """
            UPDATE fee_vouchers 
            SET total_credits = ?, tuition_fee = ?, total_amount = ?
            WHERE student_id = ?
        """
        cursor.execute(update_query, (total_credits, tuition_fee, total_amount, student_id))
    else:
        # If they don't, INSERT a new one
        insert_query = """
            INSERT INTO fee_vouchers (student_id, total_credits, tuition_fee, total_amount, status)
            VALUES (?, ?, ?, ?, 'Unpaid')
        """
        cursor.execute(insert_query, (student_id, total_credits, tuition_fee, total_amount))
    
    conn.commit()
    
    # 4. Fetch the final, updated voucher to display on the page
    cursor.execute("SELECT * FROM fee_vouchers WHERE student_id=?", (student_id,))
    final_voucher = row_to_dict(cursor, cursor.fetchone())

    cursor.close()
    conn.close()

    return render_template('voucher.html', student=student, voucher=final_voucher, fixed_charges=fixed_charges)

@app.route('/pay_voucher/<int:voucher_id>/<int:student_id>')
def pay_voucher(voucher_id, student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE fee_vouchers SET status = 'Paid' WHERE voucher_id = ?", (voucher_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('voucher', student_id=student_id))

if __name__ == '__main__':
    app.run(debug=True)