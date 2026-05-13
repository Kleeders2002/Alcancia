# 🐷 Alcancia Virtual

Aplicación web para el ahorro en pareja de Jessica y Kleeders para su primer viaje juntos.

## 📋 Descripción

Alcancia virtual que permite registrar, visualizar y gestionar depósitos hacia una meta de **$1,200 USD** con fecha límite el **31 de diciembre de 2026**.

## 🏗️ Arquitectura

- **Frontend:** HTML5 + CSS3 + JavaScript vanilla
- **Backend:** FastAPI (Python)
- **Base de datos:** PostgreSQL (Neon)

## 🚀 Despliegue

### Backend (Render)

1. Ve a [Render.com](https://render.com) y crea una cuenta
2. Conecta tu repositorio GitHub: `https://github.com/Kleeders2002/Alcancia`
3. Crea un nuevo **Web Service**
4. Configura:
   - **Name:** alcancia-backend
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Variables de entorno:**
   - `DATABASE_URL`: Tu URL de conexión a Neon PostgreSQL
6. Haz clic en "Create Web Service"

### Frontend (Vercel)

1. Ve a [Vercel.com](https://vercel.com) y crea una cuenta
2. Crea un nuevo proyecto importando: `https://github.com/Kleeders2002/Alcancia`
3. Configura:
   - **Framework Preset:** Other
   - **Root Directory:** `./` (raíz del proyecto)
   - **Build Command:** (dejar vacío)
   - **Output Directory:** `./`
4. En **Environment Variables** agrega:
   - `API_URL`: URL de tu backend en Render (ej: `https://alcancia-backend.onrender.com`)
5. Haz clic en "Deploy"

## 🔧 Configuración Local

### Instalación

```bash
pip install -r requirements.txt
```

### Ejecutar servidor local

```bash
python -m uvicorn main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## 📊 Base de Datos

La aplicación usa **PostgreSQL** hosted en **Neon**.

### Estructura de la tabla `deposits`:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | Integer | Primary Key (auto-increment) |
| person | String | "Jessica", "Kleeders", "Ambos" |
| amount | Float | Monto del depósito |
| timestamp | String | Fecha y hora del depósito |

## 🎯 Características

- ✅ Registro de depósitos por persona
- ✅ Visualización de progreso en tiempo real
- ✅ Historial completo de transacciones
- ✅ Contador de días para la meta
- ✅ Eliminación de depósitos
- ✅ Interfaz romántica y motivacional
- ✅ Diseño responsive

## 🌐 API Endpoints

- `GET /api/deposits` - Obtener todos los depósitos
- `POST /api/deposits` - Agregar nuevo depósito
- `DELETE /api/deposits/{index}` - Eliminar depósito
- `GET /` - Servir frontend

## 💡 Notas

- La base de datos está configurada para PostgreSQL en Neon
- Los datos se guardan automáticamente en la base de datos
- No se usan archivos locales para almacenamiento
- CORS está configurado para permitir todas las origins (configurar para producción)

## 👥 Usuarios

- **Jessica:** Registro de depósitos individuales
- **Kleeders:** Registro de depósitos individuales
- **Ambos:** Registro de depósitos conjuntos

## 📅 Meta del Proyecto

- **Meta:** $1,200 USD
- **Fecha límite:** 31 de diciembre de 2026
- **Objetivo:** Primer viaje juntos

---

**¡Juntos lo van a lograr!** 💑✈️
