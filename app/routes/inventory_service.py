# routes/inventory_service.py
from fastapi import APIRouter, Request, Response
import httpx
import os
from typing import Dict

router = APIRouter()
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

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
    Reenvía la petición al microservicio de inventario y retorna la Response adecuada.
    Preserva headers y el body crudo (útil para JSON y multipart).
    """
    url = f"{INVENTORY_SERVICE_URL}{path}"
    body = await request.body()
    # Copiar headers, pero quitar host (lo pone httpx) y algunos hop-by-hop
    headers: Dict[str, str] = {
        k: v for k, v in request.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS and k.lower() != "host"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(method=method, url=url, content=body, headers=headers)
        # Filtrar headers a devolver
        response_headers = {
            k: v for k, v in resp.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS
        }
        return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)


# ============================
# ALMACEN
# ============================

@router.post("/almacen")
async def crear_almacen(request: Request):
    return await forward_request("POST", "/almacen", request)

@router.get("/almacen")
async def obtener_almacenes(request: Request):
    return await forward_request("GET", "/almacen", request)

@router.get("/almacen/{id}")
async def obtener_almacen(id: str, request: Request):
    return await forward_request("GET", f"/almacen/{id}", request)

@router.patch("/almacen/{id}")
async def actualizar_almacen(id: str, request: Request):
    return await forward_request("PATCH", f"/almacen/{id}", request)

@router.delete("/almacen/{id}")
async def eliminar_almacen(id: str, request: Request):
    return await forward_request("DELETE", f"/almacen/{id}", request)


# ============================
# CLASIFICACION
# ============================

@router.post("/clasificacion")
async def crear_clasificacion(request: Request):
    return await forward_request("POST", "/clasificacion", request)

@router.get("/clasificacion")
async def obtener_clasificaciones(request: Request):
    return await forward_request("GET", "/clasificacion", request)

@router.get("/clasificacion/{id}")
async def obtener_clasificacion(id: str, request: Request):
    return await forward_request("GET", f"/clasificacion/{id}", request)

@router.patch("/clasificacion/{id}")
async def actualizar_clasificacion(id: str, request: Request):
    return await forward_request("PATCH", f"/clasificacion/{id}", request)

@router.delete("/clasificacion/{id}")
async def eliminar_clasificacion(id: str, request: Request):
    return await forward_request("DELETE", f"/clasificacion/{id}", request)


# ============================
# COMERCIA
# ============================

@router.post("/comercia")
async def crear_comercia(request: Request):
    return await forward_request("POST", "/comercia", request)

@router.get("/comercia")
async def obtener_comercias(request: Request):
    return await forward_request("GET", "/comercia", request)

@router.get("/comercia/{id}")
async def obtener_comercia(id: str, request: Request):
    return await forward_request("GET", f"/comercia/{id}", request)

@router.patch("/comercia/{id}")
async def actualizar_comercia(id: str, request: Request):
    return await forward_request("PATCH", f"/comercia/{id}", request)

@router.delete("/comercia/{id}")
async def eliminar_comercia(id: str, request: Request):
    return await forward_request("DELETE", f"/comercia/{id}", request)


# ============================
# MOVIMIENTOS
# ============================

@router.post("/movimientos")
async def crear_movimiento(request: Request):
    return await forward_request("POST", "/movimientos", request)

@router.get("/movimientos")
async def obtener_movimientos(request: Request):
    return await forward_request("GET", "/movimientos", request)

@router.get("/movimientos/{id}")
async def obtener_movimiento(id: str, request: Request):
    return await forward_request("GET", f"/movimientos/{id}", request)

@router.patch("/movimientos/{id}")
async def actualizar_movimiento(id: str, request: Request):
    return await forward_request("PATCH", f"/movimientos/{id}", request)

@router.delete("/movimientos/{id}")
async def eliminar_movimiento(id: str, request: Request):
    return await forward_request("DELETE", f"/movimientos/{id}", request)


# ============================
# PRODUCTO
# ============================

@router.post("/producto")
async def crear_producto(request: Request):
    # crear producto sin imágenes
    return await forward_request("POST", "/producto", request)

@router.post("/producto/upload")
async def crear_producto_con_imagenes(request: Request):
    # multipart upload -> reenviamos el body tal cual
    return await forward_request("POST", "/producto/upload", request)

@router.get("/producto")
async def obtener_productos(request: Request):
    return await forward_request("GET", "/producto", request)

@router.get("/producto/{id}")
async def obtener_producto(id: str, request: Request):
    return await forward_request("GET", f"/producto/{id}", request)

@router.patch("/producto/{id}")
async def actualizar_producto(id: str, request: Request):
    # puede incluir o no imágenes
    return await forward_request("PATCH", f"/producto/{id}", request)

@router.patch("/producto/{id}/imagenes")
async def actualizar_imagenes_producto(id: str, request: Request):
    return await forward_request("PATCH", f"/producto/{id}/imagenes", request)

@router.delete("/producto/{id}")
async def eliminar_producto(id: str, request: Request):
    return await forward_request("DELETE", f"/producto/{id}", request)


# ============================
# PROVEEDOR
# ============================

@router.post("/proveedor")
async def crear_proveedor(request: Request):
    return await forward_request("POST", "/proveedor", request)

@router.post("/proveedor/upload")
async def crear_proveedor_con_imagenes(request: Request):
    return await forward_request("POST", "/proveedor/upload", request)

@router.get("/proveedor")
async def obtener_proveedores(request: Request):
    return await forward_request("GET", "/proveedor", request)

@router.get("/proveedor/{id}")
async def obtener_proveedor(id: str, request: Request):
    return await forward_request("GET", f"/proveedor/{id}", request)

@router.patch("/proveedor/{id}")
async def actualizar_proveedor(id: str, request: Request):
    return await forward_request("PATCH", f"/proveedor/{id}", request)

@router.patch("/proveedor/{id}/imagenes")
async def actualizar_imagenes_proveedor(id: str, request: Request):
    return await forward_request("PATCH", f"/proveedor/{id}/imagenes", request)

@router.delete("/proveedor/{id}")
async def eliminar_proveedor(id: str, request: Request):
    return await forward_request("DELETE", f"/proveedor/{id}", request)


# ============================
# SEDE
# ============================

@router.post("/sede")
async def crear_sede(request: Request):
    return await forward_request("POST", "/sede", request)

@router.get("/sede")
async def obtener_sedes(request: Request):
    return await forward_request("GET", "/sede", request)

@router.get("/sede/{id}")
async def obtener_sede(id: str, request: Request):
    return await forward_request("GET", f"/sede/{id}", request)

@router.patch("/sede/{id}")
async def actualizar_sede(id: str, request: Request):
    return await forward_request("PATCH", f"/sede/{id}", request)

@router.delete("/sede/{id}")
async def eliminar_sede(id: str, request: Request):
    return await forward_request("DELETE", f"/sede/{id}", request)


# ============================
# STOCK
# ============================

@router.post("/stock")
async def crear_stock(request: Request):
    return await forward_request("POST", "/stock", request)

@router.get("/stock")
async def obtener_stocks(request: Request):
    return await forward_request("GET", "/stock", request)

@router.get("/stock/{almId}/{prodId}")
async def buscar_stock(almId: str, prodId: str, request: Request):
    return await forward_request("GET", f"/stock/{almId}/{prodId}", request)

@router.patch("/stock/{almId}/{prodId}")
async def actualizar_stock(almId: str, prodId: str, request: Request):
    return await forward_request("PATCH", f"/stock/{almId}/{prodId}", request)

@router.delete("/stock/{almId}/{prodId}")
async def eliminar_stock(almId: str, prodId: str, request: Request):
    return await forward_request("DELETE", f"/stock/{almId}/{prodId}", request)

