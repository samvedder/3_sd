# Proyecto Tarea 3 - Sistemas Distribuidos

## Introducción
Este proyecto tiene como objetivo implementar un sistema distribuido para monitorear tráfico en tiempo real utilizando tecnologías como Apache Kafka, Spark, Cassandra, y Elasticsearch. La arquitectura está diseñada para ser escalable y eficiente, permitiendo capturar datos en tiempo real, procesarlos y almacenarlos para análisis históricos y visualización en tiempo real.

## Requisitos
Asegúrate de tener instalados los siguientes componentes antes de ejecutar el proyecto:
- Docker y Docker Compose
- Python 3.9 o superior
- Acceso a Git para la clonación del repositorio

## Estructura del Proyecto
- **Admin**: Configuración de tópicos en Kafka.
- **Cassandra**: Base de datos distribuida para almacenamiento histórico.
- **DB-Init**: Scripts de inicialización para Cassandra.
- **Kafka-Spark**: Procesamiento en tiempo real entre Kafka y Spark.
- **Scrapper**: Extracción de datos en tiempo real desde Waze.
- **Spark-Cassandra**: Integración entre Spark y Cassandra.
- **Spark-Elasticsearch**: Procesamiento y almacenamiento de datos en Elasticsearch.

## Comandos para levantar los servicios
1. **Levantar toda la infraestructura:**
   ```bash
   sudo docker-compose -f docker-compose.Network.yml -f docker-compose.ApacheKafka.yml -f docker-compose.admin.yml -f docker-compose.Scrapper.yml -f docker-compose.ApacheSpark.yml -f docker-compose.KafkaSpark.yml -f docker-compose.ApacheCassandra.yml -f docker-compose.ElasticSearch.yml up --build
   ```

2. **Ejecutar el scrapper:**
   Una vez levantados los servicios, accede al contenedor del scrapper:
   ```bash
   docker exec -it scrapper bash
   ```
   Dentro del contenedor, ejecuta el script del scrapper:
   ```bash
   python3 scrapper.py
   ```

3. **Consultar datos en Cassandra:**
   Accede al contenedor de Cassandra:
   ```bash
   docker exec -it cassandra cqlsh
   ```
   Dentro de `cqlsh`, ejecuta las siguientes consultas:
   ```sql
   USE test_keyspace;
   SELECT * FROM alerts;
   ```
## Testeo
Para verificar si todo esta en orden, ingresar a localhost:5601 para ver que funcione correctamente el index de elastic y localhost:8090 para kafka.
