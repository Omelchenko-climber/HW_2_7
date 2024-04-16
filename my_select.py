from sqlalchemy import select, func

from connect_db import session
from models import Student, Group, Grade, Subject, Teacher


def select_1():
    stmt = select(Student.student_name, func.round(func.avg(Grade.grade), 2).label("avg_grade")) \
        .join(Grade, Student.id == Grade.student_id) \
        .group_by(Student.student_name) \
        .order_by(func.round(func.avg(Grade.grade), 2).desc()) \
        .limit(5)

    results = session.execute(stmt)

    for res in results:
        name, avg_grade = res
        print(f"Student {name} has average grade {avg_grade}")


def select_2():
    stmt = select(Student.student_name, Subject.subject_name, func.round(func.avg(Grade.grade), 2)) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.id == 1) \
        .group_by(Student.student_name, Subject.subject_name) \
        .order_by(func.round(func.avg(Grade.grade), 2).desc()) \
        .limit(5)

    results = session.execute(stmt)

    for res in results:
        name, sub, grade = res
        print(f"Student: {name}, subject: {sub} has average grade {grade}.")


def select_3():
    stmt = select(Group.group_number, Subject.subject_name, func.round(func.avg(Grade.grade), 2)) \
        .join(Student, Group.id == Student.group_id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.id == 3) \
        .group_by(Group.group_number, Subject.subject_name) \
        .order_by(func.round(func.avg(Grade.grade), 2).desc())

    results = session.execute(stmt)

    for res in results:
        group, sub, grade = res
        print(f"Group: {group}, subject: {sub} has average grade {grade}.")


def select_4():
    stmt = select(func.round(func.avg(Grade.grade), 2))

    result, = session.execute(stmt).fetchone()

    print(f"Average grade: {result}")


def select_5():
    stmt = select(Subject.subject_name, Teacher.teacher_name) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Teacher.teacher_name == "Brandy Bradford") \

    results = session.execute(stmt)

    for res in results:
        print(res)


def select_6():
    stmt = select(Student.student_name) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Group.group_number == 103)

    results = session.execute(stmt)

    for res in results:
        name, = res
        print(name)


def select_7():
    stmt = select(Grade.grade, Student.student_name, Subject.subject_name) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Subject.subject_name == "Biology") \
        .filter(Group.group_number == 101) \
        .order_by(Grade.grade.desc())

    results = session.execute(stmt)

    for res in results:
        grade, name, sub = res
        print(f"Student {name} has {grade} for {sub}.")


def select_8():
    stmt = select(Teacher.teacher_name, Subject.subject_name, func.round(func.avg(Grade.grade), 2)) \
        .join(Subject, Teacher.id == Subject.teacher_id) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .filter(Teacher.teacher_name == "Brandy Bradford") \
        .group_by(Teacher.teacher_name, Subject.subject_name) \
        .order_by(func.round(func.avg(Grade.grade), 2).desc())

    results = session.execute(stmt)

    for res in results:
        name, sub, avg_grade = res
        print(f"Teacher {name}, subject {sub}, average grade {avg_grade}.")


def select_9():
    stmt = select(Subject.subject_name, Student.student_name) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .join(Student, Grade.student_id == Student.id) \
        .filter(Student.student_name == "Robert Smith")

    results = session.execute(stmt)

    for res in results:
        sub, name = res
        print(f"Student {name}:  {sub}.")


def select_10():
    stmt = select(Student.student_name, Teacher.teacher_name, Subject.subject_name).distinct() \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.student_name == "Robert Smith") \
        .filter(Teacher.teacher_name == "Brandy Bradford")

    results = session.execute(stmt)

    for res in results:
        student, teacher, sub = res
        print(f"Student {student}, teacher {teacher}, subject {sub}.")


def select_11():
    stmt = select(Student.student_name, Teacher.teacher_name, func.round(func.avg(Grade.grade), 2)) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.student_name == "Johnny Howe") \
        .filter(Teacher.teacher_name == "Jessica Jones") \
        .group_by(Student.student_name, Teacher.teacher_name)

    result = session.execute(stmt).fetchone()

    student, teacher, avg_grade = result
    print(f"Student {student}, teacher {teacher}, average grade {avg_grade}.")


def select_12():
    stmt = select(Subject.subject_name, Student.student_name, Grade.grade, Group.group_number, Grade.date_of) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Group, Student.group_id == Group.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Group.group_number == 101) \
        .filter(Subject.subject_name == "Biology") \
        .order_by(Grade.date_of.desc(), Grade.grade.desc()) \
        .limit(15)

    results = session.execute(stmt)

    for res in results:
        sub, student, grade, group, date_of = res
        print(f"Group {group}, subject {sub}, date of {date_of}, grade {grade}, student {student}.")
