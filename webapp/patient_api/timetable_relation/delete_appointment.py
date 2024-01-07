from webapp.patient_api.router import patient_router
from webapp.models.clinic.timetable import Timetable
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import delete
from starlette import status
from fastapi.responses import Response
from webapp.metrics import patient_counter, patient_errors_counter


@patient_router.delete('/appointment/{timetable_id:int}')
async def delete_appointment(timetable_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    patient_counter.labels(endpoint='DELETE /patient/appointment').inc()
    try:
        await session.execute(
            delete(Timetable).where(Timetable.id == timetable_id),
        )
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        patient_errors_counter.labels(endpoint='DELETE /patient/appointment').inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
