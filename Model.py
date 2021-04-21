from sqlalchemy import create_engine,Column, Integer, String, ForeignKey, Table, MetaData,Date, Boolean, and_, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


def init_db():
    print("init ")
    global engine
    engine = create_engine('sqlite:///task_list.db', echo = True)
    meta = MetaData()
    global session
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    meta.create_all(engine)
    Task()


def insert_to_task(member_id,guild_id,date, message, status):
    task = Task(member_id=member_id, guild_id=guild_id, task_created_date=date, task_ending_date=date, task_text=message, status=status)
    session.add(task)
    session.commit()


def get_task_for_member_id(member_id, date=datetime.today()):
    result_list = session.query(Task).filter(Task.member_id == member_id)\
        .filter(Task.task_ending_date == func.Date(date)).all()
    return result_list


def get_task_by_username_and_text_update(member_id, task_message, date, status):
    task = session.query(Task)\
        .filter(Task.task_ending_date == func.Date(date))\
        .filter(Task.member_id == member_id)\
        .filter(Task.task_text == task_message).one()
    task.status = status
    session.commit()
    return task


def delete_task_from_db(member_id, task_message, date):
    task = session.query(Task) \
        .filter(Task.task_ending_date == func.Date(date)) \
        .filter(Task.member_id == member_id) \
        .filter(Task.task_text == task_message).delete()
    return task


def delete_task_by_id_from_db(task_id):
    result = session.query(Task) \
        .filter(Task.id == task_id).delete()
    return result


def delete_all_task_by_member_id(member_id, date):
    result = session.query(Task) \
        .filter(Task.member_id == member_id)\
        .filter(Task.task_ending_date == date).delete()


def update_task_by_id(task_id):
    task = session.query(Task) \
        .filter(Task.id == task_id).one()
    task.status = not task.status
    session.commit()
    return task


class Task(Base):
    __tablename__ = "task_list"
    id = Column("id", Integer, primary_key=True)
    member_id = Column("member_id", Integer)
    guild_id = Column("guild_id", Integer)
    task_created_date = Column("date_created", Date)
    task_ending_date = Column("date_end",Date)
    task_text = Column("task_text", String)
    status = Column("status", Boolean)
    private = Column("private", Boolean)