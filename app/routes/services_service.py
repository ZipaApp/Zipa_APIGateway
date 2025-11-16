from fastapi import APIRouter, Request, Response
import httpx
import os
from typing import Dict

router = APIRouter()
SERVICES_SERVICE_URL = os.getenv("SERVICES_SERVICE_URL")

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}
async def forward_request(method: str, path: str, request: Request) -> Response:
    """
    Reenvía la petición al microservicio de servicios.
    Mantiene raw body, headers y soporta JSON/multipart.
    """
    url = f"{SERVICES_SERVICE_URL}{path}"
    body = await request.body()

    headers: Dict[str, str] = {
        k: v for k, v in request.headers.items()
        if k.lower() not in HOP_BY_HOP_HEADERS and k.lower() != "host"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            method=method,
            url=url,
            content=body,
            headers=headers
        )

        response_headers = {
            k: v for k, v in resp.headers.items()
            if k.lower() not in HOP_BY_HOP_HEADERS
        }

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=response_headers
        )


# ==================================
# CALENDARIO
# ==================================

@router.post("/calendario")
async def crear_franja(request: Request):
    return await forward_request("POST", "/calendario", request)

@router.get("/calendario/{servicioId}")
async def obtener_disponibilidad(servicioId: str, request: Request):
    query = f"/calendario/{servicioId}"
    if request.url.query:
        query += f"?{request.url.query}"
    return await forward_request("GET", query, request)

@router.put("/calendario/{id}")
async def actualizar_franja(id: str, request: Request):
    return await forward_request("PUT", f"/calendario/{id}", request)

@router.put("/calendario/{id}/liberar")
async def liberar_franja(id: str, request: Request):
    return await forward_request("PUT", f"/calendario/{id}/liberar", request)

@router.delete("/calendario/{id}")
async def eliminar_franja(id: str, request: Request):
    return await forward_request("DELETE", f"/calendario/{id}", request)


# ==================================
# HISTORIAL
# ==================================

@router.post("/historial")
async def crear_historial(request: Request):
    return await forward_request("POST", "/historial", request)

@router.get("/historial")
async def listar_historiales(request: Request):
    return await forward_request("GET", "/historial", request)

@router.get("/historial/{mascotaId}")
async def historial_por_mascota(mascotaId: str, request: Request):
    return await forward_request("GET", f"/historial/{mascotaId}", request)

@router.put("/historial/{id}")
async def actualizar_historial(id: str, request: Request):
    return await forward_request("PUT", f"/historial/{id}", request)

@router.delete("/historial/{id}")
async def eliminar_historial(id: str, request: Request):
    return await forward_request("DELETE", f"/historial/{id}", request)


# ==================================
# RESERVAS
# ==================================

@router.post("/reservas")
async def crear_reserva(request: Request):
    return await forward_request("POST", "/reservas", request)

@router.get("/reservas")
async def listar_reservas(request: Request):
    return await forward_request("GET", "/reservas", request)

@router.get("/reservas/mascota/{mascotaId}")
async def reservas_por_mascota(mascotaId: str, request: Request):
    return await forward_request("GET", f"/reservas/mascota/{mascotaId}", request)

@router.put("/reservas/{id}/estado")
async def cambiar_estado_reserva(id: str, request: Request):
    return await forward_request("PUT", f"/reservas/{id}/estado", request)

@router.delete("/reservas/{id}")
async def cancelar_reserva(id: str, request: Request):
    return await forward_request("DELETE", f"/reservas/{id}", request)


# ==================================
# SERVICIOS DINÁMICOS POR TIPO
# ==================================

@router.get("/{type}")
async def listar_por_tipo(type: str, request: Request):
    query = f"/{type}"
    if request.url.query:
        query += f"?{request.url.query}"
    return await forward_request("GET", query, request)

@router.get("/{type}/{id}")
async def obtener_servicio(type: str, id: str, request: Request):
    return await forward_request("GET", f"/{type}/{id}", request)

@router.post("/{type}")
async def crear_servicio(type: str, request: Request):
    return await forward_request("POST", f"/{type}", request)

@router.put("/{type}/{id}")
async def actualizar_servicio(type: str, id: str, request: Request):
    return await forward_request("PUT", f"/{type}/{id}", request)

@router.delete("/{type}/{id}")
async def eliminar_servicio(type: str, id: str, request: Request):
    return await forward_request("DELETE", f"/{type}/{id}", request)

