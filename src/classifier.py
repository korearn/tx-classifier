import requests
import json

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

CATEGORIES = [
    "Alimentación",
    "Transporte",
    "Entretenimiento",
    "Servicios",
    "Salud",
    "Compras online",
    "Transferencias",
    "Retiros en efectivo",
    "Suscripciones",
    "Otros"
]

def build_prompt(description: str, amount: float) -> str:

    categories_list = "\n".join(f"- {cat}" for cat in CATEGORIES)
    
    return f"""Eres un clasificador de transacciones bancarias. 
Tu tarea es clasificar la siguiente transacción en exactamente UNA de las categorías listadas.

Transacción:
- Descripción: {description}
- Monto: ${amount} MXN

Categorías disponibles:
{categories_list}

Responde ÚNICAMENTE con un objeto JSON con este formato exacto, sin texto adicional:
{{"category": "nombre_categoria", "confidence": "alta|media|baja"}}"""


def classify_transaction(description: str, amount: float) -> dict:

    payload = {
        "model": "local-model",
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente especializado en finanzas personales. Respondes siempre en JSON válido, sin explicaciones adicionales."
            },
            {
                "role": "user", 
                "content": build_prompt(description, amount)
            }
        ],
        "temperature": 0.1, 
        "max_tokens": 100
    }
    
    try:
        response = requests.post(
            LMSTUDIO_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        content = response.json()["choices"][0]["message"]["content"].strip()
        
        
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        result = json.loads(content)
        
        if result.get("category") not in CATEGORIES:
            result["category"] = "Otros"
            result["confidence"] = "baja"
            
        return result
        
    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar a LMStudio. ¿Está corriendo el servidor?")
        return {"category": "Otros", "confidence": "baja"}
    except json.JSONDecodeError:
        print(f"Error: El modelo no respondió con JSON válido. Respuesta: {content}")
        return {"category": "Otros", "confidence": "baja"}