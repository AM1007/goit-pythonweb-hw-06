# Advanced SQLAlchemy and Database Schema Migration Features

## Implement a database with the following schema:

- A table for students.
- A table for groups.
- A table for teachers.
- A table for subjects, including the teacher assigned to each subject.
- A table for grades, where each student has grades for subjects, along with the date each grade was received.

For this assignment, we will use a **Postgres** database. Run the `Docker` container from the command line:

```Python
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD =mysecretpassword -d postgres
```

Replace `some-postgres` with your container's custom name, and use a unique password instead of `mysecretpassword` for connecting to the database.

## Task Description

### Step 1

Implement your **SQLAlchemy** models for the following tables:

- A table for students.
- A table for groups.
- A table for teachers.
- A table for subjects, including the teacher assigned to each subject.
- A table for grades, where each student has grades for subjects, along with the date the grade was received.

### Step 2

Use `alembic` to create database migrations.

### Step 3

Write a script named seed.py to populate the database with random data:

- ~30–50 students.
- 3 groups.
- 5–8 subjects.
- 3–5 teachers.
- Up to 20 grades for each student across all subjects.

Use the **Faker** library to generate random data. Populate the database using **SQLAlchemy** sessions.

### Step 4

Perform the following queries on the populated database:

1.  Find the top 5 students with the highest average grades across all subjects.
2.  Find the student with the highest average grade in a specific subject.
3.  Calculate the average grade for groups in a specific subject.
4.  Calculate the overall average grade across the entire database.
5.  List the courses taught by a specific teacher.
6.  Retrieve the list of students in a specific group.
7.  Find the grades of students in a specific group for a specific subject.
8.  Calculate the average grade given by a specific teacher across all their subjects.
9.  List the courses a specific student is enrolled in.
10. List the courses taught to a specific student by a specific teacher.

Create a separate file named `my_select.py`, where these queries are implemented as `10` functions named `select_1` through `select_10`. Use SQLAlchemy sessions for all queries.

## Additional Task

### Part 1

Write more advanced queries:

- Calculate the average grade a specific teacher gives to a specific student.
- Retrieve the grades of students in a specific group for a specific subject during the most recent class.

### Part 2

Instead of the `seed.py` script, design and implement a **full-fledged CLI** program for **CRUD** operations with the database. Use the [argparse](https://docs.python.org/3/library/argparse.html) module for this.

Support the following options:

Use `--action` or the shorthand -a for CRUD operations.
Use `--model` (or -m) to specify the model on which the operation is performed.

For example:

```bash
-action create -m Teacher --name 'Boris Johnson' # Create a teacher
-action list -m Teacher # List all teachers
-action update -m Teacher --id 3 --name 'Andy Bezos' # Update the teacher with id=3
-action remove -m Teacher --id 3 # Remove the teacher with id=3
```

Implement these operations for all models.

Examples of commands:

```python
py main .py - create -m Teacher -n 'Boris Jonson'
```

Create a teacher.

```python
py main .py - create -m Group -n 'AD-101'
```

Create a group.
