from random import randint
from datetime import datetime

from faker import Faker

from models import Student, Group, Teacher, Grade, Subject
from connect_db import session


STUDENTS = ['David Ross', 'Susan Bradshaw', 'Cynthia Shaw', 'Kathryn Waller', 'Jonathan Serrano',
                     'Kathleen Brown', 'Ann Richardson', 'Samuel Gutierrez', 'Matthew White', 'Austin Harris',
                     'Joshua Payne', 'Danielle Craig', 'Cory Martinez', 'Michael Bradley', 'Christina Jackson',
                     'Heather Lamb', 'Gina Rivera', 'Michael Bray', 'Misty Church', 'Michael Ross', 'Gabriel Bryant',
                     'Scott Weaver', 'Johnny Howe', 'Henry Dodson', 'James Carter', 'Gene Johnson', 'Brandon Morrison',
                     'Sandy Smith', 'Joshua Gibson', 'Jeanne Pacheco', 'Catherine Charles', 'Kim Cummings',
                     'Kenneth Armstrong', 'Joseph Matthews', 'Angela Jordan', 'Marissa Brooks', 'William Haynes',
                     'Troy Smith', 'Sean Hamilton', 'Scott Jennings', 'David Brown', 'Abigail Leblanc',
                     'Christine Perez', 'Kelly Johnston', 'Robert Smith']

NUMBER_GROUPS = [101, 102, 103]

TEACHERS = ["Gabrielle Curtis", "Brandy Bradford", "Jessica Jones", "Lucas Fletcher"]

NUMBER_GRADES = 20

SUBJECTS = ["Introduction to Computer Science", "Principles of Economics", "Introduction to Psychology",
            "World History Since", "Introduction to Sociology", "Mathematics", "Biology", "Physics"]


def filling_db(students, groups=None, teachers=None, subjects=None):

    fake_data = Faker()

    group_students = []
    interim_students = students
    for number in groups:
        group = Group(
            group_number=number,
            students = [
                Student(
                    student_name=name
                )
                for name in interim_students[:15]
            ]
        )

        group_students.extend([(number, student) for student in interim_students[:15]])
        interim_students = interim_students[15:]
        session.add(group)

    interim_subjects = subjects
    for name in teachers:
        teacher = Teacher(
            teacher_name=name,
            teacher_subjects=[
                Subject(
                    subject_name=subject
                )
                for subject in interim_subjects[:2]
            ]
        )
        interim_subjects = interim_subjects[2:]
        session.add(teacher)

    for _ in range(3):
        for sub in range(1, len(subjects) + 1):
            for number in groups:
                random_date = fake_data.date_between(start_date=datetime(2024, 1, 1))
                for i, student in enumerate(group_students, 1):
                    group, _ = student
                    if number == group:
                        grade = Grade(student_id=i, subject_id=sub,
                            grade=randint(1, 12), date_of=random_date)

                        session.add(grade)

    session.commit()


if __name__ == '__main__':

    filling_db(STUDENTS, NUMBER_GROUPS, TEACHERS, SUBJECTS)
