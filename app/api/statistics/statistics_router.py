from fastapi import APIRouter, status,  Depends
import asyncio

from . import statistics_models as m
from . import statistics_functions as f

router_statistics = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router_statistics.get(path='/all',
                 status_code=status.HTTP_200_OK,
                 response_model=m.AllStatistics,
                 summary='Отображение статистики',
                 )
async def stat_all_stats():
    result = await f.start_stat()
    return result
