from fastapi import APIRouter, status,  Depends

from . import main_steps_models as m
from . import main_steps_functions as f

router_main = APIRouter(
    prefix="/main",
    tags=["Main"]
)

@router_main.get(path='/users',
                 status_code=status.HTTP_200_OK,
                 response_model=m.AllInfo,
                 summary='Отображение пользователей',
                 )
def main_select_users(
    paginations: m.Paginations = Depends(m.Paginations)
    ):
    return f.select_users(paginations)



@router_main.get(path='/achievements',
                 status_code=status.HTTP_200_OK,
                 response_model=m.AllInfo,
                 summary='Отображение достижений',
                 )
def main_select_achievements(
    paginations: m.Paginations = Depends(m.Paginations)
    ):
    return f.select_achievements(paginations)


@router_main.post(path='/insert_achievement',
                 status_code=status.HTTP_200_OK,
                #  response_model=m.AllInfo,
                 summary='Добавление достижения',)
def main_insert_achievement(
    achievement: m.Achievements
    ):
    return f.insert_achievement(achievement)


@router_main.patch(path='/insert_achievement_to_user',
                 status_code=status.HTTP_200_OK,
                #  response_model=m.AllInfo,
                 summary='Добавление достижения пользователю',)
def main_insert_achievement_to_user(connection:m.UsersAchievements):
    return f.insert_achievement_to_user(connection)


@router_main.post(path='/achievement_for_user',
                 status_code=status.HTTP_200_OK,
                 response_model=m.UsersAchievementsWithLang,
                 summary='Отображение достижений по пользователю',)
def main_achievement_for_user(user:str):
    return f.achievement_for_user(user)
