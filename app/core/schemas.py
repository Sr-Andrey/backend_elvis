from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy import Column, Integer, String, BOOLEAN,TIMESTAMP
from sqlalchemy import func, CheckConstraint, ForeignKey

from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

# setting path
import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent =os.path.dirname(os.path.dirname(current))
# print(parent)
# adding the parent directory to
# the sys.path.
# sys.path.append(parent)

from app.core.my_engine import sync_engine


class Base(DeclarativeBase):
    pass


tracking_sheet = []

update_column_function = PGFunction(
  schema='public',
  signature='update_column_function()',
  definition="""
    RETURNS TRIGGER AS $$
    BEGIN
    NEW.updated_at = now();
    RETURN NEW;
    END; $$ LANGUAGE PLPGSQL;
  """
)
tracking_sheet.append(update_column_function)


class UsersAchievements(Base):
    __tablename__ = 'users_achievements'
    __table_args__ = {
        'comment': 'Пользователи и Достижения'
        }

    user_id = Column(ForeignKey("users.id", ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, comment='id пользователя (`users`)')
    achievement_id = Column(ForeignKey("achievements.id", ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, comment='id достижения (`achievements`)')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='Дата создания')
    updated_at = Column(TIMESTAMP, server_default=func.now(), comment='Дата обновления')


update_column_trigger_users_achievements = PGTrigger(
    schema='public',
    signature='update_column_trigger_users_achievements',
    on_entity = 'users_achievements',
    definition="""BEFORE UPDATE
    ON users_achievements FOR EACH ROW EXECUTE PROCEDURE
    update_column_function()"""
    )
tracking_sheet.append(update_column_trigger_users_achievements)


user_achievement_relationship = UsersAchievements.__table__

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'comment': 'Пользователи'
        }

    id = Column(Integer,primary_key=True, comment='Уникальный идентификатор')
    name = Column(String(200), nullable=False, comment='Имя пользователя')
    lang_is_russian = Column(BOOLEAN, server_default='f', nullable=False, comment='Выбранный пользователем язык (False-en/True-ru)')
    is_active = Column(BOOLEAN, server_default='t', nullable=False, comment='Активная запись (False-неактивная)')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='Дата создания')
    updated_at = Column(TIMESTAMP, server_default=func.now(), comment='Дата обновления')

    achievements: Mapped[list[Achievements]] = relationship(secondary=user_achievement_relationship, back_populates='users')


update_column_trigger_users = PGTrigger(
    schema='public',
    signature='update_column_trigger_users',
    on_entity = 'users',
    definition="""BEFORE UPDATE
    ON users FOR EACH ROW EXECUTE PROCEDURE
    update_column_function()"""
    )
tracking_sheet.append(update_column_trigger_users)


class Achievements(Base):
    __tablename__ = 'achievements'
    __table_args__ = {
        'comment': 'Достижения'
        }

    id = Column(Integer,primary_key=True, comment='Уникальный идентификатор')
    name = Column(String(200), nullable=False, comment='Имя достижения')
    number_of_points = Column(Integer, CheckConstraint('number_of_points>=0'),nullable=False, comment='Количество баллов (очков достижений) за достижение')
    descriptions = Column(String(1000), nullable=True, comment='Описание сути достижения')
    is_active = Column(BOOLEAN, server_default='t', nullable=False, comment='Активная запись (False-неактивная)')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='Дата создания')
    updated_at = Column(TIMESTAMP, server_default=func.now(), comment='Дата обновления')

    users: Mapped[list[Users]] = relationship(secondary=user_achievement_relationship, back_populates='achievements')


update_column_trigger_achievements = PGTrigger(
    schema='public',
    signature='update_column_trigger_achievements',
    on_entity = 'achievements',
    definition="""BEFORE UPDATE
    ON achievements FOR EACH ROW EXECUTE PROCEDURE
    update_column_function()"""
    )
tracking_sheet.append(update_column_trigger_achievements)

my_metadata = Base.metadata
# my_metadata.create_all(bind=sync_engine, checkfirst=True)
