from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importación de routers con los nombres exactos
from app.routes.user_service import router as user_router
from app.routes.inventory_service import router as inventory_router
from app.routes.services_service import router as services_router


app = FastAPI(
    title="API Gateway - E-commerce Mascotas",
    version="1.0.0",
    description="Gateway unificado para los microservicios del proyecto."
)


# =====================================================
#                 MIDDLEWARE – LOG DE REQUESTS
# =====================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"[Gateway] {request.method} {request.url}")
    response = await call_next(request)
    return response


# =====================================================
#                           CORS
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # en producción cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
#                 REGISTRO DE ROUTERS
# =====================================================
app.include_router(user_router, prefix="/user-service")
app.include_router(inventory_router, prefix="/inventory-service")
app.include_router(services_router, prefix="/services-service")


# =====================================================
#                        RUTA BASE
# =====================================================
@app.get("/")
async def root():
    return {
        "status": "API Gateway funcionando",
        "services": [
            "/user-service/*",
            "/inventory-service/*",
            "/services-service/*"
        ]
    }


# =====================================================
#                         RUN LOCAL
# =====================================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

