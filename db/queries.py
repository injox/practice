from db.models import Teachers, Subjects, Schedule, engine, Base, session
from sqlalchemy import or_, inspect, String, text
from sqlalchemy.exc import IntegrityError, DataError
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

table_map = {
            'teachers': Teachers,
            'subjects': Subjects,
            'schedule': Schedule
        }


class ORM:
    @staticmethod
    def create_tables():  # создание таблиц из моделей
        Base.metadata.create_all(engine)

    @staticmethod
    def add_record(table_name, **kwargs):  # добавление записи в таблицу
        if table_name not in table_map:
            raise ValueError(f"Неверное имя таблицы: {table_name}")

        table_class = table_map[table_name]

        for column, value in kwargs.items():
            column_type = getattr(table_class, column).type.python_type
            if column_type is int:
                try:
                    kwargs[column] = int(value)
                except ValueError:
                    raise ValueError(f"Значение для {column} должно быть целым числом, получено: {value}")

        try:
            new_record = table_class(**kwargs)
            session.add(new_record)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"Ошибка целостности данных: {str(e)}")
        except DataError as e:
            session.rollback()
            raise ValueError(f"Ошибка типа данных: {str(e)}")
        except Exception as e:
            session.rollback()
            raise ValueError(f"Неожиданная ошибка: {str(e)}")

    @staticmethod
    def update_data(table_name, column, row_id, new_value):  # обновление данных в таблице
        if table_name not in table_map:
            raise ValueError(f"Неверное имя таблицы: {table_name}")

        table_class = table_map[table_name]

        try:
            row_id = int(row_id)
            query = session.query(table_class).filter(table_class.id == row_id)
            record = query.first()
            if not record:
                raise ValueError(f"Запись с ID {row_id} не найдена в таблице {table_name}")

            column_type = getattr(table_class, column).type.python_type
            new_value = column_type(new_value)

            query.update({column: new_value})
            session.commit()
            return "Данные успешно обновлены"
        except ValueError as e:
            session.rollback()
            raise ValueError(str(e))
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"Ошибка целостности данных: {str(e)}")
        except DataError as e:
            session.rollback()
            raise ValueError(f"Ошибка типа данных: {str(e)}")
        except Exception as e:
            session.rollback()
            raise ValueError(f"Произошла ошибка при обновлении данных: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def search_database(table_name, search_term):
        if table_name not in table_map:
            raise ValueError(f"Неверное имя таблицы")

        model = table_map[table_name]

        try:
            query = session.query(model)
            filters = []
            for column in model.__table__.columns:
                if isinstance(column.type, String):
                    filters.append(column.ilike(f'%{search_term}%'))
                else:
                    filters.append(column == search_term)

            query = query.filter(or_(*filters))
            results = query.all()

            readable_results = []
            for result in results:
                result_dict = {column.name: getattr(result, column.name) for column in model.__table__.columns}
                readable_results.append(result_dict)

            return readable_results
        except Exception as e:
            raise ValueError(f"Произошла ошибка во время поиска: {str(e)}")
        finally:
            session.close()
    @staticmethod
    def export_database_to_xml(output_directory, selected_table):  # экспорт данных в XML
        inspector = inspect(engine)
        try:
            os.makedirs(output_directory, exist_ok=True)
            all_tables = inspector.get_table_names()

            if selected_table not in all_tables:
                return f"Выбранная таблица {selected_table} не существует в базе данных."

            file_path = os.path.join(output_directory, f"{selected_table}.xml")
            root = ET.Element(selected_table)
            columns = [col['name'] for col in inspector.get_columns(selected_table)]

            result = session.execute(text(f"SELECT * FROM {selected_table}"))

            for row in result:
                record = ET.SubElement(root, 'record')
                for col, value in zip(columns, row):
                    field = ET.SubElement(record, col)
                    field.text = str(value) if value is not None else ''

            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_str)

            return f"Данные из таблицы {selected_table} записаны в файл {file_path}"
        except Exception as e:
            return f"Произошла ошибка при экспорте данных: {str(e)}"
        finally:
            session.close()

    @staticmethod
    def display_data(table_name):
        if table_name not in table_map:
            return [{"Error": f"Неверное имя таблицы."}]

        table_class = table_map[table_name]

        if table_name == 'schedule':
            records = session.query(Schedule, Teachers, Subjects).join(Teachers).join(Subjects).all()
            if not records:
                return [{"Info": "Нет данных в таблице"}]

            return [
                {
                    "ID": schedule.id,
                    "Учитель": f"{teacher.surname} {teacher.name}",
                    "Предмет": subject.subject,
                    "Группа": schedule.group_name
                }
                for schedule, teacher, subject in records
            ]
        else:
            records = session.query(table_class).all()
            if not records:
                return [{"Info": f"Нет данных в таблице"}]

            columns = [column.name for column in table_class.__table__.columns]
            return [
                {column: getattr(record, column) for column in columns}
                for record in records
            ]

    @staticmethod
    def delete_record(table_name, record_id):  # удаление записи из таблицы
        if table_name not in table_map:
            return f"Неверное имя таблицы"

        table_class = table_map[table_name]
        try:
            record = session.query(table_class).filter(table_class.id == record_id).first()

            if record:
                session.delete(record)
                session.commit()
                return f"Запись с ID {record_id} успешно удалена из таблицы"
            else:
                return f"Запись с ID {record_id} не найдена в таблице"
        except Exception as e:
            session.rollback()
            return f"Произошла ошибка при удалении записи: {str(e)}"
        finally:
            session.close()


