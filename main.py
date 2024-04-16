import argparse
from sqlalchemy import select, delete, update

from connect_db import session
from models import Student, Group, Teacher, Subject, Grade


def create_record(model, detail):
    model = model(detail)
    session.add(model)

    session.commit()
    print("Success")


def list_model(model):
    model_to_show = select(model)
    results = session.execute(model_to_show)

    for res in results:
        print(res)


def update_record(model, id_number, name):
    model_to_update = None
    match model.__name__:
        case "Teacher":
            model_to_update = update(model).where(model.id == id_number).values(teacher_name=name)
        case "Student":
            model_to_update = update(model).where(model.id == id_number).values(student_name=name)
        case "Subject":
            model_to_update = update(model).where(model.id == id_number).values(subject_name=name)
        case "Group":
            model_to_update = update(model).where(model.id == id_number).values(group_number=name)

    if model_to_update is not None:
        session.execute(model_to_update)
        session.commit()
        print("Success")
    else:
        print("Invalid model name.")


def remove_record(model, detail):
    record_to_delete = delete(model).where(model.id == detail)
    if record_to_delete is not None:
        session.execute(record_to_delete)
        session.commit()
        print("Success")
    else:
        print(f"Not found {model} with id {detail}.")


def main():
    parser = argparse.ArgumentParser(description="CRUD operations with a database")
    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], help="Action to perform")
    parser.add_argument("-m", "--model", choices=["Student", "Group", "Teacher", "Subject", "Grade"], help="Model to operate on")
    parser.add_argument("-n", "--name", help="Name of the student or teacher, subject")
    parser.add_argument("-i", "--id", type=int, help="id of the record")

    args = parser.parse_args()

    model = None

    match args.model:
        case "Teacher":
            model = Teacher
        case "Student":
            model = Student
        case "Group":
            model = Group
        case "Grade":
            model = Grade
        case "Subject":
            model = Subject

    id_detail = args.id
    name_detail = args.name

    match args.action:
        case "create":
            create_record(model, name_detail)
        case "list":
            list_model(model)
        case "update":
            update_record(model, id_detail, name_detail)
        case "remove":
            remove_record(model, id_detail)


if __name__ == '__main__':
    main()
