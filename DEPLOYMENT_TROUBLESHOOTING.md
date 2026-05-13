# Solución de Problemas de Despliegue en Render

## Problemas Comunes y Soluciones

### 1. Error: "Read-only file system" al compilar pydantic-core

**Síntoma:**
```
error: failed to create directory `/usr/local/cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`
Caused by: Read-only file system (os error 30)
```

**Causa:**
Las dependencias con versiones específicas requieren compilación desde el código fuente (necesitan Rust), pero Render tiene restricciones en el sistema de archivos.

**Solución:**
Usar versiones sin especificar números de versión exactos para obtener binarios precompilados:
```txt
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
python-multipart
pydantic
```

### 2. Error: "ImportError: No module named 'psycopg2'"

**Síntoma:**
```
ImportError: No module named 'psycopg2'
```

**Causa:**
Falta el driver de PostgreSQL o hay problemas de compatibilidad de versión de Python.

**Solución:**
- Usar `psycopg2-binary` en lugar de `psycopg2`
- Especificar Python 3.11 en `runtime.txt` (no usar 3.14+)

### 3. Timeout de conexión a la base de datos

**Síntoma:**
La aplicación responde pero la API da errores de conexión a la base de datos.

**Causa:**
Render tiene un sistema de "sleep" que detiene servicios gratuitos después de inactividad.

**Solución:**
- Usar servicios con planes de pago o
- Implementar health checks para mantener el servicio activo

## Configuración Correcta para Render

### runtime.txt
```
3.11
```

### requirements.txt (sin versiones específicas)
```
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
python-multipart
pydantic
```

### render.yaml
```yaml
services:
  - type: web
    name: alcancia-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: PORT
        value: 10000
```

## Variables de Entorno Requeridas

En Render, debes configurar:

### DATABASE_URL
```
postgresql://usuario:password@host:puerto/database?sslmode=require
```

Ejemplo para Neon:
```
postgresql://neondb_owner:npg_XXX@ep-XXX.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## Pasos para Despliegue Exitoso

1. **Preparar el repositorio**
   - Crear `runtime.txt` con Python 3.11
   - Simplificar `requirements.txt` sin versiones específicas

2. **Configurar variables de entorno en Render**
   - `DATABASE_URL`: Tu URL de conexión a Neon

3. **Conectar el repositorio en Render**
   - New Web Service
   - Importar desde GitHub
   - Configurar build y start commands

4. **Monitorear el despliegue**
   - Revisar los logs en tiempo real
   - Verificar que no haya errores de compilación
   - Probar la API: `/api/deposits`

## Verificación de Despliegue

Una vez desplegado, verifica:

```bash
# Prueba de la API
curl https://tu-backend.onrender.com/api/deposits

# Deberías ver algo como:
# [{"person": "Ambos", "amount": 455.0, "timestamp": "2026-04-17 20:08:54"}]
```

## Recursos Adicionales

- [Render Python Deployment Guide](https://render.com/docs/deploy-python)
- [Neon PostgreSQL Documentation](https://neon.tech/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## Soporte

Si encuentras otros problemas:
1. Revisa los logs en tiempo real de Render
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que la base de datos esté accesible desde Render
4. Verifica la versión de Python especificada en `runtime.txt`
