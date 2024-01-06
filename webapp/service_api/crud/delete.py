from webapp.service_api.router import service_router
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import delete
from starlette import status
from fastapi.responses import Response
from webapp.pydantic_schemas.user import ID


@service_router.delete('/{id:int}')
async def delete_service(id: int, session: AsyncSession = Depends(get_session)) -> Response:
    try:
        await session.execute(
            delete(Service).where(Service.id == id),
        )
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
