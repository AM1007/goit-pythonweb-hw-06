from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy import func
from models import Student, Group, Teacher, Subject, Grade, init_db

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()


# Rounding results
def round_results(results):
    if isinstance(results, tuple):
        return tuple(
            round(value, 2) if isinstance(value, float) else value for value in results
        )
    elif isinstance(results, list):
        return [round_results(result) for result in results]
    return results


# 1. Find 5 students with the highest average grade across all subjects
def select_1():
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return round_results(result)


# 2. Find the student with the highest average grade in a specific subject
def select_2(subject_name):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    if result:
        return round_results([result])[0]
    return result


# 3. Find the average grade in groups for a specific subject
def select_3(subject_name):
    SubjectAlias = aliased(Subject)

    query = (
        session.query(Group.name, func.avg(Grade.grade).label("average_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(SubjectAlias, SubjectAlias.id == Grade.subject_id)
        .filter(SubjectAlias.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    return round_results(query)


# 4. Find the average grade across the entire grade table
def select_4():
    result = session.query(func.avg(Grade.grade).label("average_grade")).scalar()
    if result is not None:
        return round(result, 2)
    return result


# 5. Find the courses taught by a specific teacher
def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result


# 6. Find the list of students in a specific group
def select_6(group_name):
    result = (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )
    return result


# 7. Find the grades of students in a specific group for a specific subject
def select_7(group_name, subject_name):
    result = (
        session.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


# 8. Find the average grade given by a specific teacher for their subjects
def select_8(teacher_name):
    result = (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round(result, 2) if result is not None else result


# 9. Find the list of courses attended by a specific student
def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .all()
    )
    return result


# 10. List of courses taught to a specific student by a specific teacher
def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .all()
    )
    return result


# Function to print query results
def print_query_result(query_result, title):
    print(title)
    if query_result:
        for row in query_result:
            print(row)
    else:
        print("No results found.")
    print("\n" + "-" * 50)


if __name__ == "__main__":
    # Example usage of functions with rounding
    print_query_result(select_1(), "Top 5 Students by Average Grade")

    student_2 = select_2("Mathematics")
    if student_2:
        print_query_result([student_2], "Student with Highest Average in Mathematics")
    else:
        print("No student found with the highest average in Mathematics.")

    select_3_result = select_3("Service")
    if select_3_result:
        print_query_result(select_3_result, "Average Grade by Groups in Service")
    else:
        print("No groups found for the subject 'Service'.")

    overall_avg = select_4()
    if overall_avg is not None:
        print(f"Overall Average Grade: {overall_avg}")
    else:
        print("No average grade found.")

    select_5_result = select_5("Karen Bush")
    if select_5_result:
        print_query_result(select_5_result, "Courses Taught by Karen Bush")
    else:
        print("No courses found taught by Karen Bush.")

    select_6_result = select_6("Group 1")
    if select_6_result:
        print_query_result(select_6_result, "Students in Group 1")
    else:
        print("No students found in Group 1.")

    select_7_result = select_7("Group 1", "Service")
    if select_7_result:
        print_query_result(select_7_result, "Grades in Group 1 for Service")
    else:
        print("No grades found in Group 1 for the 'Service' subject.")

    avg_8 = select_8("Karen Bush")
    if avg_8 is not None:
        print(f"Karen Bush Average Grade: {avg_8}")
    else:
        print("No average grade found for Karen Bush.")

    select_9_result = select_9("Miguel Wilson")
    if select_9_result:
        print_query_result(select_9_result, "Courses Attended by Miguel Wilson")
    else:
        print("No courses found for Miguel Wilson.")

    select_10_result = select_10("Miguel Wilson", "Karen Bush")
    if select_10_result:
        print_query_result(
            select_10_result, "Courses Taught by Karen Bush to Miguel Wilson"
        )
    else:
        print("No courses found for Miguel Wilson taught by Karen Bush.")