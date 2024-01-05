from webapp.doctor_api.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends
from sqlalchemy import select
from typing import Any
from webapp.pydantic_schemas.doctor import DoctorModel
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import selectinload


@doctor_router.get('/get_by_id/{id:int}', response_model=DoctorModel)
async def get_patient(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    select_resp = select(Doctor).where(Doctor.id == id)    #.options(selectinload(Doctor.services))
    doctor_elem = (await session.scalars(select_resp)).one()
    return DoctorModel.model_validate(doctor_elem).model_dump(mode='json')