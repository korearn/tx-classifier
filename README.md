# TX-Classifier 🏦

Clasificador automático de transacciones bancarias usando modelos de lenguaje locales (LLM) mediante LMStudio. Sin APIs externas, sin costos, 100% privado.

## ¿Qué hace?

- Lee transacciones desde un archivo CSV
- Clasifica cada transacción en categorías usando un LLM local
- Almacena los resultados en SQLite
- Genera un resumen de gastos por categoría

## Stack técnico

- **Python 3.12** — lenguaje principal
- **LMStudio** — servidor local de LLM (compatible con Qwen, Gemma, Deepseek, entre otros)
- **SQLite** — almacenamiento de resultados
- **Pandas** — procesamiento de CSV
- **Rich** — visualización en terminal

## Estructura
```
tx-classifier/
├── data/               # CSVs de entrada (no versionados)
├── src/
│   ├── classifier.py   # Integración con LLM local
│   ├── database.py     # Capa de datos SQLite
│   └── main.py         # Punto de entrada
└── requirements.txt
```

## Instalación
```bash
git clone https://github.com/tu-usuario/tx-classifier
cd tx-classifier
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

1. Inicia LMStudio y carga un modelo (Qwen2.5, Gemma 3, etc.)
2. Activa el servidor local en `http://localhost:1234`
3. Coloca tu archivo CSV en `data/transactions.csv`
4. Ejecuta:
```bash
cd src
python main.py
```

## Formato del CSV de entrada
```csv
date,description,amount,currency
2024-01-03,OXXO SUCURSAL 234,156.50,MXN
```

## Categorías soportadas

`Alimentación` · `Transporte` · `Entretenimiento` · `Servicios` · `Salud` · `Compras online` · `Transferencias` · `Retiros en efectivo` · `Suscripciones` · `Otros`