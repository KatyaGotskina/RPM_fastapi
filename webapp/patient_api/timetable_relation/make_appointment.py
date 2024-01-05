from webapp.patient_api.router import patient_router
from webapp.models.clinic.timetable import Timetable
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import insert
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.timetable import TimetableCreateModel


@patient_router.post('/make_appointment')
async def make_appointment(body: TimetableCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    try:
        new_id = (
            await session.scalars(
                insert(Timetable).values(
                    {
                        'doctor_id': body.doctor_id, 
                        'user_id': body.user_id,
                        'service_id': body.service_id,
                        'start': body.start

                    },
                ).returning(Timetable.id),
            )
        ).one()
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username is already used',
        )
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
