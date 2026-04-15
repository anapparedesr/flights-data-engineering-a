import sys
import argparse
import logging
import os

import pandas as pd
import awswrangler as wr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)


def extract(data_dir: str) -> dict:
    """Valida que los tres archivos existen y no están vacíos."""
    archivos = {
        "flights": "flights.csv",
        "airlines": "airlines.csv",
        "airports": "airports.csv"
    }
    rutas = {}

    for nombre, archivo in archivos.items():
        ruta = f"{data_dir}/{archivo}"
        try:
            assert os.path.exists(ruta), f"No se encontró el archivo {ruta}"
            assert os.path.getsize(ruta) > 0, f"{archivo} está vacío"
            logger.info(f"{nombre}: archivo encontrado — {os.path.getsize(ruta) / 1e6:.1f} MB")
            rutas[nombre] = ruta
        except AssertionError as e:
            logger.exception(f"Validación fallida: {e}")
            sys.exit(1)

    return rutas


def load(rutas: dict, bucket: str) -> None:
    """Sube los tres CSVs a S3 en Parquet y los registra en Glue."""
    try:
        logger.info("Creando base de datos flights_bronze en Glue...")
        wr.catalog.create_database("flights_bronze", exist_ok=True)
    except Exception:
        logger.exception("Error creando la base de datos en Glue")
        sys.exit(1)

    # flights — se carga en chunks por su tamaño
    try:
        ruta_s3 = f"s3://{bucket}/flights/bronze/flights/"
        logger.info(f"Subiendo flights a {ruta_s3} en chunks...")
        
        df_iter = pd.read_csv(rutas["flights"], chunksize=100_000)
        total_filas = 0
        primer_chunk = True

        for chunk in df_iter:
            wr.s3.to_parquet(
                df=chunk,
                path=ruta_s3,
                dataset=True,
                database="flights_bronze",
                table="flights",
                mode="overwrite" if primer_chunk else "append"
            )
            total_filas += len(chunk)
            primer_chunk = False
            logger.info(f"flights: {total_filas:,} filas procesadas...")

        logger.info(f"flights: subido exitosamente — {total_filas:,} filas totales — {ruta_s3}")

    except Exception:
        logger.exception("Error subiendo flights a S3")
        sys.exit(1)

    # airlines y airports — pequeños, se cargan de un jalón
    for nombre in ["airlines", "airports"]:
        ruta_s3 = f"s3://{bucket}/flights/bronze/{nombre}/"
        try:
            logger.info(f"Subiendo {nombre} a {ruta_s3}...")
            df = pd.read_csv(rutas[nombre])

            assert not df.empty, f"{nombre} está vacío"

            wr.s3.to_parquet(
                df=df,
                path=ruta_s3,
                dataset=True,
                database="flights_bronze",
                table=nombre,
                mode="overwrite"
            )
            logger.info(f"{nombre}: subido exitosamente — {len(df):,} filas — {ruta_s3}")

        except AssertionError as e:
            logger.exception(f"Validación fallida: {e}")
            sys.exit(1)
        except Exception:
            logger.exception(f"Error subiendo {nombre} a S3")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--data-dir", default="data/")
    args = parser.parse_args()

    rutas = extract(args.data_dir)
    load(rutas, args.bucket)


if __name__ == "__main__":
    main()