from datetime import datetime

from sqlalchemy import String,Date, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship)


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_number: Mapped[int] = mapped_column(nullable=False)
    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"Group number: {self.group_number}"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_name: Mapped[str] = mapped_column(String(30), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)

    student_grade: Mapped["Grade"] = relationship(back_populates="grade_student", cascade="all, delete-orphan")
    group: Mapped["Group"] = relationship(back_populates="students")

    def __init__(self, name, group=1):
        self.student_name = name
        self.group_id = group

    def __repr__(self):
        return f"Student: {self.student_name}"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_name: Mapped[str] = mapped_column(String(30), nullable=False)
    teacher_subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")

    def __repr__(self):
        return f"Teacher: {self.teacher_name}, subjects: {self.teacher_subjects}"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    teacher: Mapped["Teacher"] = relationship(back_populates="teacher_subjects")
    subject_grades: Mapped[list["Grade"]] = relationship(back_populates="subject")

    def __repr__(self):
        return f"Subject: {self.subject_name}"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(nullable=False)
    date_of: Mapped[datetime] = mapped_column(Date, default=datetime.now().date())

    grade_student: Mapped["Student"] = relationship(back_populates="student_grade")
    subject: Mapped["Subject"] = relationship(back_populates="subject_grades")

    def __repr__(self):
        return f"Student id:{self.student_id}, subject id: {self.subject_id}, grade: {self.grade}, date of: {self.date_of}."
