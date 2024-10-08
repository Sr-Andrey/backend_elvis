from sqlalchemy import case, select,func
from sqlalchemy.exc import IntegrityError
from googletrans import Translator

from . import main_steps_models as m
from app.core.my_engine import MySession
import app.core.schemas as s
import app.core.exceptions as e


def text_translator(text, dest):
    try:
        translator = Translator()
        translation = translator.translate(text=text, dest=dest)

        return translation.text

    except Exception as ex:
        return ex


def select_users(paginations: m.Paginations):
    """Отображение всех пользователей"""
    with MySession() as session:
        query = (
            session.query(
                s.Users.name,
                case((s.Users.lang_is_russian == False, 'en'), else_ = 'ru').label("language")
            )
            .filter(s.Users.is_active==True)
            )

        # Получение данных для пагинации
        count_data = session.scalar(select(func.count()).select_from(query))
        query = query.offset((paginations.page-1)*paginations.size)
        query = query.limit(paginations.size)

        data = session.execute(query).mappings().all()

        pages = count_data//paginations.size if count_data%paginations.size==0 else count_data//paginations.size +1


    result = {
        'total': count_data,
        'page':paginations.page,
        'size':paginations.size,
        'pages':pages,
        'data': data,
        }

    return result



def select_achievements(paginations: m.Paginations):
    """Отображение всех доступных достижений"""
    with MySession() as session:
        query = (
            session.query(
                s.Achievements.name,
                s.Achievements.number_of_points,
                s.Achievements.descriptions,
                s.Achievements.is_active
            )
            # .filter(s.Achievements.is_active==True)  Варианты для фильтрации активных
            )

        # Получение данных для пагинации
        count_data = session.scalar(select(func.count()).select_from(query))
        query = query.offset((paginations.page-1)*paginations.size)
        query = query.limit(paginations.size)

        data = session.execute(query).mappings().all()


        pages = count_data//paginations.size if count_data%paginations.size==0 else count_data//paginations.size +1


    result = {
        'total': count_data,
        'page':paginations.page,
        'size':paginations.size,
        'pages':pages,
        'data': data,
        }

    return result



def insert_achievement(achievement: m.Achievements):
    """Добавление достижения"""
    #Проверка на пустое рабочее место
    with MySession() as session:
        query = (
            session.query(
                s.Achievements
                )
            .filter(s.Achievements.name==achievement.name)
        )
        data = session.execute(query).scalars().first()
        if data:
            raise e.is_achievements

        add_value = s.Achievements(
            name = achievement.name,
            number_of_points = achievement.number_of_points,
            descriptions = achievement.descriptions,
            is_active = achievement.is_active
        )

        session.add(add_value)
        session.commit()

    return "success, entry added"


def insert_achievement_to_user(connection:m.UsersAchievements):
    """Добавление достижения пользователю"""
    with MySession() as session:
        #Получение id достижения
        achievement_name_object = session.query(s.Achievements).filter(s.Achievements.name==connection.achievement_name).scalar()

        if not achievement_name_object:
            raise e.is_not_achievement

        result = session.query(s.Users).where(s.Users.name==connection.user_name).one_or_none()

        if not result:
            raise e.is_not_user

        result.achievements.append(achievement_name_object)

        try:
            session.commit()
        except IntegrityError:
            raise e.is_connection


    return f"success, {connection.user_name} add achievement - {connection.achievement_name}"


def achievement_for_user(user:str):
    """информация о выданных пользователю достижениях на выбранном пользователем языке"""
    with MySession() as session:
        result = session.query(s.Users).where(s.Users.name==user).one_or_none()

        if not result:
            raise e.is_not_user
        print(result.lang_is_russian)
        lang = 'ru' if result.lang_is_russian else 'en'
        for i in result.achievements:
            print(i.name)
            print(i.number_of_points)
            print(i.descriptions)
            print(text_translator(text=i.descriptions,dest=lang))
    return result
