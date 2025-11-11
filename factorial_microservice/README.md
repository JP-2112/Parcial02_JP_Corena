# Factorial microservice — Integración de historial

Propósito
--------
Este repositorio contiene un microservicio que calcula el factorial de un número
y, opcionalmente, envía un registro de ese cálculo a otro servicio que persiste
el historial en una base de datos externa. El envío del historial no debe
bloquear ni afectar la respuesta al cliente.

Endpoint principal
------------------
- GET /api/factorial?n={n}

Ejemplo de respuesta (200):

```json
{ "numero": 5, "factorial": "120", "paridad": "par" }
```

Contrato con el servicio de historial (Servicio B)
--------------------------------------------------
- POST /api/historial
  - Body JSON esperado:

```json
{
  "numero": 5,
  "factorial": "120",
  "paridad": "par",
  "timestamp": "2025-11-10T18:00:00Z",
  "source": "factorial-ms"
}
```

Configuración (variables de entorno)
-----------------------------------
- HISTORY_ENABLED=true|false
- HISTORY_BASE_URL=http://localhost:9001
- HISTORY_API_KEY=secret-token  (opcional)

Recomendaciones de diseño 
----------------------------------------------------------
- Envío no bloqueante: construir y devolver la respuesta al cliente y luego
  disparar el envío al servicio B en segundo plano (por ejemplo,
  `asyncio.create_task(try_send_history(data))`).
- Resiliencia: usar timeout corto (p. ej. 2s) y 1–3 reintentos con backoff
  exponencial; atrapar y loggear errores sin propagarlos al endpoint.
- Seguridad y observabilidad: no loggear tokens, usar `Authorization: Bearer ...`
  cuando aplique, y agregar métricas/trazas si se integra OpenTelemetry.
- Criterio de aceptación clave: A responde siempre al cliente aunque B falle.

Alternativa desacoplada (mensajería)
-----------------------------------
Si se necesita mayor resiliencia ante picos o latencias variables, publicar un
evento en una cola (RabbitMQ/Kafka/SQS) con tópico `calculado.factorial` y dejar
que Servicio B consuma y persista. Ventaja: desacople temporal y reintentos
gestionados por el broker; coste: mayor complejidad operativa.

Modelo de datos sugerido en B
----------------------------
Tabla `historial` (ejemplo):
- id (PK)
- numero (INT)
- factorial (TEXT)
- paridad (VARCHAR)
- timestamp (TIMESTAMP)
- source (VARCHAR)

Cómo ejecutar y probar rápido
-----------------------------
Desde la raíz del proyecto:

```powershell
uvicorn app.main:app --reload --port 8000
curl "http://localhost:8000/api/factorial?n=5"
```

Archivos relevantes
------------------
- `app/main.py` — endpoint y cálculo del factorial.
- `app/history_client.py` — cliente HTTP con timeout y manejo básico de errores
  (buena base para añadir reintentos/backoff).

