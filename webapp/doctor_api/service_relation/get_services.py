from webapp.doctor_api.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from typing import List
from webapp.pydantic_schemas.service import ServiceModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from webapp.db.redis import get_redis
import json


redis = get_redis()


@doctor_router.get('/services/{doctor_id:int}', response_model=List[ServiceModel])
async def get_doctor_services(doctor_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    redis_key = 'doctor ' + str(doctor_id) + ' services'
    print(redis_key)
    services = await redis.get(redis_key)
    if services:
        print('HHHEEWWRAY')
        return ORJSONResponse({'services': services})
    select_resp = select(Doctor).where(Doctor.id == doctor_id).options(selectinload(Doctor.services))
    sqlalch_obj_services = (await session.scalars(select_resp)).one().services
    services = [service.to_dict() for service in sqlalch_obj_services]
    await redis.set('doctor' + str(doctor_id) + 'services', json.dumps(services))

    return ORJSONResponse({'services': services})
