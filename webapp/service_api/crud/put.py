from webapp.service_api.router import service_router
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import update
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.service import ServiceModel


@service_router.put('/')
async def update_service_data(body: ServiceModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    try:
        updated_data = (
            await session.execute(
                update(Service)
                .where(Service.id == body.id)
                .values({
                    'name': body.name,
                    'duration': body.duration,
                }).returning(Service.name, Service.duration)
            )
        ).one()
        await session.commit()
        return ORJSONResponse(
            {
                'name': updated_data.name,
                'duration': updated_data.duration,
            },
        )
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='name is already used',
        )
