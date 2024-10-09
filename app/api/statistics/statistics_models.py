from pydantic import BaseModel,Field


class MaxCountAchievements(BaseModel):
    """Пользователь с максимальным количеством достижений"""
    name : str
    achievements_count : int


class MaxSumAchievements(BaseModel):
    """Пользователь с максимальным количеством очков достижений"""
    name : str
    total_points : int


class MaxMinDifSum(BaseModel):
    """Пользователи с разностью очков достижений"""
    user1_name : str
    user2_name : str
    points_difference : int


class UserName(BaseModel):
    """Имя пользователя"""
    name: str


class AllStatistics(BaseModel):
    """Отображение статистики"""
    max_count_achievements : MaxCountAchievements | None
    max_sum_achievements : MaxSumAchievements | None
    max_dif_sum : MaxMinDifSum | None
    min_dif_sum : MaxMinDifSum | None
    users_in_7_days : list[UserName]
