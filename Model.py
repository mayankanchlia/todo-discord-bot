from sqlalchemy import create_engine,Column, Integer, String, ForeignKey, Table, MetaData,Date, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


def init():
    print("init ")
    global engine
    engine = create_engine('sqlite:///tasks.db', echo = True)
    Base = declarative_base()
    meta = MetaData()
    global task
    task = Table(
        "task", meta,
        Column("id", Integer, primary_key=True),
        Column("member_id", Integer),
        Column("guild_id", Integer),
        Column("date_list", Date),
        Column("task_message", String),
        Column("status", Boolean)
    )
    meta.create_all(engine)


def insert_to_task(member_id,guild_id,date, message, status):
    ins = task.insert().values(member_id=member_id, guild_id=guild_id, date_list=date, task_message=message, status=status)
    conn = engine.connect()
    result = conn.execute(ins)


def get_task_for_username(member_id, date=datetime.today()):
    s= task.select().where(task.c.member_id == member_id and task.c.date_list == date)
    conn = engine.connect()
    result = conn.execute(s)
    return result
