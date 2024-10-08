from faker import Faker

# setting path
import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)


import app.core.schemas as s
from app.core.my_engine import MySession

fake = Faker()
Faker.seed(0)

# Генерация пользователей
def create_fake_users(n):
    with MySession() as session:
        users = []
        for _ in range(n):
            user = s.Users(
                name=fake.name(),
                lang_is_russian=fake.boolean(chance_of_getting_true=75),
                is_active=fake.boolean(chance_of_getting_true=90)
            )
            users.append(user)
        session.add_all(users)
        session.commit()

# Генерация достижений
def create_fake_achievements(n):
    with MySession() as session:
        achievements = []
        for _ in range(n):
            achievement = s.Achievements(
                name=fake.word(),
                number_of_points=fake.random_int(min=70, max=100),
                descriptions=fake.sentence(nb_words=10),
                is_active=fake.boolean(chance_of_getting_true=90)
            )
            achievements.append(achievement)
        session.add_all(achievements)
        session.commit()

# Связывание пользователей с достижениями
def create_fake_users_achievements(n):
    with MySession() as session:
        user_ids = [user.id for user in session.query(s.Users).all()]
        achievement_ids = [achievement.id for achievement in session.query(s.Achievements).all()]

        existing_pairs = set()

        while len(existing_pairs) < n:
            user_id = fake.random_element(user_ids)
            achievement_id = fake.random_element(achievement_ids)
            pair = (user_id, achievement_id)

            # Проверяем, существует ли пара
            if pair not in existing_pairs:
                user_achievement = s.UsersAchievements(
                    user_id=user_id,
                    achievement_id=achievement_id
                )
                session.add(user_achievement)
                existing_pairs.add(pair)  # Добавляем пару в множество

        session.commit()

# Вызов функций для генерации данных
create_fake_users(10)  # Создание 10 пользователей
create_fake_achievements(5)  # Создание 5 достижений
create_fake_users_achievements(20)  # Связывание пользователей и достижений (20 связей)
