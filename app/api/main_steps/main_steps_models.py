from pydantic import BaseModel,Field


class Paginations(BaseModel):
    """Пагинация для отображения"""
    page : int = Field(default=1)
    size : int = Field(default=50, ge=5, le=100)


class Users(BaseModel):
    """Модель пользователя"""
    name : str
    language : str


class Achievements(BaseModel):
    """Модель достижения"""
    name : str
    number_of_points : int
    descriptions : str | None
    is_active : bool | None


class AllInfo(BaseModel):
    """Отображение информации"""
    total : int
    page : int
    size : int
    pages : int
    data : list[Users | Achievements]


class UsersAchievements(BaseModel):
    """Изменения связей"""
    user_name : str
    achievement_name : str
