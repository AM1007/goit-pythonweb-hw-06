import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade
from pprint import pprint

# Initialize Faker
fake = Faker()

# Database connection settings
DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Number of records to generate
NUM_GROUPS = 3
NUM_TEACHERS = 5
NUM_SUBJECTS = 8
NUM_STUDENTS = 50
MAX_GRADES_PER_STUDENT = 20


def seed_data():
    try:
        # Clear existing data (first grades, then students to avoid foreign key errors)
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()

        # Create groups
        groups = []
        for i in range(NUM_GROUPS):
            group_name = f"Group {i+1}"
            groups.append(Group(name=group_name))

        session.add_all(groups)
        session.commit()

        # Log successful addition of groups
        print(f"Groups: {', '.join([group.name for group in groups])} successfully added!")

        # Create teachers
        teachers = [Teacher(name=fake.name()) for _ in range(NUM_TEACHERS)]
        session.add_all(teachers)
        session.commit()

        # Log successful addition of teachers
        print(f"Teachers: {', '.join([teacher.name for teacher in teachers])} successfully added!")

        # Create subjects
        subjects = [
            Subject(name=fake.word().capitalize(), teacher=random.choice(teachers))
            for _ in range(NUM_SUBJECTS)
        ]
        session.add_all(subjects)
        session.commit()

        # Log successful addition of subjects
        print(f"Subjects: {', '.join([subject.name for subject in subjects])} successfully added!")

        # Create students
        students = [
            Student(name=fake.name(), group=random.choice(groups))
            for _ in range(NUM_STUDENTS)
        ]
        session.add_all(students)
        session.commit()

        # Log successful addition of students
        print("Students:")
        pprint([student.name for student in students])

        # Create grades
        grades = []
        for student in students:
            for _ in range(random.randint(1, MAX_GRADES_PER_STUDENT)):
                grade = Grade(
                    student=student,
                    subject=random.choice(subjects),
                    grade=random.uniform(1.0, 5.0),
                    date_received=fake.date_between(start_date="-2y", end_date="today"),
                )
                grades.append(grade)

        session.add_all(grades)
        session.commit()

        # Log successful addition of grades
        print("Grades for students successfully added!")

        print("Data successfully added to the database!")
    except Exception as e:
        session.rollback()
        print(f"Error while populating the database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()