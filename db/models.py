from sqlalchemy import create_engine, MetaData, ForeignKey, String, Integer
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase

engine = create_engine("sqlite:///database.db")


class Base(DeclarativeBase):
    pass


metadata_obj = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


class Teachers(Base):  # таблица преподавателей
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_code: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(30))
    degree: Mapped[str] = mapped_column(String(30))
    work_position: Mapped[str] = mapped_column(String(30))
    experience: Mapped[int] = mapped_column(Integer)


class Subjects(Base):  # таблица предметов
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_code: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(String(30), nullable=False)
    hours: Mapped[int] = mapped_column(Integer, nullable=False)


class Schedule(Base): # таблица разгрузки
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_code: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.teacher_code"), nullable=False)
    subject_code: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.subject_code"), nullable=False)
    group_name: Mapped[str] = mapped_column(String(30), nullable=False)


table_display_names = {
    "teachers": "Преподаватели",
    "subjects": "Предметы",
    "schedule": "Нагрузка"
}

teacher_column_names = {
    "teacher_code": "Код учителя",
    "name": "Имя",
    "surname": "Фамилия",
    "middle_name": "Отчество",
    "degree": "Учёная степень",
    "work_position": "Должность",
    "experience": "Стаж"
}

subject_column_names = {
    "subject_code": "Код предмета",
    "subject": "Название",
    "hours": "Количество часов"
}

schedule_column_names = {
    "teacher_code": "Преподаватель",
    "subject_code": "Предмет",
    "group_name": "Группа"
}