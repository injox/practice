from sqlalchemy import create_engine, MetaData, ForeignKey, String, Integer
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase

engine = create_engine("sqlite:///database.db")

class Base(DeclarativeBase):
    pass


metadata_obj = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


class Teachers(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_code: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(30))
    degree: Mapped[str] = mapped_column(String(30))
    work_position: Mapped[str] = mapped_column(String(30))
    experience: Mapped[int] = mapped_column(Integer)


class Subjects(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_code: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(String(30), nullable=False)
    hours: Mapped[int] = mapped_column(Integer, nullable=False)


class Schedule(Base):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_code: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.teacher_code"), nullable=False)
    subject_code: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.subject_code"), nullable=False)
    group_name: Mapped[str] = mapped_column(String(30), nullable=False)