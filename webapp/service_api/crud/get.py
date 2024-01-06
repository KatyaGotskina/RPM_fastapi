from webapp.service_api.router import service_router
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends
from sqlalchemy import select
from typing import List, Any
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.service import ServiceModel


@service_router.get('/all', response_model=List[ServiceModel])
async def get_services(session: AsyncSession = Depends(get_session)) -> ORJSONResponse: 
    services = (await session.execute(select(Service))).scalars()
    services_json = [ServiceModel.model_validate(service).model_dump(mode='json') for service in services]
    return ORJSONResponse(services_json)

@service_router.get('/{id:int}', response_model=ServiceModel)
async def get_service(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    select_resp = select(Service).where(Service.id == id)
    service = (await session.scalars(select_resp)).one()
    return ServiceModel.model_validate(service).model_dump(mode='json')
