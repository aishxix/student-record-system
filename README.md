
# Student Record Management System

A beginner-friendly, full-stack CRUD application built for a DBMS mini-project using Python, Flask, MySQL, and Bootstrap.

## Prerequisites
- Python 3.x installed
- MySQL Server installed (XAMPP, WAMP, or standalone MySQL)
- pip (Python package installer)

## Step-by-Step Setup Guide

### 1. Set Up the Database
1. Open your MySQL command line or a GUI tool like phpMyAdmin/MySQL Workbench.
2. Copy the contents of `database.sql` and execute it. This will create the `student_db` database, the `students` table, and insert dummy data.

### 2. Configure the Backend
1. Open `app.py` in your text editor.
2. Check the `db_config` dictionary at the top of the file:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': '', # Add your MySQL password if you have one
       'database': 'student_db'
   }