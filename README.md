# Flights Data Engineering

Pipeline de datos end-to-end sobre el dataset de vuelos domésticos de EE.UU. 2015 (5.8M vuelos).

> Un análisis contesta una pregunta. Un pipeline de datos la contesta todos los días, de forma confiable, sin que nadie tenga que intervenir. En esta tarea construyes ese pipeline: desde los CSVs crudos hasta el análisis estadístico, pasando por una arquitectura Medallion en S3 y Athena, un modelo relacional en PostgreSQL, y un notebook de análisis con regresión y pronóstico de series de tiempo. El dataset es el registro completo de vuelos domésticos en Estados Unidos durante 2015 — 5.8 millones de vuelos, tres tablas, decisiones reales de diseño.

## Objetivo

Al terminar esta tarea habrás construido, de principio a fin, un pipeline de datos sobre el dataset de vuelos de 2015:

- **ETL scripts** (no notebooks) que implementan la arquitectura Medallion Bronze → Silver → Gold sobre S3 y Athena con AWS Glue Data Catalog
- **Modelo relacional** en PostgreSQL provisionado con CloudFormation, cargado con SQLAlchemy y consultado con DBeaver
- **Análisis exploratorio** en Jupyter con visualizaciones sobre las agregaciones Silver y Gold
- **Regresión estadística** con `statsmodels` para identificar los factores que explican el retraso de llegada
- **Pronóstico de series de tiempo** con `StatsForecast` (AutoETS, AutoARIMA, AutoTheta) sobre la demanda mensual de vuelos

---

## Arquitectura

```
CSVs locales  →  Bronze (S3 + Glue)  →  Silver (Parquet + Snappy)  →  Gold (Anthena CTAS) 
↓
PostgresSQL (RDS)
↓
Notebook de análisis
```

---

## ETL — Arquitectura Medallion

| Capa   | Script          | Descripción |
|--------|-----------------|-------------|
| Bronze | `etl/bronze.py` | Sube los tres CSVs a S3 y los registra en Glue |
| Silver | `etl/silver.py` | Transforma a Parquet + Snappy y construye tres agregaciones |
| Gold   | `etl/gold.py`   | Ejecuta el CTAS en Athena para construir la tabla analítica |

---

## Cómo correr el ETL

```bash
python etl/bronze.py --bucket itam-analytics-ana --data-dir data/flights
python etl/silver.py --bucket itam-analytics-ana
python etl/gold.py   --bucket itam-analytics-ana
```
---

## ERD

![ERD](docs/erd-flights.png)

---

## Análisis

El notebook `flights_analytics.ipynb` contiene:
- Queries SQL sobre PostgreSQL (P1-P5, W1-W3)
- Regresión lineal con `statsmodels`
- Pronóstico de series de tiempo con `StatsForecast`

---

## Screenshots 

**Consola AWS Glue confirmando que flights_bronce contiene las tres tablas:**

<img width="1132" height="470" alt="GlueBronze" src="https://github.com/user-attachments/assets/6b098577-562b-4a49-b7bf-c07ca58d30f2" />

---

**Consola AWS Glue confirmando que flights_silver contiene las tablas:**

<img width="1210" height="413" alt="GlueSilver" src="https://github.com/user-attachments/assets/478db2e6-c55d-4590-8f71-a6f1afa7050a" />

**Prueba de las particiones**

<img width="1196" height="443" alt="GlueSilverParts" src="https://github.com/user-attachments/assets/b46395e4-07c9-4491-8bd0-d1d51e5ab7bf" />

---

**Verificar que Anthena devuelve resultados con los nombres de aerolínea y aeropuerto correctamente resueltos**

<img width="1162" height="419" alt="AnthenaQuery" src="https://github.com/user-attachments/assets/e0c29987-d9ba-44f0-9613-9c9a906700ab" />

**Consola AWS Glue confirmando que flights_gold contiene la tabla vuelos_analitica**

<img width="1222" height="353" alt="flights_gold" src="https://github.com/user-attachments/assets/8026bddd-785c-49d9-94ee-3dada4105cb7" />

---

**Consola de CloudFormation con el stack en estado CREATE_COMPLETE**

<img width="1280" height="518" alt="stack_complete" src="https://github.com/user-attachments/assets/99dca873-1844-489c-acdd-267b26eeb78e" />

**Consola de CloudFormation mostrando los Outputs con ambos endpoints**

<img width="1280" height="428" alt="outputs" src="https://github.com/user-attachments/assets/3a8361b3-4c60-49e1-90a0-2bff4b8d367e" />

---

**SELECT COUNT(*) por tabla en DBeaver confirmando la carga**

<img width="972" height="577" alt="dbeaver_carga" src="https://github.com/user-attachments/assets/fa3806b7-03bc-4aa6-a3c8-910a9139ae38" />

**Árbol de esquemas**

<img width="1186" height="463" alt="Árbol de esquemas" src="https://github.com/user-attachments/assets/c113650d-dc47-4cef-9a3f-4534b06e0da9" />

---

**P1 - DBeaver**

<img width="596" height="469" alt="P1" src="https://github.com/user-attachments/assets/bd389734-138c-4d78-8ad6-1e5f38805594" />

**P2 - DBeaver**

<img width="1013" height="640" alt="P2" src="https://github.com/user-attachments/assets/e25cf077-34b0-404b-8371-d048143f5a47" />

**P3 - DBeaver**

<img width="634" height="626" alt="P3" src="https://github.com/user-attachments/assets/a3bfae7a-c137-4dd0-885d-8d43a1f326bb" />

**P4 - DBeaver**

<img width="643" height="549" alt="p4" src="https://github.com/user-attachments/assets/bd113bab-50e0-4096-999b-427569efa5cd" />

**P5 - DBeaver** 

<img width="572" height="720" alt="p5" src="https://github.com/user-attachments/assets/09be64ad-a7ba-4285-ad0f-5f8af6c4a8b2" />

---

**W1 - DBeaver** 

<img width="884" height="720" alt="w1" src="https://github.com/user-attachments/assets/f2a65b17-e9be-48bc-927f-0dcb07f9f64e" />

**W3 - DBeaver**

<img width="971" height="720" alt="w3" src="https://github.com/user-attachments/assets/4e7f9de3-1ac1-4ea7-a3ae-6f6ba363d82d" />











