from fastapi import APIRouter, Depends, Request, Response
import httpx
import os

router = APIRouter()

USER_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")


# -----------------------------------------
# Helper: reenviar peticiones al microservicio
# -----------------------------------------
async def forward_request(method: str, path: str, request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.body()

        # Headers válidos (evitar errores con host, content-length, etc.)
        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in ["host", "content-length", "connection"]
        }

        # Query params
        query_params = request.query_params

        # Realizar la petición
        response = await client.request(
            method=method,
            url=f"{USER_SERVICE_URL}{path}",
            content=body,
            headers=headers,
            params=query_params,
        )

        # Devolver respuesta compatible con FastAPI
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )


# =====================================================
#                     AUTH
# =====================================================

@router.post("/auth/login")
async def login(request: Request):
    return await forward_request("POST", "/auth/login", request)

@router.post("/auth/register")
async def register(request: Request):
    return await forward_request("POST", "/auth/register", request)

@router.post("/auth/refresh")
async def refresh(request: Request):
    return await forward_request("POST", "/auth/refresh", request)

@router.post("/auth/forgot-password")
async def forgot_password(request: Request):
    return await forward_request("POST", "/auth/forgot-password", request)

@router.post("/auth/reset-password")
async def reset_password(request: Request):
    return await forward_request("POST", "/auth/reset-password", request)

@router.post("/auth/profile")
async def profile(request: Request):
    return await forward_request("POST", "/auth/profile", request)


# =====================================================
#                   DIRECCIONES
# =====================================================

@router.get("/direcciones/usuario/{Usu_id}")
async def direcciones_por_usuario(Usu_id: str, request: Request):
    return await forward_request("GET", f"/direcciones/usuario/{Usu_id}", request)

@router.post("/direcciones/{Usu_id}")
async def crear_direccion(Usu_id: str, request: Request):
    return await forward_request("POST", f"/direcciones/{Usu_id}", request)

@router.put("/direcciones/{Dir_id}")
async def actualizar_direccion(Dir_id: str, request: Request):
    return await forward_request("PUT", f"/direcciones/{Dir_id}", request)

@router.delete("/direcciones/{Dir_id}")
async def eliminar_direccion(Dir_id: str, request: Request):
    return await forward_request("DELETE", f"/direcciones/{Dir_id}", request)


# =====================================================
#                     MASCOTAS
# =====================================================

@router.get("/mascotas/usuario/{Usu_id}")
async def mascotas_por_usuario(Usu_id: str, request: Request):
    return await forward_request("GET", f"/mascotas/usuario/{Usu_id}", request)

@router.post("/mascotas/{Usu_id}")
async def crear_mascota(Usu_id: str, request: Request):
    return await forward_request("POST", f"/mascotas/{Usu_id}", request)

@router.put("/mascotas/{Masc_id}")
async def actualizar_mascota(Masc_id: str, request: Request):
    return await forward_request("PUT", f"/mascotas/{Masc_id}", request)

@router.delete("/mascotas/{Masc_id}")
async def eliminar_mascota(Masc_id: str, request: Request):
    return await forward_request("DELETE", f"/mascotas/{Masc_id}", request)


# =====================================================
#                 MÉTODOS DE PAGO
# =====================================================

@router.get("/metodos-pago/usuario/{Usu_id}")
async def pagos_por_usuario(Usu_id: str, request: Request):
    return await forward_request("GET", f"/metodos-pago/usuario/{Usu_id}", request)

@router.post("/metodos-pago/{Usu_id}")
async def crear_metodo_pago(Usu_id: str, request: Request):
    return await forward_request("POST", f"/metodos-pago/{Usu_id}", request)

@router.put("/metodos-pago/{Met_id}")
async def actualizar_metodo_pago(Met_id: str, request: Request):
    return await forward_request("PUT", f"/metodos-pago/{Met_id}", request)

@router.delete("/metodos-pago/{Met_id}")
async def eliminar_metodo_pago(Met_id: str, request: Request):
    return await forward_request("DELETE", f"/metodos-pago/{Met_id}", request)

@router.put("/metodos-pago/predeterminado/{Usu_id}/{Met_id}")
async def marcar_predeterminado(Usu_id: str, Met_id: str, request: Request):
    return await forward_request("PUT", f"/metodos-pago/predeterminado/{Usu_id}/{Met_id}", request)


# =====================================================
#                   NOTIFICACIONES
# =====================================================

@router.get("/notificaciones/usuario/{Usu_id}")
async def notificaciones_por_usuario(Usu_id: str, request: Request):
    return await forward_request("GET", f"/notificaciones/usuario/{Usu_id}", request)

@router.post("/notificaciones/{Usu_id}")
async def crear_notificacion(Usu_id: str, request: Request):
    return await forward_request("POST", f"/notificaciones/{Usu_id}", request)

@router.put("/notificaciones/leer/{Not_id}")
async def marcar_leida(Not_id: str, request: Request):
    return await forward_request("PUT", f"/notificaciones/leer/{Not_id}", request)

@router.delete("/notificaciones/{Not_id}")
async def eliminar_notificacion(Not_id: str, request: Request):
    return await forward_request("DELETE", f"/notificaciones/{Not_id}", request)


# =====================================================
#                       ROLES
# =====================================================

@router.get("/roles")
async def roles(request: Request):
    return await forward_request("GET", "/roles", request)

@router.get("/roles/{id}")
async def obtener_rol(id: str, request: Request):
    return await forward_request("GET", f"/roles/{id}", request)

@router.post("/roles")
async def crear_rol(request: Request):
    return await forward_request("POST", "/roles", request)

@router.put("/roles/{id}")
async def actualizar_rol(id: str, request: Request):
    return await forward_request("PUT", f"/roles/{id}", request)

@router.delete("/roles/{id}")
async def eliminar_rol(id: str, request: Request):
    return await forward_request("DELETE", f"/roles/{id}", request)


# =====================================================
#                     USUARIOS
# =====================================================

@router.get("/usuarios")
async def usuarios(request: Request):
    return await forward_request("GET", "/usuarios", request)

@router.get("/usuarios/{id}")
async def usuario_por_id(id: str, request: Request):
    return await forward_request("GET", f"/usuarios/{id}", request)

@router.post("/usuarios")
async def crear_usuario(request: Request):
    return await forward_request("POST", "/usuarios", request)

@router.put("/usuarios/{id}")
async def actualizar_usuario(id: str, request: Request):
    return await forward_request("PUT", f"/usuarios/{id}", request)

@router.delete("/usuarios/{id}")
async def eliminar_usuario(id: str, request: Request):
    return await forward_request("DELETE", f"/usuarios/{id}", request)

