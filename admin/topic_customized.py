from confluent_kafka.admin import AdminClient, NewTopic

def crear_topico(bootstrap_servers, client_id, nombre_topico, num_particiones, replication_factor):
    admin_client = AdminClient({
        'bootstrap.servers': bootstrap_servers,
        'client.id': client_id
    })

    # Verificar si el tópico ya existe
    topics = admin_client.list_topics().topics
    if nombre_topico in topics:
        print(f"El tópico '{nombre_topico}' ya existe.")
        return

    # Confirmar la creación del tópico
    confirmacion = input(f"¿Estás seguro de que deseas crear el tópico '{nombre_topico}'? (s/n): ")
    if confirmacion.lower() != 's':
        print("Creación de tópico cancelada.")
        return

    fs = admin_client.create_topics([NewTopic(nombre_topico, num_particiones=num_particiones, replication_factor=replication_factor)])

    for topic, f in fs.items():
        try:
            f.result()  
            print(f"Tópico '{topic}' creado exitosamente")
        except Exception as e:
            print(f"Fallo al crear el tópico '{topic}': {e}")

if __name__ == "__main__":
    bootstrap_servers = 'kafka:9093'
    client_id = 'topic-from-python'
    
    # Solicitar datos al usuario
    nombre_topico = input("Introduce el nombre del tópico: ")
    num_particiones = int(input("Introduce el número de particiones: "))
    replication_factor = int(input("Introduce el factor de replicación: "))
    
    crear_topico(bootstrap_servers, client_id, nombre_topico, num_particiones, replication_factor)