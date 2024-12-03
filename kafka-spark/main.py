from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType,
    BooleanType, LongType
)
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_to_cassandra(batch_df, batch_id):
    try:
        row_count = batch_df.count()
        logger.info(f"Batch {batch_id}: Escribiendo {row_count} filas en Cassandra.")
        if row_count > 0:
            batch_df.write \
                .format("org.apache.spark.sql.cassandra") \
                .mode("append") \
                .options(table="alerts", keyspace="test_keyspace") \
                .save()
            logger.info(f"Batch {batch_id}: Escritura a Cassandra completada.")
        else:
            logger.info(f"Batch {batch_id}: No hay filas para escribir en Cassandra.")
    except Exception as e:
        logger.error(f"Batch {batch_id}: Error al escribir en Cassandra - {e}")

def main():
    # Crear una sesión de Spark con las configuraciones necesarias
    spark = SparkSession.builder \
        .appName("KafkaSparkIntegrationAlerts") \
        .config("spark.sql.adaptive.enabled", "false") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,"
                "org.elasticsearch:elasticsearch-spark-30_2.12:8.6.2,"
                "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0") \
        .config("spark.cassandra.connection.host", "cassandra") \
        .getOrCreate()

    # Configurar el nivel de registro para reducir la verbosidad
    spark.sparkContext.setLogLevel("WARN")

    # Definir la dirección de los brokers de Kafka
    kafka_bootstrap_servers = "kafka1:9093,kafka2:9095,kafka3:9097"

    # Definir el esquema de los datos que se esperan recibir desde Kafka
    alerts_schema = StructType([
        StructField("country", StringType(), True),
        StructField("city", StringType(), True),
        StructField("reliability", IntegerType(), True),
        StructField("type", StringType(), True),
        StructField("uuid", StringType(), True),
        StructField("speed", IntegerType(), True),
        StructField("subtype", StringType(), True),
        StructField("street", StringType(), True),
        StructField("id", StringType(), True),
        StructField("ncomments", IntegerType(), True),  # En minúsculas
        StructField("inscale", BooleanType(), True),
        StructField("confidence", IntegerType(), True),
        StructField("roadtype", IntegerType(), True),   # En minúsculas
        StructField("location_x", DoubleType(), True),  # Separado en x
        StructField("location_y", DoubleType(), True),  # Separado en y
        StructField("pubmillis", LongType(), True)      # En minúsculas
    ])

    # Leer el stream desde Kafka
    alerts_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", "alerts") \
        .option("startingOffsets", "earliest") \
        .load()

    # Convertir los datos binarios de Kafka a cadenas de texto
    alerts_strings = alerts_df.selectExpr("CAST(value AS STRING) as json_str")

    # Parsear el JSON y aplicar el esquema definido
    alerts_parsed = alerts_strings.select(from_json(col("json_str"), alerts_schema).alias("data")).select("data.*")

    # Filtrar alertas con alta confiabilidad
    high_reliability_alerts = alerts_parsed.filter(col("reliability") >= 7)

    # Escribir los datos procesados en ElasticSearch
    es_query = high_reliability_alerts.writeStream \
        .outputMode("append") \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "elasticsearch") \
        .option("es.port", "9200") \
        .option("checkpointLocation", "/tmp/spark/checkpoints_elasticsearch") \
        .start("alerts")

    # Escribir los datos procesados en Cassandra
    cassandra_query = high_reliability_alerts.writeStream \
        .outputMode("append") \
        .foreachBatch(write_to_cassandra) \
        .option("checkpointLocation", "/tmp/spark/checkpoints_cassandra") \
        .start()

    # Escribir los resultados en la consola con ubicación de checkpoints
    console_query = high_reliability_alerts.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .option("checkpointLocation", "/tmp/spark/checkpoints_console") \
        .start()

    # Esperar a que las consultas terminen
    es_query.awaitTermination()
    cassandra_query.awaitTermination()
    console_query.awaitTermination()

if __name__ == "__main__":
    main()
