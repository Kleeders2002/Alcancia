# Fix para errores de despliegue en Render

## Problema detectado:
Error al importar psycopg2 en Render debido a incompatibilidad con Python 3.14.

## Solución aplicada:

### 1. Agregado `runtime.txt`
Especifica Python 3.11 en lugar de la versión 3.14 que usa Render por defecto.

### 2. Actualizado `render.yaml`
- Agregado explicitamente la versión de Python
- Actualizado el build command con flag `--no-cache-dir`

### 3. Actualizado `requirements.txt`
- Agregadas dependencias faltantes:
  - `pydantic==2.9.2`
  - `python-multipart==0.0.12`

## Pasos para aplicar los cambios en Render:

### Opción 1: Redesplegar automático (recomendado)
Render debería detectar el nuevo commit y redesplegar automáticamente.

### Opción 2: Forzar redespliegue manual
1. Ve a tu dashboard de Render
2. Encuentra el servicio "alcancia-backend"
3. Haz clic en el botón "Manual Deploy"
4. Selecciona "Deploy latest commit"

### Opción 3: Configurar variables de entorno
Asegúrate de tener configurada la variable `DATABASE_URL` en Render:
1. Ve al servicio en Render
2. Haz clic en "Environment"
3. Agrega:
   - **Key:** `DATABASE_URL`
   - **Value:** Tu URL de conexión a Neon PostgreSQL

## Verificar el despliegue:
Después de aplicar los cambios, verifica que:
- ✅ El servicio esté en estado "Live"
- ✅ No haya errores en los logs
- ✅ Puedas acceder a la URL del backend

## URL esperada:
Tu backend debería estar disponible en algo como:
`https://alcancia-backend.onrender.com`

## Prueba de conexión:
Puedes probar si el backend funciona correctamente visitando:
`https://alcancia-backend.onrender.com/api/deposits`

Deberías ver una respuesta JSON con los depósitos.
