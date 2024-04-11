from sqlalchemy import Table, Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship)
from datetime import datetime


class Base(DeclarativeBase):
    pass


student_grade_association = Table(
    "student_grade_association", Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("grades_id", Integer, ForeignKey("grades.id"))
)


subject_grade_association = Table(
    "subject_grade_association", Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id")),
    Column("grades_id", Integer, ForeignKey("grades.id"))
)


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_number: Mapped[int] = mapped_column(nullable=False)
    students = relationship("Student", back_populates ="group")


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_name: Mapped[str] = mapped_column(String(30), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", secondary=student_grade_association, back_populates="students")


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_name: Mapped[str] = mapped_column(String(30), nullable=False)
    subject = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subject")
    grades = relationship("Grade", secondary=subject_grade_association, back_populates="subjects")


class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete=""))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(nullable=False)
    date_of: Mapped[datetime] = mapped_column(Date, default=datetime.now().date())
    students = relationship("Student", secondary=student_grade_association, back_populates="grades")
    subjects = relationship("Subject", secondary=subject_grade_association, back_populates="grades")
