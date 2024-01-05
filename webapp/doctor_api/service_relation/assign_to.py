from webapp.doctor_api.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException, Response
from starlette import status
from sqlalchemy import select
from webapp.pydantic_schemas.doctor import DoctorServiceID
from sqlalchemy.orm import selectinload


# НЕ работает уникальность пары ID и ошибка не конкретезирована
@doctor_router.post('/assign_service/')
async def assign_service_to_doctor(body: DoctorServiceID, session: AsyncSession = Depends(get_session)) -> Response:
    try:
        select_resp = select(Doctor).where(Doctor.id == body.doctor_id).options(selectinload(Doctor.services))
        doctor = (await session.scalars(select_resp)).one()
        service = (await session.scalars(select(Service).where(Service.id == body.service_id))).one()
        doctor.services.append(service)
        await session.commit()
        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
