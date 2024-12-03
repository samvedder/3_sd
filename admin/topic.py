from confluent_kafka.admin import AdminClient, NewTopic

# Configura los brokers en el clúster
admin_client = AdminClient({
    'bootstrap.servers': 'kafka1:9093,kafka2:9095,kafka3:9097',
    'client.id': 'topic-from-python'
})

# Crea nuevos tópicos "alerts" y "jams" con replicación entre brokers
new_topics = [
    NewTopic(topic='alerts', num_partitions=3, replication_factor=3),
    NewTopic(topic='jams', num_partitions=3, replication_factor=3)
]

# Solicitud para crear los tópicos
fs = admin_client.create_topics(new_topics)

for topic, f in fs.items():
    try:
        f.result()  
        print(f"Tópico {topic} creado exitosamente")
    except Exception as e:
        print(f"Fallo al crear el tópico {topic}: {e}")