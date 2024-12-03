import json
import os
import time
import requests
from kafka import KafkaProducer

# Configuración de Kafka
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka1:9093,kafka2:9095,kafka3:9097')

# Inicializar productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

keys_to_remove = [
    "comments",
    "reportDescription",
    "nThumbsUp",
    "reportBy",
    "reportByMunicipalityUser",
    "reportRating",
    "reportMood",
    "fromNodeId",
    "toNodeId",
    "magvar",
    "additionalInfo",
    "wazeData"
]

def remove_keys_from_dict(data, keys_to_remove):
    """Función recursiva para eliminar claves específicas de un diccionario."""
    if isinstance(data, list):
        for item in data:
            remove_keys_from_dict(item, keys_to_remove)
    elif isinstance(data, dict):
        for key in keys_to_remove:
            if key in data:
                del data[key]

        for key in data:
            if isinstance(data[key], (dict, list)):
                remove_keys_from_dict(data[key], keys_to_remove)

def scrape_traffic_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta contiene un estado HTTP de error
        data = response.json()

        # Eliminar los atributos innecesarios
        remove_keys_from_dict(data, keys_to_remove=keys_to_remove)

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a {url}: {e}")
        return {}

def main():
    # Establecer la URL predeterminada
    default_url = "https://www.waze.com/live-map/api/georss?top=-33.37380423388275&bottom=-33.418863153828454&left=-70.73255538940431&right=-70.54201126098634&env=row&types=alerts,traffic"

    url = input(f"Ingrese la URL a hacer scraping (predeterminada: {default_url}): ")
    if not url:
        url = default_url

    print(f"Scrapeando datos de la URL: {url}")

    while True:
        try:
            print("Extrayendo datos de tráfico...")
            traffic_data = scrape_traffic_data(url)

            # Separar los datos en dos partes: alerts y jams
            alerts_data = traffic_data.get("alerts", [])
            jams_data = traffic_data.get("jams", [])

            # Enviar los datos de "alerts" al tópico "alerts"
            for alert in alerts_data:
                producer.send('alerts', alert)
                print(f"Alerta enviada a Kafka: {alert}")

            # Enviar los datos de "jams" al tópico "jams"
            for jam in jams_data:
                producer.send('jams', jam)
                print(f"Jam enviado a Kafka: {jam}")

            time.sleep(10)
        except Exception as e:
            print(f"Error en el scraper: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
