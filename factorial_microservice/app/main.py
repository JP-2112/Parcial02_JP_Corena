from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import math

app = FastAPI(title="Factorial Microservice", version="1.0.0")

class FactorialResponse(BaseModel):
    numero: int
    factorial: str
    paridad: str  # "par" o "impar"

def compute_factorial(n: int) -> int:
    # Para evitar tiempos de cómputo excesivos, acotamos n.
    if n < 0:
        raise ValueError("n debe ser >= 0")
    if n > 5000:
        # 5000! es enorme; rechazamos para proteger el servicio
        raise OverflowError("n demasiado grande (máx 5000)")
    # math.factorial es rápido y preciso para enteros arbitrarios
    return math.factorial(n)

@app.get("/api/factorial", response_model=FactorialResponse)
def factorial_endpoint(n: int = Query(..., description="Número entero >= 0")):
    try:
        fact = compute_factorial(n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OverflowError as e:
        raise HTTPException(status_code=413, detail=str(e))  # Payload Too Large (aprox)

    # La paridad debe depender del número ingresado, no del factorial.
    parity = "par" if (n % 2 == 0) else "impar"
    # Convertimos a str para evitar problemas con enteros muy grandes en JSON.
    data = {
        "numero": n,
        "factorial": str(fact),
        "paridad": parity
    }
    return JSONResponse(content=data)

@app.get("/health")
def health():
    return {"status": "ok"}

# Nota: Para enviar historial, podrías hacer algo como:
# from app.history_client import try_send_history
# import asyncio
# asyncio.create_task(try_send_history(data))
