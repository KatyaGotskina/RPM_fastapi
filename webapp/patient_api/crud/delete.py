from webapp.patient_api.router import patient_router
from webapp.models.clinic.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import delete
from starlette import status
from fastapi.responses import Response
from webapp.metrics import patient_counter, patient_errors_counter


@patient_router.delete('/{id:int}')
async def delete_user(id: int, session: AsyncSession = Depends(get_session)) -> Response:
    patient_counter.labels(endpoint='/patient/delete').inc()
    try:
        await session.execute(
            delete(User).where(User.id == id),
        )
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        patient_errors_counter.labels(endpoint='/patient/delete').inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
