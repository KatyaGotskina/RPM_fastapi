from webapp.patient_api.router import patient_router
from webapp.models.clinic.timetable import Timetable
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import delete
from starlette import status
from fastapi.responses import Response
from webapp.pydantic_schemas.user import ID


@patient_router.delete('/delete_appointment')
async def delete_appointment(body: ID, session: AsyncSession = Depends(get_session)) -> Response:
    try:
        await session.execute(
            delete(Timetable).where(Timetable.id == body.id),
        )
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
