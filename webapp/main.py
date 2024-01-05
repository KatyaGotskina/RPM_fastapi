from fastapi import FastAPI
from webapp.patient_api.router import patient_router
from webapp.service_api.router import service_router
from webapp.doctor_api.router import doctor_router
import uvicorn
from webapp.metrics import metrics


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)
    app.include_router(patient_router)
    app.include_router(service_router)
    app.include_router(doctor_router)

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    setup_routers(app)
    return app

if __name__ == '__main__':
    uvicorn.run('main:create_app', host='0.0.0.0', port=8000, factory=True, reload=True)