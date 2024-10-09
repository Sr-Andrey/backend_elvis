import asyncio
from sqlalchemy import select, func, and_, distinct, text
from sqlalchemy.orm import aliased


from app.core.my_engine import MyAsyncSession
import app.core.schemas as s


async def statics_1():
    """пользователь с максимальным количеством достижений (штук)"""
    #Рассмотреть получения списка обьектов, а не одного
    async with MyAsyncSession() as session:
        # SQLAlchemy запрос
        stmt = (
            select(
                s.Users.id,
                s.Users.name,
                func.count(s.UsersAchievements.achievement_id).label("achievements_count")
                )
                .join(s.UsersAchievements, s.UsersAchievements.user_id==s.Users.id, isouter=True)
                .group_by(s.Users.id, s.Users.name)
                .order_by(func.count(s.UsersAchievements.achievement_id).desc())
        )

        result = await session.execute(stmt)
        user_with_max_achievements = result.mappings().first()

    return user_with_max_achievements


async def statics_2():
    """пользователь с максимальным количеством очков достижений (баллов суммарно)"""
    #Рассмотреть получения списка обьектов, а не одного
    async with MyAsyncSession() as session:
        # SQLAlchemy запрос
        stmt = (
            select(
                s.Users.id,
                s.Users.name,
                func.coalesce(func.sum(s.Achievements.number_of_points),0).label("total_points")
            )
            .join(s.UsersAchievements, s.UsersAchievements.user_id==s.Users.id, isouter=True)
            .join(s.Achievements, s.UsersAchievements.achievement_id==s.Achievements.id, isouter=True)
            .group_by(s.Users.id, s.Users.name)
            .order_by(func.coalesce(func.sum(s.Achievements.number_of_points),0).desc())
        )

        result = await session.execute(stmt)
        user_with_max_points = result.mappings().first()

    return user_with_max_points



async def statics_3():
    """пользователи с максимальной разностью очков достижений (разность баллов между
пользователями)"""
    #Рассмотреть получения списка обьектов, а не одного
    async with MyAsyncSession() as session:
        # SQLAlchemy запрос
        stmt = (
            select(
                s.Users.id,
                s.Users.name,
                func.coalesce(func.sum(s.Achievements.number_of_points),0).label("total_points")
            )
            .join(s.UsersAchievements, s.UsersAchievements.user_id==s.Users.id, isouter=True)
            .join(s.Achievements, s.UsersAchievements.achievement_id==s.Achievements.id, isouter=True)
            .group_by(s.Users.id, s.Users.name)
            .order_by(func.coalesce(func.sum(s.Achievements.number_of_points),0).asc())
        )

        result = await session.execute(stmt)
        user_with_min_points = result.mappings().first()

    return user_with_min_points


async def statics_4():
    """пользователи с минимальной разностью очков достижений(разность баллов между
пользователями)"""
    #Рассмотреть получения списка обьектов, а не одного
    async with MyAsyncSession() as session:
        # SQLAlchemy запрос для суммирования очков
        subquery = (
            select(
                s.Users.id.label("user_id"),
                s.Users.name.label("user_name"),
                func.coalesce(func.sum(s.Achievements.number_of_points), 0).label("total_points")
            )
            .outerjoin(s.UsersAchievements, s.Users.id == s.UsersAchievements.user_id)
            .outerjoin(s.Achievements, s.UsersAchievements.achievement_id == s.Achievements.id)
            .group_by(s.Users.id)
            .subquery()
        )
        other = aliased(subquery)
        # Основной запрос для нахождения минимальной разности
        stmt = (
            select(
                subquery.c.user_id.label("user1_id"),
                subquery.c.user_name.label("user1_name"),
                other.c.user_id.label("user2_id"),
                other.c.user_name.label("user2_name"),
                func.abs(subquery.c.total_points - other.c.total_points).label("points_difference")
            )
            .select_from(subquery)
            .join(other, subquery.c.user_id != other.c.user_id)
            .order_by(func.abs(subquery.c.total_points - other.c.total_points))  # Сортируем по возрастанию
            # .limit(1)
        )

        result = await session.execute(stmt)
        min_difference = result.mappings().first()

    return min_difference


async def statics_5():
    """пользователи, которые получали достижения 7 дней подряд (по дате выдачи, хотя бы
одно в каждый из 7 дней)"""
    #Рассмотреть получения списка обьектов, а не одного
    async with MyAsyncSession() as session:
        # SQLAlchemy запрос
        stmt = text("""WITH consecutive_dates AS (SELECT user_id,
            DATE(created_at) AS achievement_date,
            ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY DATE(created_at)) AS rn,
            DATE(created_at) - INTERVAL '1 day' * ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY DATE(created_at)) AS grp
                FROM
                    users_achievements )
            SELECT user_id, users.name
            FROM
                consecutive_dates
            LEFT JOIN users ON users.id=consecutive_dates.user_id
            GROUP BY
                user_id,users.name, grp
            HAVING
                COUNT(DISTINCT achievement_date) >= 7;""")

        result = await session.execute(stmt)
        users = result.mappings().all()

    return users



async def start_stat():
    """Создание задач"""
    task_statics_1 = asyncio.create_task(statics_1())
    task_statics_2 = asyncio.create_task(statics_2())
    task_statics_3 = asyncio.create_task(statics_3())
    task_statics_4 = asyncio.create_task(statics_4())
    task_statics_5 = asyncio.create_task(statics_5())


    results = await asyncio.gather(task_statics_1, task_statics_2,task_statics_3,task_statics_4,task_statics_5)

    itog = {"max_count_achievements": results[0],
            "max_sum_achievements": results[1],
            "max_dif_sum": {"user1_name" : results[2]['name'],
                            "user2_name" : results[1]['name'],
                            "points_difference" : results[1]['total_points'] - results[2]['total_points']
                            },
            "min_dif_sum": results[3],
            "users_in_7_days" : results[4]
            }


    return itog
